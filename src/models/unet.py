"""
Standard U-Net Architecture (Ronneberger et al., 2015)
======================================================
Deep Learning Baseline for Retinal Blood Vessel Segmentation
(Experiment 2: ML/DL-based Technique)

Input: 3-channel RGB Fundus (no domain-specific morphological channel)
Output: 1-channel binary vessel probability map
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class DoubleConv(nn.Module):
    """(Conv -> BatchNorm -> ReLU) * 2"""
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.conv(x)


class UNet(nn.Module):
    """
    Standard U-Net for medical image segmentation.
    Used as the classical Deep Learning benchmark to compare against Morph-ViT.
    """
    def __init__(self, in_channels: int = 3, out_channels: int = 1, base_filters: int = 32):
        super().__init__()
        self.inc = DoubleConv(in_channels, base_filters)
        self.down1 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(base_filters, base_filters * 2))
        self.down2 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(base_filters * 2, base_filters * 4))
        self.down3 = nn.Sequential(nn.MaxPool2d(2), DoubleConv(base_filters * 4, base_filters * 8))

        self.up1 = nn.ConvTranspose2d(base_filters * 8, base_filters * 4, kernel_size=2, stride=2)
        self.conv_up1 = DoubleConv(base_filters * 8, base_filters * 4)

        self.up2 = nn.ConvTranspose2d(base_filters * 4, base_filters * 2, kernel_size=2, stride=2)
        self.conv_up2 = DoubleConv(base_filters * 4, base_filters * 2)

        self.up3 = nn.ConvTranspose2d(base_filters * 2, base_filters, kernel_size=2, stride=2)
        self.conv_up3 = DoubleConv(base_filters * 2, base_filters)

        self.outc = nn.Conv2d(base_filters, out_channels, kernel_size=1)

    def forward(self, x):
        # Handle 4-channel input if passed by extracting only first 3 RGB channels
        if x.shape[1] == 4:
            x = x[:, :3, :, :]

        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)

        u1 = self.up1(x4)
        if u1.shape[2:] != x3.shape[2:]:
            u1 = F.interpolate(u1, size=x3.shape[2:], mode='bilinear', align_corners=True)
        u1 = torch.cat([u1, x3], dim=1)
        u1 = self.conv_up1(u1)

        u2 = self.up2(u1)
        if u2.shape[2:] != x2.shape[2:]:
            u2 = F.interpolate(u2, size=x2.shape[2:], mode='bilinear', align_corners=True)
        u2 = torch.cat([u2, x2], dim=1)
        u2 = self.conv_up2(u2)

        u3 = self.up3(u2)
        if u3.shape[2:] != x1.shape[2:]:
            u3 = F.interpolate(u3, size=x1.shape[2:], mode='bilinear', align_corners=True)
        u3 = torch.cat([u3, x1], dim=1)
        u3 = self.conv_up3(u3)

        logits = self.outc(u3)
        return logits

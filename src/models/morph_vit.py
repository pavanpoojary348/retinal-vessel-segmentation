"""
Retinal Blood Vessel Segmentation - Morphology-Guided Vision Transformer (Morph-ViT)
===================================================================================
Fundamental of Image Processing (FIP) Course Project

A hybrid Vision Transformer architecture designed for medical fundus segmentation:
1. Multi-scale morphological feature integration (fusing classical FIP filters with deep attention)
2. Configurable Patch Embedding (patch size P x P)
3. Multi-Head Self-Attention (MHSA) Transformer Encoder with configurable depth and attention heads
4. High-resolution convolutional decoder with skip connections to preserve thin vessels
5. Binary vessel probability map output [0, 1]
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class PatchEmbedding(nn.Module):
    """
    Splits image/feature map into non-overlapping patches and projects them
    to an embedding dimension D.
    """
    def __init__(self, in_channels: int = 4, patch_size: int = 16, embed_dim: int = 128):
        super().__init__()
        self.patch_size = patch_size
        self.proj = nn.Conv2d(
            in_channels, embed_dim,
            kernel_size=patch_size, stride=patch_size
        )
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        # x: (B, C, H, W)
        B, C, H, W = x.shape
        x = self.proj(x)  # (B, embed_dim, H/P, W/P)
        Hp, Wp = x.shape[2], x.shape[3]
        x = x.flatten(2).transpose(1, 2)  # (B, num_patches, embed_dim)
        x = self.norm(x)
        return x, Hp, Wp


class TransformerBlock(nn.Module):
    """
    Standard Vision Transformer Encoder Layer:
    LayerNorm -> Multi-Head Self-Attention -> Residual ->
    LayerNorm -> Feed-Forward MLP (GELU) -> Residual.
    """
    def __init__(self, embed_dim: int = 128, num_heads: int = 4, mlp_ratio: float = 2.0, dropout: float = 0.1):
        super().__init__()
        self.norm1 = nn.LayerNorm(embed_dim)
        self.attn = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )
        self.norm2 = nn.LayerNorm(embed_dim)
        mlp_hidden_dim = int(embed_dim * mlp_ratio)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, mlp_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mlp_hidden_dim, embed_dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        # Self-attention with pre-norm and residual
        norm_x = self.norm1(x)
        attn_out, _ = self.attn(norm_x, norm_x, norm_x)
        x = x + attn_out
        # MLP with pre-norm and residual
        x = x + self.mlp(self.norm2(x))
        return x


class DecoderBlock(nn.Module):
    """Convolutional upsampling block with skip connection."""
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int):
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
        total_in = in_channels + skip_channels
        self.conv = nn.Sequential(
            nn.Conv2d(total_in, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x, skip=None):
        x = self.up(x)
        if skip is not None:
            # Handle slight odd-dimension shape differences via interpolation
            if x.shape[2:] != skip.shape[2:]:
                x = F.interpolate(x, size=skip.shape[2:], mode='bilinear', align_corners=True)
            x = torch.cat([x, skip], dim=1)
        return self.conv(x)


class MorphologyVisionTransformer(nn.Module):
    """
    Morphology-Guided Vision Transformer (Morph-ViT) for Retinal Vessel Segmentation.

    Parameters:
    - in_channels: 4 (RGB Fundus channels + 1 Morphological Top-Hat enhanced channel)
    - patch_size: Size of patch embedding (e.g. 8 or 16)
    - embed_dim: Embedding dimension of Transformer tokens (e.g. 128 or 256)
    - depth: Number of Transformer Encoder layers
    - num_heads: Number of Multi-Head Self-Attention heads
    - mlp_ratio: Expansion ratio for Transformer MLP
    - dropout: Dropout probability
    """
    def __init__(
        self,
        in_channels: int = 4,
        patch_size: int = 16,
        embed_dim: int = 128,
        depth: int = 4,
        num_heads: int = 4,
        mlp_ratio: float = 2.0,
        dropout: float = 0.1
    ):
        super().__init__()
        self.patch_size = patch_size
        self.embed_dim = embed_dim
        self.depth = depth
        self.num_heads = num_heads

        # Low-level CNN stem to extract fine local vessel features for skip connections
        self.stem = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )

        # ViT Patch embedding
        self.patch_embed = PatchEmbedding(
            in_channels=in_channels,
            patch_size=patch_size,
            embed_dim=embed_dim
        )

        # Transformer encoder layers
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(embed_dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, dropout=dropout)
            for _ in range(depth)
        ])
        self.norm = nn.LayerNorm(embed_dim)

        # Decoder upsampling stages
        # Assuming patch_size = 16 (upsample factor 16 = 2 * 2 * 2 * 2)
        # Or patch_size = 8  (upsample factor 8  = 2 * 2 * 2)
        self.dec1 = DecoderBlock(embed_dim, 0, 64)
        self.dec2 = DecoderBlock(64, 0, 32)
        self.dec3 = DecoderBlock(32, 64, 32)   # Skip connection with stem output
        self.final_conv = nn.Sequential(
            nn.Conv2d(32, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 1, kernel_size=1)
        )

    def forward(self, x):
        """
        Input:
        - x: (B, 4, H, W) -> 3 RGB channels + 1 Morphological Top-Hat enhanced channel
        Output:
        - logits: (B, 1, H, W)
        """
        orig_h, orig_w = x.shape[2], x.shape[3]

        # 1. Low-level skip feature from CNN stem
        stem_feat = self.stem(x)  # (B, 64, H, W)

        # 2. Vision Transformer tokenization & self-attention
        tokens, hp, wp = self.patch_embed(x)  # (B, num_patches, embed_dim)

        # Add 1D Learnable Positional Encoding dynamically interpolated
        B, N, D = tokens.shape
        pos_embed = self._get_positional_encoding(N, D, tokens.device)
        tokens = tokens + pos_embed

        for block in self.transformer_blocks:
            tokens = block(tokens)
        tokens = self.norm(tokens)

        # Reshape tokens back to 2D spatial feature map
        feat_2d = tokens.transpose(1, 2).reshape(B, D, hp, wp)  # (B, embed_dim, hp, wp)

        # 3. Progressive Decoder with skip connections
        d1 = self.dec1(feat_2d)  # 2x up
        d2 = self.dec2(d1)       # 4x up
        # Match size of d2 with stem_feat for skip concatenation
        if d2.shape[2:] != stem_feat.shape[2:]:
            d2 = F.interpolate(d2, size=stem_feat.shape[2:], mode='bilinear', align_corners=True)
        d3 = self.dec3(d2, skip=stem_feat)

        out = self.final_conv(d3)
        if out.shape[2:] != (orig_h, orig_w):
            out = F.interpolate(out, size=(orig_h, orig_w), mode='bilinear', align_corners=True)

        return out

    def _get_positional_encoding(self, num_patches: int, embed_dim: int, device):
        pe = torch.zeros(1, num_patches, embed_dim, device=device)
        position = torch.arange(0, num_patches, dtype=torch.float, device=device).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2, dtype=torch.float, device=device) * (-math.log(10000.0) / embed_dim))
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        return pe


class DiceBCELoss(nn.Module):
    """
    Combined Binary Cross-Entropy (with class weighting) and Dice Loss.
    Optimizes both pixel-level accuracy and vascular structure overlap,
    resolving extreme vessel class imbalance (~10% vessel, ~90% background).
    """
    def __init__(self, pos_weight: float = 4.0, dice_weight: float = 1.0, eps: float = 1e-6):
        super().__init__()
        self.pos_weight = torch.tensor([pos_weight])
        self.dice_weight = dice_weight
        self.eps = eps

    def forward(self, logits, targets, fov_mask=None):
        if self.pos_weight.device != logits.device:
            self.pos_weight = self.pos_weight.to(logits.device)

        probs = torch.sigmoid(logits)

        # Mask invalid pixels outside Field of View (FOV)
        if fov_mask is not None:
            mask = (fov_mask > 0).float()
            bce = F.binary_cross_entropy_with_logits(
                logits, targets, pos_weight=self.pos_weight, reduction='none'
            )
            bce = (bce * mask).sum() / (mask.sum() + self.eps)

            probs_masked = probs * mask
            targets_masked = targets * mask
            intersection = (probs_masked * targets_masked).sum()
            dice = 1.0 - (2.0 * intersection + self.eps) / (probs_masked.sum() + targets_masked.sum() + self.eps)
        else:
            bce = F.binary_cross_entropy_with_logits(
                logits, targets, pos_weight=self.pos_weight
            )
            intersection = (probs * targets).sum()
            dice = 1.0 - (2.0 * intersection + self.eps) / (probs.sum() + targets.sum() + self.eps)

        return bce + self.dice_weight * dice

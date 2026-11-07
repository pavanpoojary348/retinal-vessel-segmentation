"""
Retinal Blood Vessel Segmentation - Unified Entry Point
========================================================
FIP Course Project

    python main.py train                        -- train the model
    python main.py evaluate                     -- evaluate on training split
    python main.py predict --image <path>       -- predict on a single image
    python main.py visualise                    -- plot training curves + sample panels
    python main.py all                          -- train -> evaluate -> visualise

Run any sub-command with --help for its full option list.
"""

import sys, os, argparse, subprocess

def run_script(script_path, extra_args):
    cmd = [sys.executable, script_path] + extra_args
    print(f"\n>>> Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Morph-ViT Retinal Vessel Segmentation -- Unified Entry Point",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", choices=["train","evaluate","predict","visualise","all"],
        help="train / evaluate / predict / visualise / all")
    parser.add_argument("--data_root",  type=str, default="data/raw")
    parser.add_argument("--output_dir", type=str, default="outputs")
    parser.add_argument("--checkpoint", type=str, default="outputs/checkpoints/best_model.pth")
    parser.add_argument("--image",      type=str, default=None)
    parser.add_argument("--fov",        type=str, default=None)
    args, extra = parser.parse_known_args()

    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

    def _train():
        run_script(os.path.join(src_dir, "train.py"),
                   ["--data_root", args.data_root, "--output_dir", args.output_dir] + extra)

    def _evaluate():
        run_script(os.path.join(src_dir, "evaluate.py"),
                   ["--data_root", args.data_root, "--checkpoint", args.checkpoint,
                    "--output_dir", args.output_dir, "--split", "training"] + extra)

    def _predict():
        if args.image is None:
            print("Error: --image is required for the predict command."); sys.exit(1)
        predict_args = ["--image", args.image, "--checkpoint", args.checkpoint,
                        "--output_dir", os.path.join(args.output_dir, "predictions")]
        if args.fov:
            predict_args += ["--fov", args.fov]
        run_script(os.path.join(src_dir, "predict.py"), predict_args + extra)

    def _visualise():
        log_path = os.path.join(args.output_dir, "train_log.csv")
        if not os.path.exists(log_path):
            print(f"[WARN] Training log not found at {log_path} -- skipping training curves.")
        else:
            sys.path.insert(0, src_dir)
            from visualise import plot_training_curves
            curves_path = os.path.join(args.output_dir, "training_curves.png")
            plot_training_curves(log_path, save_path=curves_path)
            print(f"Training curves saved: {curves_path}")

        results_dir = os.path.join(args.output_dir, "results")
        panels_dir  = os.path.join(args.output_dir, "panels")
        os.makedirs(panels_dir, exist_ok=True)

        import glob, numpy as np
        from PIL import Image as PILImage

        pred_files = sorted(glob.glob(os.path.join(results_dir, "*_pred_binary.png")))
        if not pred_files:
            print("[INFO] No prediction files found in outputs/results/. Run evaluate first.")
            return

        sys.path.insert(0, src_dir)
        from dataset import DRIVEDataset, load_image
        from morphology import enhance_retinal_vessels
        from visualise import plot_sample_panel

        ds = DRIVEDataset(root_dir=args.data_root, split="training",
                          img_size=(576,576), augment=False)
        for sample_data in ds.samples[:5]:
            img_id    = sample_data["image_id"]
            prob_path = os.path.join(results_dir, f"{img_id}_pred_prob.npy")
            bin_path  = os.path.join(results_dir, f"{img_id}_pred_binary.png")
            if not os.path.exists(prob_path): continue

            rgb   = load_image(sample_data["img_path"],  size=(576,576), mode="RGB")
            fov   = load_image(sample_data["fov_path"],  size=(576,576), mode="L")
            lbl   = load_image(sample_data["lbl_path"],  size=(576,576), mode="L") if sample_data["lbl_path"] else np.zeros((576,576), dtype=np.uint8)
            morph = enhance_retinal_vessels(rgb, fov_mask=fov)["morph_enhanced"]
            prob  = np.load(prob_path)
            binary_arr = np.array(PILImage.open(bin_path).convert("L"))

            panel_path = os.path.join(panels_dir, f"{img_id}_panel.png")
            plot_sample_panel(rgb=rgb, fov=fov, label=lbl, morph=morph,
                              pred_prob=prob, pred_binary=binary_arr,
                              title=f"Morph-ViT Prediction -- {img_id}",
                              save_path=panel_path)
            print(f"  Saved panel: {panel_path}")

    if args.command == "train":        _train()
    elif args.command == "evaluate":   _evaluate()
    elif args.command == "predict":    _predict()
    elif args.command == "visualise":  _visualise()
    elif args.command == "all":
        _train(); _evaluate(); _visualise()

if __name__ == "__main__":
    main()

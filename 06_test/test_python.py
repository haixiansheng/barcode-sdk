"""
Barcode Detection SDK — Python 推理测试
=========================================
【伪代码 / Pseudocode】
展示 Python 推理测试流程。
"""

import os
import sys
import time
import json
sys.path.insert(0, str(os.path.dirname(__file__) + "/../05_deployment/python"))
from barcode_detector import BarcodeDetector


def run_tests(model_path, img_dir, conf=0.30):
    """运行推理测试。"""
    print(f"Python Inference Test")
    print(f"  Model: {model_path}")
    print(f"  Images: {img_dir}")

    detector = BarcodeDetector(model_path, conf_thresh=conf)

    image_files = sorted([
        f for f in os.listdir(img_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    total_dets = 0
    for img_file in image_files:
        img_path = os.path.join(img_dir, img_file)
        start = time.time()
        detections = detector.detect(img_path)
        elapsed = (time.time() - start) * 1000

        total_dets += len(detections)
        print(f"  {img_file:30s} -> {len(detections):3d} barcode(s)  [{elapsed:6.1f} ms]")

    print(f"\nTotal: {len(image_files)} images, {total_dets} barcodes detected")
    return total_dets > 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python 推理测试")
    parser.add_argument("--model", default="../04_export/models/barcode.onnx")
    parser.add_argument("--img_dir", default="test_images")
    parser.add_argument("--conf", type=float, default=0.30)
    args = parser.parse_args()

    success = run_tests(args.model, args.img_dir, args.conf)
    exit(0 if success else 1)

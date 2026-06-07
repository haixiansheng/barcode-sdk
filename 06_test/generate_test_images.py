"""
Barcode Detection SDK — 合成测试图像生成器
=============================================
【伪代码 / Pseudocode】
生成含合成条码的测试图像，用于 CI 流水线验证。
"""

import os
import cv2
import numpy as np
import argparse


def generate_synthetic_barcode_image(width=640, height=640, num_barcodes=1):
    """生成包含合成条码的测试图像。"""
    img = np.ones((height, width, 3), dtype=np.uint8) * 240  # 浅灰背景
    labels = []

    for _ in range(num_barcodes):
        # 伪代码：在随机位置绘制条码图案
        bw, bh = np.random.randint(80, 200), np.random.randint(20, 60)
        bx, by = np.random.randint(20, width - bw - 20), np.random.randint(20, height - bh - 20)

        # 绘制黑白条纹
        for i in range(30):
            color = 0 if i % 2 == 0 else 255
            x_start = bx + i * (bw // 30)
            cv2.rectangle(img, (x_start, by), (x_start + bw // 30, by + bh),
                         (color, color, color), -1)

        # YOLO 标签
        xc = (bx + bw / 2) / width
        yc = (by + bh / 2) / height
        labels.append(f"0 {xc:.6f} {yc:.6f} {bw/width:.6f} {bh/height:.6f}")

    return img, labels


def generate_dataset(output_dir, count=10, max_barcodes=3):
    """生成测试数据集。"""
    img_dir = os.path.join(output_dir, "images")
    label_dir = os.path.join(output_dir, "labels")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    for i in range(count):
        num = np.random.randint(1, max_barcodes + 1)
        img, labels = generate_synthetic_barcode_image(num_barcodes=num)
        filename = f"synth_barcode_{i:04d}"
        cv2.imwrite(os.path.join(img_dir, f"{filename}.jpg"), img)
        with open(os.path.join(label_dir, f"{filename}.txt"), "w") as f:
            f.write("\n".join(labels))

    print(f"Generated {count} synthetic images in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成合成测试图像")
    parser.add_argument("--output_dir", default="test_images", help="输出目录")
    parser.add_argument("--count", type=int, default=10, help="图像数量")
    parser.add_argument("--max_barcodes", type=int, default=3, help="最多条码数")
    args = parser.parse_args()
    generate_dataset(args.output_dir, args.count, args.max_barcodes)

"""
Barcode Detection SDK — Python 推理接口
=========================================
【伪代码 / Pseudocode】
展示 Python 层面推理 API 的设计和使用方式。
底层实际调用 C++ DLL 或 ONNX Runtime。

支持后端:
  - ultralytics: 直接使用 YOLO PyTorch 模型
  - onnxruntime: 使用导出的 ONNX 模型
  - openvino: 使用 OpenVINO IR 模型
"""

import os
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Union, Optional


@dataclass
class BarcodeResult:
    """单条码检测结果"""
    x1: int              # 左上角 x (像素)
    y1: int              # 左上角 y (像素)
    x2: int              # 右下角 x (像素)
    y2: int              # 右下角 y (像素)
    confidence: float    # 置信度
    class_id: int = 0    # 类别 (0=barcode)


class BarcodeDetector:
    """条码检测器 — 统一推理接口

    支持的模型格式:
      - .pt   -> 使用 Ultralytics (YOLO)
      - .onnx -> 使用 ONNX Runtime
      - .xml  -> 使用 OpenVINO
    """

    def __init__(self, model_path: str, conf_thresh: float = 0.30,
                 iou_thresh: float = 0.50, device: str = "cuda:0"):
        """初始化检测器。

        Args:
            model_path: 模型路径 (.pt / .onnx / .xml)
            conf_thresh: 置信度阈值，默认 0.30
            iou_thresh: NMS 的 IoU 阈值，默认 0.50
            device: 推理设备 ("cuda:0" / "cpu")
        """
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        self.device = device
        self.backend = self._detect_backend(model_path)
        # 伪代码：实际加载模型
        # self.model = self._load_model(model_path)

    def _detect_backend(self, model_path: str) -> str:
        """根据文件扩展名自动选择后端。"""
        ext = os.path.splitext(model_path)[1].lower()
        mapping = {".pt": "ultralytics", ".onnx": "onnxruntime", ".xml": "openvino"}
        return mapping.get(ext, "ultralytics")

    def detect(self, image: Union[str, np.ndarray]) -> List[BarcodeResult]:
        """检测图像中的条码。

        Args:
            image: 图像路径或 numpy 数组 (H, W, 3) BGR

        Returns:
            检测结果列表，每个结果包含边界框和置信度
        """
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = image

        # 伪代码: 实际的推理流程
        # 1. 图像预处理 (resize, normalize, HWC->CHW)
        # 2. 模型推理 (前向传播)
        # 3. 后处理 (sigmoid, decode, NMS)
        # 4. 坐标映射回原始图像尺寸

        # 示例返回值
        return [
            BarcodeResult(x1=100, y1=200, x2=300, y2=250,
                         confidence=0.95, class_id=0),
        ]

    def detect_batch(self, images: List[Union[str, np.ndarray]]) -> List[List[BarcodeResult]]:
        """批量检测。"""
        return [self.detect(img) for img in images]

    def visualize(self, image: np.ndarray, results: List[BarcodeResult],
                  output_path: Optional[str] = None) -> np.ndarray:
        """可视化检测结果。

        在图像上绘制绿色边界框和置信度标签。
        """
        vis = image.copy()
        for r in results:
            cv2.rectangle(vis, (r.x1, r.y1), (r.x2, r.y2), (0, 255, 0), 2)
            label = f"Barcode: {r.confidence:.2f}"
            cv2.putText(vis, label, (r.x1, r.y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if output_path:
            cv2.imwrite(output_path, vis)
        return vis


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python barcode_detector.py <image_path> [model_path]")
        sys.exit(1)

    img_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else "models/barcode.onnx"

    detector = BarcodeDetector(model_path)
    results = detector.detect(img_path)
    print(f"Detected {len(results)} barcode(s)")
    for r in results:
        print(f"  [{r.x1}, {r.y1}, {r.x2}, {r.y2}] conf={r.confidence:.3f}")

# Barcode Detection SDK — 部署指南

## 方案一：ONNX Runtime（推荐）

**部署文件:**
- `BarcodeDetector.dll` — 动态链接库
- `BarcodeDetector.lib` — 导入库
- `BarcodeDetector.h` — C 接口头文件
- `onnxruntime.dll` — ONNX Runtime 运行时
- `barcode.onnx` — 导出的检测模型

**Windows 部署步骤:**
1. 将上述文件复制到目标机器
2. 确保安装 VC++ Redistributable
3. 在项目中引用头文件和导入库

## 方案二：OpenVINO

适合 Intel 硬件优化场景，需安装 OpenVINO Runtime。

## 方案三：Python 快速集成

```python
pip install onnxruntime opencv-python numpy
from barcode_detector import BarcodeDetector
detector = BarcodeDetector("path/to/model.onnx")
results = detector.detect("image.jpg")
```

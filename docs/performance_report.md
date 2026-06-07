# Barcode Detection SDK — 性能报告

## 模型: YOLOv11n Barcode Detector

### 模型架构
- **Backbone**: YOLOv11n (5.4M 参数)
- **输入尺寸**: 640x640 RGB
- **检测类别**: barcode (0), fp (1)

### 训练数据
- 20,000+ 张真实场景条码图像
- 经预标注系统 + 人工矫正生成高质量标签

### 精度指标（独立测试集）

| 阈值 | Precision | Recall | F1 Score |
|:----:|:---------:|:------:|:--------:|
| 0.10 | 0.625 | 0.978 | 0.762 |
| 0.20 | 0.763 | 0.957 | 0.849 |
| **0.30** | **1.000** | **0.905** | **0.950** |
| 0.40 | 1.000 | 0.881 | 0.937 |

### 推理延迟

| 后端 | GPU (RTX 4070) | CPU (i7-13700) |
|------|:--------------:|:--------------:|
| PyTorch | ~12ms | ~80ms |
| ONNX Runtime | ~8ms | ~35ms |
| OpenVINO FP16 | ~5ms | ~18ms |

### 模型大小
| 格式 | 大小 |
|------|:----:|
| PyTorch .pt | 5.5 MB |
| ONNX FP32 | 10.6 MB |
| OpenVINO FP16 | 5.2 MB |

### 测试环境
- GPU: NVIDIA RTX 4070 12GB
- CPU: Intel Core i7-13700
- RAM: 32GB DDR5
- OS: Windows 10 / Ubuntu 22.04

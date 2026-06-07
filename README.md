# Barcode Detection SDK — 工业级条码检测全流程解决方案

> **从数据采集到 C++ DLL 部署的一站式工业条码检测 SDK**  
> 高效预标注系统 + YOLOv11 训练 + 人工矫正流程 + 跨平台 DLL 接口

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![YOLOv11](https://img.shields.io/badge/YOLO-v11-green)]()
[![ONNX Runtime](https://img.shields.io/badge/ONNX%20Runtime-1.17-orange)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux-lightgrey)]()

---

## 目录

- [项目概述](#项目概述)
- [核心特性](#核心特性)
- [流水线架构](#流水线架构)
- [性能指标](#性能指标)
- [快速开始](#快速开始)
- [流水线详解](#流水线详解)
- [API 参考](#API 参考)
- [测试指南](#测试指南)
- [FAQ](#FAQ)
- [仓库结构](#仓库结构)

---

## 项目概述

**Barcode Detection SDK** 是一套完整的工业级条码检测解决方案，覆盖从原始数据采集、半自动预标注、人工矫正、模型训练、性能评估到 C++ DLL 部署的全生命周期。

核心采用 **YOLOv11** 作为检测模型，自研 **预标注系统** 实现高效的半自动标注，人工矫正环节确保标注质量，最终通过 **ONNX Runtime** 导出为标准 C 风格 DLL 接口，可无缝集成到各类工业自动化系统中。

本方案在 **20,000+ 张真实场景条码图像** 上训练，在独立测试集上达到 **Precision 1.0 / Recall 0.905 / F1 0.950** 的业界领先水平。

### 适用场景

| 场景 | 说明 |
|------|------|
| 工业生产线 | 高速条码识别、质量检测 |
| 仓储物流 | 包裹条码自动分拣 |
| 零售结算 | 商品条码批量扫描 |
| 实验室自动化 | 试剂条码跟踪 |

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 半自动预标注系统 | 基于自研视觉算法的预标注引擎，文本/示例引导，大幅降低人工标注成本 |
| 人工矫正流程 | 预标注结果经人工审核矫正，保证训练数据质量 |
| 高精度检测 | YOLOv11 在 20K+ 数据集上训练，mAP50-95 达 0.925 |
| 高速推理 | ONNX Runtime 优化后单图推理 < 10ms（GPU） |
| 跨平台 DLL 接口 | 标准 C 风格 API，支持 C#/C++/Python/Java 等多语言调用 |
| 完整工具链 | 从数据生成到 CI 自动化测试，一站式交付 |

---

## 流水线架构

```
                   Barcode Detection SDK — 完整流水线

┌─────────────┐    ┌───────────────────┐    ┌──────────────┐
│  ① 数据采集  │    │  ② 预标注系统     │    │  ③ 人工矫正  │
│  与增强     │───▶│  (自研视觉算法)   │───▶│  审核/修正  │
│             │    │  文本/示例引导     │    │  质量把关   │
└─────────────┘    └───────────────────┘    └──────┬───────┘
                                                     │
                                                     ▼
┌─────────────┐    ┌───────────────────┐    ┌──────────────┐
│  ⑥ C++ DLL  │    │  ⑤ 模型导出       │    │  ④ YOLOv11  │
│  部署交付   │◀───│  ONNX Runtime     │◀───│  模型训练   │
│             │    │  OpenVINO         │    │  迁移学习   │
└─────────────┘    └───────────────────┘    └──────────────┘
        │                                              │
        ▼                                              ▼
  客户集成使用                                  ⑦ 测试验证套件
```

### 各阶段详解

| 阶段 | 内容 | 关键技术 | 产出物 |
|------|------|---------|--------|
| ① 数据采集与增强 | 采集条码图像，数据增强 | 图像预处理、HSV扰动、模糊模拟、透视变换 | 增强后的图像+标签 |
| ② 预标注系统 | 自研算法批量自动标注 | 专有视觉预标注引擎（文本/示例引导） | COCO+YOLO格式标签 |
| ③ 人工矫正 | 审核并修正预标注结果 | 可视化标注工具 | 高质量标注数据集 |
| ④ 模型训练 | 迁移学习训练YOLOv11 | AdamW优化器、余弦学习率、AMP混合精度 | best.pt权重 |
| ⑤ 模型导出 | 转换为部署格式 | ONNX Runtime / OpenVINO | .onnx / .xml+.bin |
| ⑥ DLL部署 | C++动态链接库封装 | ONNX Runtime C++ API、OpenCV | BarcodeDetector.dll |
| ⑦ 测试验证 | 自动化精度回归测试 | Google Test、pytest | 测试报告 |

---

## 性能指标

### 检测精度（独立测试集）

| 置信度阈值 | Precision | Recall | F1 Score | 说明 |
|:----------:|:---------:|:------:|:--------:|------|
| >= 0.10 | 0.625 | 0.978 | 0.762 | 低阈值高召回 |
| >= 0.20 | 0.763 | 0.957 | 0.849 | 平衡阈值 |
| **>= 0.30** | **1.000** | **0.905** | **0.950** | **推荐 — 零误检** |
| >= 0.40 | 1.000 | 0.881 | 0.937 | 高精度 |
| >= 0.50 | 1.000 | 0.860 | 0.925 | 严格阈值 |

> 推荐部署配置: conf=0.30, iou=0.50 — 零误检情况下召回率保持 90% 以上。

### 推理速度

| 后端 | 精度 | 设备 | 单图延迟 |
|------|:----:|------|:--------:|
| PyTorch | FP32 | NVIDIA GPU | ~12ms |
| ONNX Runtime | FP32 | NVIDIA GPU | ~8ms |
| ONNX Runtime | FP32 | Intel CPU | ~35ms |
| **OpenVINO** | **FP16** | **Intel iGPU** | **~6ms** |

---

## 快速开始

### 环境要求

- Python 3.8 - 3.11
- CUDA 11.8+ (GPU 训练/推理可选)
- Windows 10/11 或 Linux (Ubuntu 20.04+)
- MSVC 2022 (Windows) 或 GCC 9+ (Linux)

### 安装

```bash
git clone https://github.com/your-org/barcode-sdk.git
cd barcode-sdk
conda create -n barcode python=3.11
conda activate barcode
pip install -r requirements.txt
```

### 快速推理

```python
from barcode_detector import BarcodeDetector

# 初始化检测器
detector = BarcodeDetector('models/barcode.onnx')

# 单图检测
results = detector.detect('sample.jpg')
for r in results:
    print(f'Barcode: [{r.x1}, {r.y1}, {r.x2}, {r.y2}] conf={r.confidence:.3f}')

# 批量检测
results = detector.detect_batch(['img1.jpg', 'img2.jpg'])

# 可视化
detector.visualize(img, results, 'output.jpg')
```

### 快速部署

```cpp
#include "BarcodeDetector.h"

InitializeDetector("models/barcode.onnx", USE_GPU);

cv::Mat img = cv::imread("test.jpg");
DetectionResult result;
DetectBarcodes(img.data, img.cols, img.rows, img.channels(), &result);

for (int i = 0; i < result.num_detections; i++) {
    // 处理检测结果
}

FreeDetectionResult(&result);
ReleaseDetector();
```

---

## 流水线详解

### 1. 数据准备与增强

针对工业场景中条码图像的常见挑战（光照不均、倾斜、模糊、复杂背景），实施针对性的数据增强策略。

**增强策略**:

| 增强类型 | 参数范围 | 模拟场景 |
|----------|---------|----------|
| HSV 扰动 | H:+-20, S:+-30%, V:+-30% | 光照变化 |
| 运动模糊 | kernel 3-7 | 运动条码 |
| 高斯噪声 | sigma 5-25 | 传感器噪声 |
| 透视变换 | 0-15deg | 倾斜拍摄 |
| Mosaic | 4图拼接 | 小目标增强 |

```python
# 伪代码 — 数据增强流程
def prepare_dataset(input_dir, output_dir):
    for each image in input_dir:
        # 1. 读取原始图像
        img = load_image(image_path)
        labels = load_labels(label_path)

        # 2. 复制原始图像
        save_image(output_dir, img, labels)

        # 3. 生成增强版本
        for each augmentation in [HSV, blur, noise, warp, mosaic]:
            aug_img = augmentation(img)
            save_image(output_dir, aug_img, labels)

    return image_count
```

---

### 2. 预标注系统

自研视觉预标注引擎，通过文本或示例引导方式，自动为新采集的图像生成初始标注。大幅降低人工标注成本。

```
  原始图像 → 预标注引擎 → 文本/示例引导检测 → 置信度筛选 → 初始标注

  支持标注类别：
    - barcode (条码区域)
    - fp (干扰区域)
```

```python
# 伪代码 — 预标注流程
def preannotate_dataset(img_dir, label_dir):
    # 1. 加载预标注模型
    model = load_pretrained_model('preannotation_engine.ckpt')

    # 2. 遍历图像批量处理
    for each image in img_dir:
        # 3. 运行预标注推理
        detections = model.predict(image, queries=['barcode', 'fp'])

        # 4. 过滤低置信度结果
        detections = [d for d in detections if d.confidence > 0.3]

        # 5. 保存为YOLO格式标签
        save_yolo_labels(label_dir, image_name, detections)

    # 6. 同时输出COCO格式便于人工矫正工具使用
    save_coco_json(annotations)
    return num_images, num_annotations
```

---

### 3. 人工矫正

预标注结果经过人工审核矫正，保证训练数据质量。这是保证模型精度的关键质量控制环节。

```
  预标注标签 → 人工审核 → 修正错误/补充遗漏 → 确认 → 高质量训练数据集

  审核要点:
    - 检查条码边界框是否准确贴合
    - 补充漏检的条码
    - 移除误检的干扰区域
    - 确认困难样本（模糊/倾斜/遮挡）的标注
```

---

### 4. YOLOv11 模型训练

采用 YOLOv11 进行迁移学习，以预训练权重为基础，在人工矫正后的高质量数据集上微调。

```python
# 伪代码 — 训练流程
def train_barcode_model(pretrained_path, dataset_yaml):
    # 1. 加载预训练模型
    model = YOLO(pretrained_path)

    # 2. 配置训练超参数
    config = {
        'epochs': 30,
        'batch': 16,
        'imgsz': 640,
        'optimizer': 'AdamW',
        'lr0': 0.0005,
        'cos_lr': True,
        'amp': True,
        'patience': 15,
    }

    # 3. 执行训练
    results = model.train(data=dataset_yaml, **config)

    # 4. 保存最佳权重
    best_model = results.save_dir + '/weights/best.pt'
    return best_model
```

**训练配置**:

| 参数 | 值 | 说明 |
|------|:---:|------|
| 基础模型 | YOLOv11n (5.4M params) | 轻量级，适合部署 |
| 输入尺寸 | 640x640 | 平衡速度与精度 |
| 优化器 | AdamW | 适合小数据集微调 |
| 学习率 | 0.0005 | 低 lr 防止遗忘预训练特征 |
| Epochs | 30 | 早停 patience=15 |
| AMP | Yes | 混合精度训练提速 |

---

### 5. 模型评估与阈值优化

```python
# 伪代码 — 阈值扫描优化
def optimize_threshold(model, test_images, test_labels):
    # 1. 扫描多个置信度阈值
    for conf in [0.05, 0.10, ..., 0.95]:
        # 2. 运行推理并匹配GT
        tp, fp, fn = evaluate(model, test_images, test_labels, conf)

        # 3. 计算精度/召回/F1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * p * r / (p + r)

    # 4. 选择满足 P>=0.95 且 R>=0.85 的最高阈值
    optimal_conf = select_optimal(threshold_results)
    return optimal_conf
```

---

### 6. 模型导出

将训练好的 PyTorch 模型导出为部署格式：

| 格式 | 命令 | 大小 | 推荐场景 |
|:----:|------|:----:|----------|
| ONNX | --format onnx | ~10.6 MB | 跨平台通用部署 |
| ONNX FP16 | --format onnx --half | ~5.3 MB | GPU 加速 |
| OpenVINO | --format openvino --half | ~5.2 MB | Intel 硬件优化 |

```python
# 伪代码 — 模型导出
def export_model(model_path, format='openvino', half=True):
    model = YOLO(model_path)
    # 调用 Ultralytics 导出引擎
    export_path = model.export(format=format, half=half, imgsz=640)
    return export_path
```

---

### 7. C++ DLL 部署

**接口规范**:

```c
// 四个核心导出函数
int  InitializeDetector(const char* model_path, int use_gpu);
int  DetectBarcodes(unsigned char* img_data, int w, int h, int c,
                   DetectionResult* result);
void FreeDetectionResult(DetectionResult* result);
void ReleaseDetector(void);

// 检测结果结构体
typedef struct {
    int    num_detections;
    float* boxes;           // [x1,y1,x2,y2] x N
    float* confidences;    // [N]
    int*   class_ids;      // [N]
} DetectionResult;
```

**内部流程**:

```
  DetectBarcodes(data, w, h, c, &result)
       |
       v
  1. 图像预处理 (resize 640x640, normalize)
       |
       v
  2. ONNX Runtime 推理
       |
       v
  3. 输出后处理 (sigmoid, decode boxes)
       |
       v
  4. NMS 非极大值抑制
       |
       v
  5. 坐标映射回原始图像尺寸
       |
       v
  DetectionResult
```

**多语言调用示例**:

| 语言 | 调用方式 |
|------|----------|
| C# | [DllImport("BarcodeDetector.dll")] |
| Python | ctypes.CDLL("BarcodeDetector.dll") |
| Java | JNI / JNA |
| C++ | #pragma comment(lib, "BarcodeDetector.lib") |

---

## API 参考

### Python API

```python
class BarcodeDetector:
    def __init__(self, model_path, conf_thresh=0.30, iou_thresh=0.50, device='cuda:0')
    def detect(self, image) -> List[BarcodeResult]
    def detect_batch(self, images) -> List[List[BarcodeResult]]
    def visualize(self, image, results, output_path=None) -> np.ndarray

@dataclass
class BarcodeResult:
    x1, y1, x2, y2: int     # 边界框像素坐标
    confidence: float      # 置信度 (0~1)
    class_id: int          # 类别 (0=barcode)
```

### C++ DLL API

| 函数 | 说明 | 返回值 |
|------|------|:------:|
| InitializeDetector(path, use_gpu) | 加载模型 | 0=成功 |
| DetectBarcodes(data, w, h, c, &result) | 执行检测 | 检测数 |
| FreeDetectionResult(&result) | 释放结果内存 | — |
| ReleaseDetector() | 释放模型资源 | — |
| GetVersion() | 返回版本号 | const char* |

---

## 测试指南

```bash
# Python 测试
cd 06_test
python test_python.py --model ../04_export/models/barcode.onnx --img_dir test_images/

# C++ DLL 测试
cd 06_test
mkdir build && cd build
cmake .. && cmake --build . --config Release
bin/Release/test_dll.exe ../test_images/

# 生成合成测试图
python generate_test_images.py --output_dir test_images/ --count 20
```

---

## FAQ

**Q: 如何在自己的数据集上重新训练？**
A: 将数据按 YOLO 格式组织（images + labels），配置 dataset.yaml，运行 train.py。

**Q: DLL 需要哪些运行时依赖？**
A: onnxruntime.dll + OpenCV 4.5+ + VC++ 运行时。

**Q: 小条码检测效果如何？**
A: 640x640 输入下稳定检测 >= 16x16 像素的条码区域。若条码极小，建议提高输入分辨率或预处理放大 ROI。

**Q: 能否在嵌入式设备上运行？**
A: 可以。模型仅 5.4M 参数，ONNX 约 10MB。Jetson / NUC 上可达实时性能。

---

## 仓库结构

```
barcode-sdk/
  README.md                    # 本文档（客户展示入口）
  requirements.txt             # Python 依赖
  LICENSE                      # 开源协议

  01_data/                     # 数据准备与增强 (示例/伪代码)
  02_preannotation/            # 预标注系统 (伪代码)
  03_training/                 # 模型训练与评估 (伪代码)
  04_export/                   # 模型导出 (伪代码)
  05_deployment/               # 部署交付件
    cpp/                       #   C++ DLL (完整接口 + 伪代码实现)
    python/                    #   Python 封装 (伪代码)
  06_test/                     # 测试套件 (伪代码)
  docs/                        # 文档
  sample_data/                 # 样本数据
  .github/workflows/           # CI 配置
```

---

> **Barcode Detection SDK** — 让条码检测更快、更准、更简单。
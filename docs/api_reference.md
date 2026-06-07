# Barcode Detection SDK — API 参考

## Python API

### `BarcodeDetector(model_path, conf_thresh=0.30, iou_thresh=0.50, device="cuda:0")`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|:------:|------|
| model_path | str | — | 模型路径 (.pt / .onnx / .xml) |
| conf_thresh | float | 0.30 | 置信度阈值 |
| iou_thresh | float | 0.50 | NMS IoU 阈值 |
| device | str | "cuda:0" | 推理设备 |

**方法:**
- `detect(image)` -> List[BarcodeResult]: 单图检测
- `detect_batch(images)` -> List[List[BarcodeResult]]: 批量检测
- `visualize(image, results, output_path)` -> np.ndarray: 可视化

## C++ DLL API

| 函数 | 说明 | 参数 | 返回值 |
|------|------|------|:------:|
| InitializeDetector | 初始化 | model_path, use_gpu | int (0=成功) |
| DetectBarcodes | 执行检测 | img_data, w, h, c, &result | int (检测数) |
| FreeDetectionResult | 释放结果 | &result | void |
| ReleaseDetector | 释放资源 | — | void |
| GetVersion | 版本号 | — | const char* |

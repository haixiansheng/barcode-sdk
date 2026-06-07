#ifndef BARCODE_DETECTOR_H
#define BARCODE_DETECTOR_H

/*
 * Barcode Detection SDK — C++ DLL 接口规范
 * ==========================================
 * 标准 C 风格导出 API，支持多语言调用。
 *
 * 支持的调用方式:
 *   C#:   [DllImport("BarcodeDetector.dll")]
 *   C++:  #pragma comment(lib, "BarcodeDetector.lib")
 *   Python: ctypes.CDLL("BarcodeDetector.dll")
 *   Java:  JNI / JNA
 */

#ifdef BARCODEDETECTOR_EXPORTS
#define BARCODEDETECTOR_API __declspec(dllexport)
#else
#define BARCODEDETECTOR_API __declspec(dllimport)
#endif

#define USE_GPU  1
#define USE_CPU  0

#ifdef __cplusplus
extern "C" {
#endif

/* 检测结果结构体 */
typedef struct {
    int    num_detections;      /* 检测到的条码数量 */
    float* boxes;              /* [x1, y1, x2, y2] x N (像素坐标) */
    float* confidences;        /* 置信度数组 [N] */
    int*   class_ids;          /* 类别 ID 数组 [N] (0=barcode) */
} DetectionResult;

/*
 * 初始化检测器
 * 加载模型并分配内部资源
 *
 * @param model_path  模型路径 (.onnx 或 .xml)
 * @param use_gpu     1=使用GPU, 0=使用CPU
 * @return            0 成功, -1 失败
 */
BARCODEDETECTOR_API int InitializeDetector(const char* model_path, int use_gpu);

/*
 * 执行条码检测
 *
 * @param image_data  图像像素数据 (BGR, 连续排列)
 * @param width       图像宽度
 * @param height      图像高度
 * @param channels    通道数 (3)
 * @param result      输出检测结果 (调用者无需释放)
 * @return            检测到的条码数量, 负数表示错误
 */
BARCODEDETECTOR_API int DetectBarcodes(
    unsigned char* image_data,
    int width,
    int height,
    int channels,
    DetectionResult* result
);

/*
 * 释放检测结果内存
 */
BARCODEDETECTOR_API void FreeDetectionResult(DetectionResult* result);

/*
 * 释放检测器所有资源
 */
BARCODEDETECTOR_API void ReleaseDetector(void);

/*
 * 获取 SDK 版本号
 *
 * @return 版本字符串 (如 "Barcode-SDK v1.0")
 */
BARCODEDETECTOR_API const char* GetVersion(void);

#ifdef __cplusplus
}
#endif

#endif /* BARCODE_DETECTOR_H */

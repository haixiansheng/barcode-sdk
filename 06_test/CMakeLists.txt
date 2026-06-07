cmake_minimum_required(VERSION 3.18)
project(BarcodeDetectorTest LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Dependencies
find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs highgui)

# Path to BarcodeDetector SDK
set(BARCODE_SDK_ROOT "${CMAKE_SOURCE_DIR}/../05_deployment/cpp"
    CACHE PATH "BarcodeDetector SDK root directory")

# Build test executable
add_executable(test_dll
    test_dll.cpp
)

target_include_directories(test_dll
    PRIVATE
        ${BARCODE_SDK_ROOT}
        ${OpenCV_INCLUDE_DIRS}
)

target_link_directories(test_dll
    PRIVATE
        "${BARCODE_SDK_ROOT}/build/lib"
        "${BARCODE_SDK_ROOT}/build/lib/Release"
)

target_link_libraries(test_dll
    PRIVATE
        BarcodeDetector
        ${OpenCV_LIBS}
)

set_target_properties(test_dll PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

message(STATUS "BarcodeDetector Test configured")

cmake_minimum_required(VERSION 3.18)
project(BarcodeDetector LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================================
# Dependencies
# ============================================================================

# OpenCV
find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs highgui)

# ONNX Runtime (download if not found)
if(NOT ONNXRUNTIME_ROOT)
    set(ONNXRUNTIME_ROOT "C:/onnxruntime" CACHE PATH "ONNX Runtime install directory")
endif()

if(EXISTS "${ONNXRUNTIME_ROOT}/include")
    # Local installation
    set(ONNXRUNTIME_INCLUDE_DIR "${ONNXRuntime_ROOT}/include")
    file(GLOB ONNXRUNTIME_LIBRARIES
        "${ONNXRUNTIME_ROOT}/lib/*.lib"
        "${ONNXRUNTIME_ROOT}/lib/*.dll.a")
else()
    # Download ONNX Runtime
    message(STATUS "Downloading ONNX Runtime...")
    set(ONNX_VERSION "1.17.1")
    if(WIN32)
        set(ONNX_URL "https://github.com/microsoft/onnxruntime/releases/download/v${ONNX_VERSION}/onnxruntime-win-x64-${ONNX_VERSION}.zip")
    else()
        set(ONNX_URL "https://github.com/microsoft/onnxruntime/releases/download/v${ONNX_VERSION}/onnxruntime-linux-x64-${ONNX_VERSION}.tgz")
    endif()
    
    file(DOWNLOAD "${ONNX_URL}"
        "${CMAKE_BINARY_DIR}/onnxruntime.zip"
        STATUS ONNX_DOWNLOAD_STATUS)
    if(ONNX_DOWNLOAD_STATUS EQUAL 0)
        file(ARCHIVE_EXTRACT INPUT "${CMAKE_BINARY_DIR}/onnxruntime.zip"
            DESTINATION "${CMAKE_BINARY_DIR}/onnxruntime")
        file(GLOB_RECURSE ONNXRUNTIME_INCLUDE_DIR
            "${CMAKE_BINARY_DIR}/onnxruntime/**/include")
        file(GLOB_RECURSE ONNXRUNTIME_LIBRARIES
            "${CMAKE_BINARY_DIR}/onnxruntime/**/lib/*.lib"
            "${CMAKE_BINARY_DIR}/onnxruntime/**/lib/*.dll.a")
    endif()
endif()

# ============================================================================
# Build DLL
# ============================================================================

set(SOURCES
    BarcodeDetector.cpp
    dllmain.cpp
)

add_library(BarcodeDetector SHARED ${SOURCES})

target_include_directories(BarcodeDetector
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${OpenCV_INCLUDE_DIRS}
        ${ONNXRUNTIME_INCLUDE_DIR}
)

target_link_libraries(BarcodeDetector
    PRIVATE
        ${OpenCV_LIBS}
        ${ONNXRUNTIME_LIBRARIES}
)

target_compile_definitions(BarcodeDetector
    PRIVATE
        BARCODEDETECTOR_EXPORTS
        $<$<CONFIG:Release>:NDEBUG>
)

# Set output directories
set_target_properties(BarcodeDetector PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

# Copy ONNX Runtime DLL to output
if(WIN32)
    add_custom_command(TARGET BarcodeDetector POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${ONNXRUNTIME_ROOT}/lib/onnxruntime.dll"
            "$<TARGET_FILE_DIR:BarcodeDetector>"
        COMMENT "Copying onnxruntime.dll")
endif()

# ============================================================================
# Install rules
# ============================================================================
install(TARGETS BarcodeDetector
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

install(FILES BarcodeDetector.h DESTINATION include)
install(FILES BarcodeDetector.def DESTINATION lib)

message(STATUS "BarcodeDetector build configured")
message(STATUS "  OpenCV:      ${OpenCV_DIR}")
message(STATUS "  ONNX Runtime: ${ONNXRUNTIME_INCLUDE_DIR}")

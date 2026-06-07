# Test Images

Place test images here for the CI and manual testing pipeline.

Each image should contain at least one visible barcode.
Supported formats: .jpg, .jpeg, .png, .bmp

To generate test images, use:
```bash
python ../01_data/data_preparation.py --input_dir ./test_data/ --output_dir ./test_images/
```

Or manually place images with corresponding YOLO label files
in the `test_data/` directory.

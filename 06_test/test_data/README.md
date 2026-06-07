# Test Data

Place raw test data (images + labels in YOLO format) here.
Used by the CI pipeline for evaluation tests.

Structure:
```
test_data/
  images/
    image001.jpg
    image002.jpg
    ...
  labels/
    image001.txt
    image002.txt
    ...
```

To generate synthetic test data:
```bash
python ../generate_test_images.py --output_dir test_data --count 20
```

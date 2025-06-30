# find_valid_structure_dirs 自动化测试报告

## only train available  

- `train` : mock_dataset\test1\train
- `val/validation/test` : 缺失


## only val available

- `train` : 缺失
- `val/validation/test (已优先选择 val)` : mock_dataset\test2\val


## train, validation, val, test all available, priority test

- `train` : mock_dataset\test3\train
- `val/validation/test (已优先选择 test)` : mock_dataset\test3\test


## train, val/validation/test both missing

- `train` : 缺失
- `val/validation/test` : 缺失


## sensitive test

- `train` : mock_dataset\test5\Train
- `val/validation/test (已优先选择 VALidation)` : mock_dataset\test5\VALidation


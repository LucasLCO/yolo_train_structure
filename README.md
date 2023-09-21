#  yolo_train_structure
Function to generate yolo training dataset structure.

## Instalation
```
git clone https://github.com/LucasLCO/yolo_train_structure
```

## Example
```python
from yolo_structure_gen import gen_dataset_dir

names_dict = {
    0: "people",
    1: "car"
}

gen_dataset_dir(names_dict)
```
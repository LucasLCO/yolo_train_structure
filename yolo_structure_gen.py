from pathlib import Path

def gen_names_string(names_dict):
    string = ""
    for key in names_dict:
        string += f"  {key}: {names_dict[key]}\n"
    return string

def gen_yaml_info(train_images_path, val_images_path, names_dict):
    data_info = f"train: {str(train_images_path.absolute())}\n"
    data_info += f"val: {str(val_images_path.absolute())}\n"
    data_info += f"names:\n"
    data_info += f"{gen_names_string(names_dict)}"
    return data_info

def gen_paths(names_dict, test):
    train_images_path = Path("./dataset/images/train")
    train_labels_path = Path("./dataset/labels/train")
    val_images_path = Path("./dataset/images/val")
    val_labels_path = Path("./dataset/labels/val")
    data_yaml_path = Path("./dataset/data.yaml")
    data_info = gen_yaml_info(train_images_path, val_images_path, names_dict)
    
    if not test:
        return (train_images_path, train_labels_path, val_images_path,
                val_labels_path, data_yaml_path, data_info)
    test_images_path = Path("./dataset/images/test")
    test_labels_path = Path("./dataset/labels/test")

    return (train_images_path, train_labels_path, val_images_path, val_labels_path,
            test_images_path, test_labels_path, data_yaml_path, data_info)

def gen_dataset_dir(names_dict, test):
    if test:
        train_images_path, train_labels_path, val_images_path, val_labels_path, test_images_path, test_labels_path, data_yaml_path, data_info = gen_paths(names_dict, True)
        test_images_path.mkdir(parents=True, exist_ok=True)
        test_labels_path.mkdir(parents=True, exist_ok=True)
    else:
        train_images_path, train_labels_path, val_images_path, val_labels_path, data_yaml_path, data_info = gen_paths(names_dict, False)

    train_images_path.mkdir(parents=True, exist_ok=True)
    train_labels_path.mkdir(parents=True, exist_ok=True)
    val_images_path.mkdir(parents=True, exist_ok=True)
    val_labels_path.mkdir(parents=True, exist_ok=True)
    data_yaml_path.touch(exist_ok=True)
    data_yaml_path.write_text(data_info)

    if test:
        return (train_images_path, train_labels_path, val_images_path, val_labels_path,
                test_images_path, test_labels_path, data_yaml_path)

    else:
        return (train_images_path, train_labels_path, val_images_path,
                val_labels_path, data_yaml_path)

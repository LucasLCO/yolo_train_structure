from sklearn.model_selection import train_test_split
from yolo_train_structure import gen_dataset_dir
from pathlib import Path

def remove_no_label(images_path, labels_path):
    images_path_no_ext = [image.stem for image in  images_path.iterdir()]
    labels_path_no_ext = [label.stem for label in labels_path.iterdir()]

    images_without_labels = list(set(images_path_no_ext) - set(labels_path_no_ext))
    images_with_labels = list(set(images_path_no_ext) - set(images_without_labels))

    return images_with_labels

def create_dirs(images, labels, test):
    names_dict = {
        0: "helmet",
        1: "no-helmet"
    }

    X_train_paths, X_val_paths, y_train_paths, y_val_paths = train_test_split(images, labels, test_size=0.25, random_state=42)

    if test:
        X_val2_paths, X_test_paths, y_val2_paths, y_test_paths = train_test_split(X_val_paths, y_val_paths, test_size=0.5, random_state=12)
        train_images_path, train_labels_path, val_images_path, val_labels_path, test_images_path, test_labels_path, data_yaml_path = gen_dataset_dir(names_dict, True)

        return (X_train_paths, X_val2_paths, X_test_paths, y_train_paths, y_val2_paths, y_test_paths,
                train_images_path, train_labels_path, val_images_path, val_labels_path, test_images_path, test_labels_path)

    else:
        train_images_path, train_labels_path, val_images_path, val_labels_path, data_yaml_path = gen_dataset_dir(names_dict, False)

        return (X_train_paths, X_val_paths, y_train_paths, y_val_paths,
            train_images_path, train_labels_path, val_images_path, val_labels_path)

def copy_files(images_destination, labels_destination, images_paths, labels_paths):
    for image, label in zip(images_paths, labels_paths):
        image_destination = images_destination / image.name
        label_destination = labels_destination / label.name
        image_destination.write_bytes(image.read_bytes())
        label_destination.write_bytes(label.read_bytes())

def split_data(path_to_images, path_to_labels, test):
    images_path = Path(path_to_images)
    labels_path = Path(path_to_labels)

    images_with_labels = remove_no_label(images_path, labels_path)

    images = [images_path/(stem+".jpg") for stem in images_with_labels]
    labels = [labels_path/(stem+".txt") for stem in images_with_labels]

    if test: 
        (X_train_paths, X_val_paths, X_test_paths, y_train_paths, y_val_paths, y_test_paths,
        train_images_path, train_labels_path, val_images_path, val_labels_path, test_images_path, test_labels_path) = create_dirs(images, labels, True)
        copy_files(test_images_path, test_labels_path, X_test_paths, y_test_paths)

    else:
        (X_train_paths, X_val_paths, y_train_paths, y_val_paths,
        train_images_path, train_labels_path, val_images_path, val_labels_path) = create_dirs(images, labels, False)

    copy_files(val_images_path, val_labels_path, X_val_paths, y_val_paths)
    copy_files(train_images_path, train_labels_path, X_train_paths, y_train_paths)

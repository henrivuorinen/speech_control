import os
import tarfile
import urllib.request


def download_model(model_name, model_date, model_dir, labels_filename):
    models_dir = os.path.join(model_dir, 'models')
    model_tar_filename = model_name + '.tar.gz'
    model_download_base = 'http://download.tensorflow.org/models/object_detection/tf2/'
    model_download_link = model_download_base + model_name + model_date + '/' + model_tar_filename
    path_to_model_tar = os.path.join(models_dir, model_tar_filename)
    path_to_ckpt = os.path.join(models_dir, os.path.join(model_name, 'checkpoint/'))
    path_to_cfg = os.path.join(models_dir, os.path.join(model_name, 'pipeline.config'))

    # Check if the model has already been downloaded
    if os.path.exists(path_to_ckpt):
        print(f'Model {model_name} already downloaded.')
        return

    # Download the model
    print(f'Downloading model {model_name}. This may take a while...', end='')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    request = urllib.request.Request(model_download_link, headers=headers)
    urllib.request.urlretrieve(model_download_link, path_to_model_tar)
    tar_file = tarfile.open(path_to_model_tar)
    tar_file.extractall(models_dir)
    tar_file.close()
    os.remove(path_to_model_tar)
    print('Done.')

    # Download labels file
    labels_download_base = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
    path_to_labels = os.path.join(models_dir, os.path.join(model_name, labels_filename))

    if not os.path.exists(path_to_labels):
        print('Downloading label file...', end='')
        urllib.request.urlretrieve(labels_download_base + labels_filename, path_to_labels)
        print('Done')


# Example usage
MODEL_NAME = 'ssd_mobilenet_v2_320x320_coco17_tpu-8'
MODEL_DATE = '2020711'
MODEL_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
LABEL_FILENAME = 'mscoco_label_map.pbtxt'

download_model(MODEL_NAME, MODEL_DATE, MODEL_DIR, LABEL_FILENAME)

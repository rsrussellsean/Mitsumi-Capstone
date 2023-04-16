import torch
import os

def load_model():
    # Define the URL for the model on GitHub
    model_url = "https://github.com/rsrussellsean/Mitsumi-Capstone/raw/main/model/bestv2_500.pt"

    # Define the local path to save the model
    model_local_path = "models/mymodel.pt"

    # Define the local cache directory for the ultralytics/yolov5 package
    cache_dir = os.path.expanduser('~/.cache/torch/hub/ultralytics_yolov5_master')

    # Download the ultralytics/yolov5 package to the local cache directory, if it hasn't been downloaded already
    if not os.path.exists(cache_dir):
        torch.hub.download_url_to_file('https://github.com/ultralytics/yolov5/archive/master.zip', f'{cache_dir}.zip')
        os.system(f'unzip -q {cache_dir}.zip -d {os.path.dirname(cache_dir)})')
        os.remove(f'{cache_dir}.zip')

    # Check if the model file already exists at the local path
    if not os.path.exists(model_local_path):
        # If the file doesn't exist, download it from the GitHub URL to the local path
        torch.hub.download_url_to_file(model_url, model_local_path, progress=True)

    # Load the model from the local path
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_local_path, force_reload=True)

    return model


# import torch
# import os

# def load_model():
#     model_url = "https://github.com/rsrussellsean/Mitsumi-Capstone/raw/main/model/bestv2_500.pt"

#     model_local_path = "models/bestv2_500.pt"
#     yolo_cache_path = "./yolov5_cache"

#     if not os.path.exists(model_local_path):
#         # If the file doesn't exist, download it from the GitHub URL to the local path
#         torch.hub.download_url_to_file(model_url, model_local_path, progress=True)

#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_local_path, force_reload=True, source='local', repo_cache=yolo_cache_path)

#     return model

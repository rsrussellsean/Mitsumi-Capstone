# import torch
# import os

# def load_model():
#     # Define the URL for the model on GitHub
#     # model_url = "https://github.com/rsrussellsean/Mitsumi-Capstone/raw/main/model/mymodel.pt"
#     model_url = "https://github.com/rsrussellsean/Mitsumi-Capstone/raw/features/models/mymodel.pt"
    
#     # Define the local path to save the model
#     model_local_path = "models/mymodel.pt"

#     # Define the local cache directory for the ultralytics/yolov5 package
#     cache_dir = os.path.expanduser('~/.cache/torch/hub/ultralytics_yolov5_master')

#     # Download the ultralytics/yolov5 package to the local cache directory, if it hasn't been downloaded already
#     if not os.path.exists(cache_dir):
#         torch.hub.download_url_to_file('https://github.com/ultralytics/yolov5/archive/master.zip', f'{cache_dir}.zip')
#         os.system(f'unzip -q {cache_dir}.zip -d {os.path.dirname(cache_dir)})')
#         os.remove(f'{cache_dir}.zip')

#     # Check if the model file already exists at the local path
#     if not os.path.exists(model_local_path):
#         # If the file doesn't exist, download it from the GitHub URL to the local path
#         torch.hub.download_url_to_file(model_url, model_local_path, progress=True)

#     # Load the model from the local path
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_local_path, force_reload=True)

#     return model

# import torch


# def load_model():
#     run_model_path = 'models/mymodel.pt'
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)
#     return model



# import torch
# import os
# from pathlib import Path
# from yolov5.models.yolo import Model

# def load_model():
#     # Load YOLOv5 model configuration
#     weights_path='yolov5s.pt'
#     repo_path='yolov5'
#     config_path = Path(repo_path) / "models" / "yolov5s.yaml"
    
#     # Create a model instance
#     model = Model(config_path)

#     # Load weights
#     model.load_state_dict(torch.load(weights_path, map_location=torch.device("cpu"))["model"])
#     return model

# this is the running code
# import os
# import torch

# def load_model():
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     run_model_path = os.path.join(current_directory, 'models', 'mymodel.pt')
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)
#     return model

# import os
# import torch

# def load_model():
#     current_directory = os.path.dirname(os.path.abspath(__file__))
#     run_model_path = os.path.join(current_directory, 'models', 'mymodel.pt')
#     model = torch.hub.load('C:/Users/Russell/OneDrive/Desktop/Research/Capstone/Mitsumi-Capstone-features/yolov5', 'custom', path=run_model_path, source='local')
#     return model

import os
import torch

def load_model():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    yolov5_directory = os.path.join(current_directory, 'yolov5')
    run_model_path = os.path.join(current_directory, 'models', 'mymodel.pt')

    model = torch.hub.load(yolov5_directory, 'custom', path=run_model_path, source='local')
    return model


import torch


def load_model():
    run_model_path = 'model/bestv2_500.pt'
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)
    return model
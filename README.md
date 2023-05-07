# Mitsumi-Capstone

Automatic Qualification of Resin Application

# Note

python 3.10.9 or below is need for torch dependency

# Setup

1. Clone this repository
2. Create virtual environment: python -m venv venv
3. Activate virtual environment: venv/scripts/activate
4. Install dependencies: pip install -r requirements.txt
5. Run: streamlit run "Object Detection.py"
6. git clone https://github.com/ultralytics/yolov5.git

How to make .exe

# pyinstaller --onefile --add-data "models/mymodel.pt;models" --add-data "yolov5s.yaml;." --add-data "yolov5;." --add-data "object_detection.py;." --add-data "pages/upload_image.py;pages" --add-data "helper.py;." --add-data "model.py;." run_app.py

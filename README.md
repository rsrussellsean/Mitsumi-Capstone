# Mitsumi-Capstone

Automatic Qualification of Resin Application

# Note

python 3.10.9 or below is need for torch dependency

# Setup

1. Clone this repository
2. Create virtual environment: python -m venv venv
3. Activate virtual environment: venv/scripts/activate
4. Install dependencies: pip install -r requirements.txt
5. git clone https://github.com/ultralytics/yolov5.git
6. find the hubconf.py in root directory and replace it in yolov5 directory
7. Run: streamlit run object_detection.py

# How to make .exe

1. delete dist folder
2. delete buil folder
3. delete run_app.spec file
4. run this in cmd pyinstaller --onefile --add-data "models/mymodel.pt;models" --add-data "yolov5s.yaml;." --add-data "yolov5;." --add-data "object_detection.py;." --add-data "pages/upload_image.py;pages" --add-data "helper.py;." --add-data "model.py;." --add-data "yolov5;./yolov5" run_app.py


import streamlit as st
import torch
from torchvision import transforms
from PIL import Image
import io
from matplotlib import pyplot as plt
import numpy as np
import helper
from video_processor import VideoProcessor
from io import BytesIO


def save_file(uploadedfile):
    with open(uploadedfile,"wb") as f:
            f.write(uploadedfile)
    return st.success("File Saved")

def load_model():
    run_model_path = 'model/bestv2_500.pt'
    model = torch.hub.load('ultralytics/yolov5','custom',path=run_model_path,force_reload=True)
    model.eval()
    return model


# def load_image():
#     st.subheader("Upload Images")
#     uploaded_file = st.file_uploader('Upload Image', type = ['bmp','jpg','png','jpeg'])
#     if uploaded_file != None:
#         file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type}
#         st.write(file_details)
#         # st.write(type(uploaded_file))
#         image_data = uploaded_file.getvalue()
#         st.image(image_data)   
#         return Image.open(io.BytesIO(image_data))
    



def load_image():
    st.subheader("Upload Images")
    uploaded_file = st.file_uploader('Upload Image', type = ['bmp','jpg','png','jpeg'])
    if uploaded_file != None:
        file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type}
        st.write(file_details)
        # st.write(type(uploaded_file))
        image_data = uploaded_file.getvalue()
        st.image(image_data)   
        return Image.open(io.BytesIO(image_data))
    else:
        return None
    
def predict(model, image):
    print(type(image))
    output = model(image)
    return output

def main():
    model = load_model()
    image = load_image()
    if image is not None:
        result = predict(model,image)
        print(type(result))
        df = result.pandas().xyxy[0]
        print(df.to_dict('records'))
        # print(df.to_dict('records')[0]['confidence'])
        st.image(np.squeeze(result.render()))  
              
        records = df.to_dict('records')   
        st.header("Classes found in the image")
        for i, record in enumerate(records):
            confidence_percentage = record['confidence'] * 100
            st.subheader(f"[{i}: {record['name']}, {confidence_percentage:.2f}%]")
    else:
        st.warning("Please upload an image.")   

# def main():
#     model = load_model()
#     image = load_image()
#     result = predict(model,image)
#     print(type(result))
#     df = result.pandas().xyxy[0]
#     print(df.to_dict('records'))
#     # print(df.to_dict('records')[0]['confidence'])
#     st.image(np.squeeze(result.render()))  
          
#     records = df.to_dict('records')   
#     st.header("Classes found in the image")
#     for i, record in enumerate(records):
#         confidence_percentage = record['confidence'] * 100
#         st.subheader(f"[{i}: {record['name']}, {confidence_percentage:.2f}%]")

    # for i, record in enumerate(records):
    #     confidence_percentage = record['confidence'] * 100
    #     record_info = f"{record['name']}, {confidence_percentage:.2f}%"
    #     st.header(f"{record_info}")
main()


    
    
    
    


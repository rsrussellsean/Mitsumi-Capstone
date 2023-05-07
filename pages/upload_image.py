import streamlit as st
import io
import numpy as np
import zipfile
import helper
from model import load_model
from PIL import Image

def save_file(uploadedfile):
    with open(uploadedfile,"wb") as f:
            f.write(uploadedfile)
    return st.success("File Saved")

# YoloV5 model with 500 epochs
# def load_model():
#     run_model_path = 'models/bestv2_500.pt'
#     model = torch.hub.load('ultralytics/yolov5','custom',path=run_model_path,force_reload=True)
#     model.eval()
#     return model
        
def predict(model, image):
    output = model(image)
    return np.squeeze(output.render())

def load_image():
    st.title("Test images for Qualification of Resin Application")
    st.markdown('<div style="display: flex; justify-content: center; margin:20px 20px">'
                '<span style="color: #FF7220; font-size: 24px;">• NoResin</span>'
                '<span style="color: #FE9E97; font-size: 24px; margin-left: 20px;">• Lacking</span>'
                '<span style="color: #FF3837; font-size: 24px; margin-left: 20px;">• Good</span>'
                '<span style="color: #FFB21D; font-size: 24px; margin-left: 20px;">• Over</span>'
                '</div>', 
                unsafe_allow_html=True)
    uploaded_files = st.file_uploader('Generated with YoloV5', type = ['bmp','jpg','png','jpeg'], accept_multiple_files=True)
    images = []
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type}
            # st.write(file_details)
            image_data = uploaded_file.getvalue()
            # st.image(image_data)
            image = Image.open(io.BytesIO(image_data))
            images.append((image, uploaded_file.name))
            
    return images

def main():
    model = load_model()
    images = load_image()
    if images:
        all_predictions = []
        file_names = []
        predicted_images = []  # To store predicted images
        with st.container():
            for image, file_name in images:
                predicted_image = predict(model,image)
                with st.expander(file_name):
                    st.image(image)
                    st.image(predicted_image)
                    result = model(image)
                    df = result.pandas().xyxy[0]
                    records = df.to_dict('records')
                    all_predictions.append(records)
                    file_names.append(file_name)
                    predicted_images.append(predicted_image)  # Add predicted image to list
                    st.subheader(f"Classes found in {file_name}")
                    for i, record in enumerate(records):
                        confidence_percentage = record['confidence'] * 100
                        st.subheader(f"{record['name']}, {confidence_percentage:.2f}%")
                        
            st.text("")
            st.text("")
            
            # # Create the XLS file
            # xls_data = helper.create_xls(all_predictions, file_names)

            # # Add the download button
            # if xls_data:
            #     st.download_button(
            #         label="Download xls",
            #         data=xls_data,
            #         file_name="resin.xls",
            #         mime="application/vnd.ms-excel",
            #     )
            # else:
            #     st.warning("Unable to create the XLS file.")
                
            
            # Create the CSV file
            csv_data = helper.create_csv(all_predictions, file_names)

            # Add the download button
            if csv_data:
                st.download_button(
                    label="Download Data",
                    data=csv_data,
                    file_name="result_data.csv",
                    mime="application/vnd.ms-excel",
                )
            else:
                st.warning("Unable to create the CSV file of data.")
            
            # Add a download button for predicted images
            if predicted_images:
                def download_predicted_images():
                    zip_file = io.BytesIO()
                    with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                        for i, image in enumerate(predicted_images):
                            buffer = io.BytesIO()
                            Image.fromarray(image).save(buffer, format="BMP")
                            file_name = f"{file_names[i]}.bmp"
                            zf.writestr(file_name, buffer.getvalue())
                    zip_file.seek(0)
                    return zip_file.getvalue()

                predicted_images_data = download_predicted_images()

                st.download_button(
                    label="Download Predicted Images",
                    data=predicted_images_data,
                    file_name="predicted_images.zip",
                    mime="application/zip",
                )
            else:
                st.warning("Unable to create a ZIP file of predicted images.")
    else:
        st.warning("Please upload at least one image.")
        
main()

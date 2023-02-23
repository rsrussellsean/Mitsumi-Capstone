
from PIL import Image
import numpy as np
import av
import streamlit as st
import helper
import random
import logging
import os
os.environ["STREAMLIT_SERVER_RUNNING_MODE"] = "RunOnSave"

DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# confidence_threshold = st.slider(
#     "Confidence threshold", 0.0, 1.0, DEFAULT_CONFIDENCE_THRESHOLD, 0.05
# )

class VideoProcessorMaker:
    saved_records = []
    threshold = 0.5
    batch_number = None

    def __init__(self, batch_name) -> None:
        self.batch_number = batch_name

    def make(self):
        VideoProcessor.batch_number = self.batch_number
        return VideoProcessor
class VideoProcessor:
    saved_records = []
    threshold = 0.5
    batch_number = None
    end_callback = None
    classes_found = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # vision processing
        flipped = img[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        results = st.model(im_pil, size=112)
        df = results.pandas().xyxy[0]

        if len(df.index) > 0:
            records = df.to_dict('records')
            if len(records) > 0:
                # results.save()
                filtered_record = helper.filter_data_by_treshold(
                    records, self.threshold)
                if len(filtered_record) > 0:
                    self.saved_records.append(filtered_record)

        bbox_img = np.array(results.render()[0])

        return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")

    def on_ended(self):
        print('====Video Ended====')

        jsonData = self.saved_records

        flatData = helper.flat_result_data(jsonData)
        classes_found = helper.get_categories(flatData)
        st.header(classes_found)

        print("====Classes Found====")
        print(classes_found)

        print("====JSON Data====")
        helper.print_json_data(flatData)

        rand_number = random.randint(100000, 1000000)

        if self.batch_number:
            rand_number = self.batch_number

        helper.export_to_json(jsonData, rand_number)
        


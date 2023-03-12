import numpy as np
import av
import streamlit as st
import helper
import random
import os
import torch
import pandas as pd
import time
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from model import load_model


os.environ["STREAMLIT_SERVER_RUNNING_MODE"] = "RunOnSave"

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

    def __init__(self, threshold, batch_number, end_callback=None):
        self.threshold = threshold
        self.batch_number = batch_number
        self.end_callback = end_callback

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


st.title('Automatic Qualification of Resin Application')
st.caption('in collaboration with MinebeaMitsumi')

batch_number = 0
if 'item_batch_count' not in st.session_state:
    st.session_state['item_batch_count'] = 0

if not hasattr(st, 'classifier'):
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    st.model = load_model()

score_threshold = st.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.05)


streaming_placeholder = st.empty()

with streaming_placeholder.container():
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_processor_factory=lambda: VideoProcessor(
            threshold=score_threshold, batch_number=batch_number
        ),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

    
            
if st.checkbox("Show the detected labels", value=True):
    if webrtc_ctx.state.playing:
        labels_placeholder = st.empty()
        while True:
            try:
                json_data = webrtc_ctx.video_processor.saved_records
                df = pd.DataFrame(helper.flat_result_data(json_data))
                labels_placeholder.table(df)
                time.sleep(0.5)
            except IndexError:
                pass


import numpy as np
import av
import streamlit as st
# import random
import os
import torch
import pandas as pd
import time
import helper
import cv2
from model import load_model
from PIL import Image
from streamlit_webrtc import webrtc_streamer, WebRtcMode

import copy


os.environ["STREAMLIT_SERVER_RUNNING_MODE"] = "RunOnSave"
class VideoProcessorMaker:
    saved_records = []
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
    canny = False

    def __init__(self, batch_number, end_callback=None):
        self.batch_number = batch_number
        self.end_callback = end_callback
        self.last_detected_data = None
        self.timer_start = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # update canny
        if self.canny:
            img = cv2.cvtColor(cv2.Canny(img, self.canny_threshold1, self.canny_threshold2), cv2.COLOR_GRAY2BGR)
            
        # vision processing
        flipped = img[:, ::-1, :]
        
        # model processing
        im_pil = Image.fromarray(img)
        results = st.model(im_pil, size=224)#112 224 256
        df = results.pandas().xyxy[0]

        if len(df.index) > 0:
            records = df.to_dict('records')
            if len(records) > 0:
                # results.save()
                filtered_record = helper.filter_data_by_treshold(
                    records, self.threshold)
                if len(filtered_record) > 0:
                    self.last_detected_data = filtered_record
                    self.timer_start = time.time()

        # check if 5 seconds have passed since last detection
        if self.last_detected_data and time.time() - self.timer_start >= 0.5:
            self.saved_records.append(self.last_detected_data)
            self.last_detected_data = None
            self.timer_start = None

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

        # rand_number = random.randint(100000, 1000000)

        # if self.batch_number:
        #     rand_number = self.batch_number

        # helper.export_to_json(jsonData, rand_number)

st.title('Automatic Qualification of Resin Application')
st.caption('in collaboration with MinebeaMitsumi')

batch_number = 0
if 'item_batch_count' not in st.session_state:
    st.session_state['item_batch_count'] = 0

if not hasattr(st, 'classifier'):
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    st.model = load_model()


streaming_placeholder = st.empty()

with streaming_placeholder.container():
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_processor_factory=lambda: VideoProcessor(
            batch_number=batch_number
        ),
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )
    
# save Batch
if st.button("Save Batch"):
    if webrtc_ctx.video_processor.saved_records:
        print('Found classes:', webrtc_ctx.video_processor.classes_found)
        os.makedirs("./output", exist_ok=True)
        batch_number = st.session_state['item_batch_count'] + 1
        VideoProcessorMaker(batch_name=batch_number).make()
        st.session_state['item_batch_count'] = batch_number
        st.success(f"Batch {batch_number} saved!")
        
        print("====SAVED====")
        json_data = webrtc_ctx.video_processor.saved_records
        helper.export_to_json(json_data, batch_number)
        webrtc_ctx.video_processor.on_ended()
    else:
        st.warning("No classes found in this batch!")

# adjust threshold
score_threshold = st.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.05, key="score_threshold")

if webrtc_ctx.state.playing and webrtc_ctx.video_processor:
    if "score_threshold" not in st.session_state:
        st.session_state["score_threshold"] = 0.5

    if score_threshold != st.session_state["score_threshold"]:
        webrtc_ctx.video_processor.threshold = score_threshold
        st.session_state["score_threshold"] = score_threshold

# Canny edge threshold
if st.checkbox("Canny Edge Detection", value=False):
    canny_threshold1 = st.slider("Canny Threshold 1", 0, 255, 100, 5)
    canny_threshold2 = st.slider("Canny Threshold 2", 0, 255, 200, 5)
    if webrtc_ctx.state.playing and webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.canny = True
        webrtc_ctx.video_processor.canny_threshold1 = canny_threshold1
        webrtc_ctx.video_processor.canny_threshold2 = canny_threshold2
else:
    if webrtc_ctx.state.playing and webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.canny = False

# detected table
if st.checkbox("Show the detected labels", value=False):
    if webrtc_ctx.state.playing:
        labels_placeholder = st.empty()
        while True:
            try:
                json_data = webrtc_ctx.video_processor.saved_records
                df = pd.DataFrame(helper.flat_result_data(json_data))
                labels_placeholder.table(df)
                # time.sleep(0.5)
            except IndexError:
                pass
    
    
# if st.checkbox("Show the detected labels", value=False):
#     if webrtc_ctx.state.playing:
#         labels_placeholder = st.empty()
#         last_data = []
#         while True:
#             try:
#                 json_data = webrtc_ctx.video_processor.saved_records
#                 df = pd.DataFrame(helper.flat_result_data(json_data))
#                 # check if new data has been added since last loop
#                 if json_data != last_data:
#                     last_data = copy.deepcopy(json_data)
#                     labels_placeholder.table(df)
#                 time.sleep(0.5)
#             except IndexError:
#                 pass
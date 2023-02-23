import streamlit as st
from model import load_model
import torch
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from video_processor import VideoProcessorMaker


st.title('Automatic Qualification of Resin Application')
st.caption('in collaboration with MinebeaMitsumi')

batch_number = 0
if 'item_batch_count' not in st.session_state:
    st.session_state['item_batch_count'] = 0

if not hasattr(st, 'classifier'):
    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
    st.model = load_model()

# batch_number = st.number_input(
#     'Insert batch number', format="%d", value=1001, step=1)
# if st.button('Submit'):
#     st.write('Batch '+str(batch_number)+' would be recorded')
#     st.session_state['item_batch_count'] += 1
# else:
#     st.write("Submit to record this detection")

webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessorMaker(batch_number).make(),
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)


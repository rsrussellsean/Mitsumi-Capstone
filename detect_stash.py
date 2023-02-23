# import streamlit as st
# import torch
# import cv2
# import av
# from streamlit_webrtc import webrtc_streamer, WebRtcMode
# from PIL import Image
# import numpy as np
# import json
# import os
# import random

# st.header('Defect Detection')


# def load_model():
#     run_model_path = './best.pt'
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path=run_model_path)
#     # model.eval()
#     return model

# # model = load_model()


# if not hasattr(st, 'classifier'):
#     torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
#     st.model = load_model()
#     # st.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',  _verbose=False)

# batchNumber = st.number_input(
#     'Insert batch number', format="%d", value=1001, step=1)
# if st.button('Submit'):
#     st.write('Batch '+str(batchNumber)+' would be recorded')
#     st.session_state['item_batch_count'] += 1
# else:
#     st.write("Submit to record this detection")


# class VideoProcessor:
#     savedRecords = []
#     def recv(self, frame):
#         img = frame.to_ndarray(format="bgr24")
#         # vision processing
#         flipped = img[:, ::-1, :]

#         # model processing
#         im_pil = Image.fromarray(flipped)
#         results = st.model(im_pil, size=112)
#         df = results.pandas().xyxy[0]

#         if len(df.index) > 0:
#             records = df.to_dict('records')
#             if len(records) > 0:
#                 # results.save()
#                 filteredRecord = list(filter(lambda record: record['confidence'] > 0.4,records))
#                 if len(filteredRecord) > 0:
#                     self.savedRecords.append(filteredRecord)

#         bbox_img = np.array(results.render()[0])


#         return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
#     def on_ended(self):
#         print('====Video Ended====')
#         jsonData = self.savedRecords

#         rand_number = random.randint(100000,1000000)
#         if batchNumber:
#             rand_number = batchNumber
#         with open("output-"+str(rand_number)+".json", "w") as outfile:
#             json.dump(jsonData, outfile)
#         outfile.close()


# # class VideoProcessor:
# #     saved_records = []
# #     def recv(self, frame):
# #         img = frame.to_ndarray(format="bgr24")
# #         # vision processing
# #         flipped = img[:, ::-1, :]

# #         # model processing
# #         im_pil = Image.fromarray(flipped)
# #         results = st.model(im_pil, size=112)
# #         df = results.pandas().xyxy[0]

# #         if len(df.index) > 0:
# #             records = df.to_dict('records')
# #             if len(records) > 0:
# #                 # results.save()
# #                 filtered_record = list(filter(lambda record: record['confidence'] > threshold,records))
# #                 if len(filtered_record) > 0:
# #                     self.saved_records.append(filtered_record)

# #         bbox_img = np.array(results.render()[0])


# #         return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
# #     def on_ended(self):
# #         print('====Video Ended====')

# #         jsonData = self.saved_records


# #         flatData = helper.flat_result_data(jsonData)
# #         classes_found = helper.get_categories(flatData)

    
# #         print("====Classes Found====")
# #         print(classes_found)

# #         rand_number = random.randint(100000,1000000)

# #         if batchNumber:
# #             rand_number = batchNumber

# #         helper.export_to_json(jsonData,rand_number)



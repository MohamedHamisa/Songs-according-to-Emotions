import streamlit as st  #like flask web workframe to build web apps that used in it common components
from streamlit_webrtc import webrtc_streamer  #stream webrtc api to access local media devices 
#webrtc_streamer is an experiment to stream video capture devices through webRTC using simple mechanism 
import av   #av is used to access your media through streames or frames and to get data from/to packages
import mediapipe as mp 
import numpy as np 
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model 
model  = load_model("model.h5")
label = np.load("labels.npy")



holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils
if "run" not in st.session_state :
  st.session_state["run"] = "true"   #to be able to run the code multuple time seperatelt
try:
  emotions = np.load("emotion.npy")[0]  #the emotion is array so we want to access the zeroth element
except:
  emotion=""
if not (emotion):
  st.session_state["run"] = "true" 
else:
  st.session_state["run"] = "false"   
class EmotionsProcessor:
  def recv(self,frame):
      frm = frame.to_ndarray(frm,format="bgr24") #bgr24 is format with 24 bits per pixels
  
      frm = cv2.flip(frm, 1)

      res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
      lst = []

      if res.face_landmarks:
        for i in res.face_landmarks.landmark:
          lst.append(i.x - res.face_landmarks.landmark[1].x)
          lst.append(i.y - res.face_landmarks.landmark[1].y)

        if res.left_hand_landmarks:
          for i in res.left_hand_landmarks.landmark:
            lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
            lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
        else:
          for i in range(42):
            lst.append(0.0)

        if res.right_hand_landmarks:
          for i in res.right_hand_landmarks.landmark:
            lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
            lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
        else:
          for i in range(42):
            lst.append(0.0)
        lst=np.array(lst).reshape(-1,1)
        pred=label[np.argmax(model.predict(lst))]   
        print(pred)
        cv2.putText(frm, str(data_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
        np.save("emotion.npy",np.array([pred]))

      drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_CONTOURS)
      drawing.draw_landmarks(frm, res.left_hand_landmarks, hands.HAND_CONNECTIONS)
      drawing.draw_landmarks(frm, res.right_hand_landmarks, hands.HAND_CONNECTIONS)


      return av.VideoFrame.from_ndarray(frm,format="bgr24")
lang= st.text_input("Language")
singer=st.text_input("Singer")
if lang and singer and st.session_state ["run"]!=  "false" :
  webrtc_streamer(key="key" . desired_playing_state = True
                    video_processor_factory=EmotionProcessor)
btn = st.button ("recommend me a song")  
if btn :
  if not (emotion):
    st.warning("please let capyure your emotion")
    st.session_state["run"] = "true" 
  else:
    webbrowser.open(f"http://www.youtube.com/result?search_query={lang}+{emotion}+song+{singer}") 
    np.save("emotion.npy",np.array([""])) #if you open the browser it will reset the emotions    
    st.session_state["run"] = "false"  













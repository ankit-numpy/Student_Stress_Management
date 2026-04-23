import streamlit as st
import numpy as np
import pickle
import pandas as pd
import plotly.express as px
import cv2
import os
from dotenv import load_dotenv
import google.generativeai as genai
from deepface import DeepFace

# ================= CHATBOT =================
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
chat_model = genai.GenerativeModel("gemini-flash-latest")

def get_response(user_input):
    try:
        response = chat_model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ================= EMOTION =================
def detect_emotion():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        try:
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )
            return result[0]['dominant_emotion']
        except:
            return "Not detected"
    return "Camera Error"

# ================= MODEL =================
model = pickle.load(open("model.pkl","rb"))

# ================= PAGE =================
st.set_page_config(page_title="AI Stress Management",layout="wide")

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page="Home"

if "user" not in st.session_state:
    st.session_state.user=None

if "stress_history" not in st.session_state:
    st.session_state.stress_history=[]

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

# ================= UI STYLE =================
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#e3f2fd,#e0f2f1,#f1f8e9);
}

.glass{
background:rgba(255,255,255,0.15);
backdrop-filter:blur(12px);
padding:40px;
border-radius:20px;
box-shadow:0 0 25px rgba(0,0,0,0.1);
}

.stButton>button{
border-radius:12px;
background:#5c6bc0;
color:white;
font-weight:bold;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.05);
box-shadow:#3f51b5 0px 5px 15px;
}
</style>
""",unsafe_allow_html=True)

# ================= NAVBAR =================
st.markdown("## 🌐 AI Student Stress Management")

c1,c2,c3,c4,c5=st.columns(5)

if c1.button("Home"):
    st.session_state.page="Home"

if c2.button("Login"):
    st.session_state.page="Login"

if c3.button("Analyze Stress"):
    st.session_state.page="Analyze"

if c4.button("Solutions"):
    st.session_state.page="Solutions"

if c5.button("Dashboard"):
    st.session_state.page="Dashboard"

st.markdown("---")

# =================================================
# HOME
# =================================================
if st.session_state.page=="Home":

    st.title("Understanding Student Stress")

    st.write("""
Stress is the body's psychological response to overwhelming challenges.
After COVID-19, global surveys reported **70%+ students experiencing anxiety**.

### Effects on Students
• Academic pressure  
• Social media comparison  
• Career uncertainty  
• Financial stress  

### Causes
• Sleep deprivation  
• Study overload  
• Emotional isolation  
• Fear of failure
""")

    data=pd.DataFrame({
        "Country":["India","USA","UK","China","Canada"],
        "Stress Level":[78,68,63,72,55]
    })

    fig=px.bar(data,x="Country",y="Stress Level",
               title="Global Student Stress Survey")
    st.plotly_chart(fig,use_container_width=True)

# =================================================
# LOGIN
# =================================================
elif st.session_state.page=="Login":

    col1,col2=st.columns(2)

    with col1:
        st.markdown('<div class="glass">',unsafe_allow_html=True)

        st.subheader("Login / Sign Up")

        username=st.text_input("Username")
        password=st.text_input("Password",type="password")

        if st.button("Login", key="login"):
            st.session_state.user=username
            st.session_state.page="Analyze"

        st.write("New User?")
        if st.button("Create Account", key="signup"):
            st.session_state.user=username
            st.session_state.page="Analyze"

        st.markdown("</div>",unsafe_allow_html=True)

    with col2:
        st.image("boy_stress.jpg",use_container_width=True)

# =================================================
# ANALYZE
# =================================================
elif st.session_state.page=="Analyze":

    if not st.session_state.user:
        st.warning("Please Login First")
    else:

        st.title("AI Stress Analysis")

        auto_value=5

        if st.button("Detect Emotion",key="emotion"):
            emotion=detect_emotion()
            st.success(f"Detected Emotion: {emotion}")

            auto_map={
                "happy":2,
                "sad":8,
                "angry":7,
                "fear":9,
                "neutral":4
            }

            auto_value=auto_map.get(emotion,5)

        col1,col2=st.columns(2)

        with col1:
            anxiety=st.slider("Anxiety",0,10,auto_value)
            self_esteem=st.slider("Self Esteem",0,10)
            mental_health=st.slider("Mental Health History",0,10)
            depression=st.slider("Depression",0,10)
            headache=st.slider("Headache",0,10)
            bp=st.slider("Blood Pressure",0,10)
            sleep=st.slider("Sleep Quality",0,10)
            breathing=st.slider("Breathing Problem",0,10)

        with col2:
            noise=st.slider("Noise Level",0,10)
            living=st.slider("Living Conditions",0,10)
            safety=st.slider("Safety",0,10)
            basic=st.slider("Basic Needs",0,10)
            academic=st.slider("Academic Performance",0,10)
            study_load=st.slider("Study Load",0,10)
            teacher=st.slider("Teacher Relationship",0,10)
            future=st.slider("Future Concerns",0,10)
            social=st.slider("Social Support",0,10)
            peer=st.slider("Peer Pressure",0,10)
            extra=st.slider("Extracurricular Activities",0,10)
            bullying=st.slider("Bullying",0,10)

        input_data=np.array([[anxiety,self_esteem,mental_health,depression,
                              headache,bp,sleep,breathing,
                              noise,living,safety,basic,
                              academic,study_load,teacher,future,
                              social,peer,extra,bullying]])

        if st.button("Analyze Stress",key="analyze"):

            result=model.predict(input_data)[0]
            st.session_state.stress_history.append(result)

            if result==2:
                st.error("High Stress")
            elif result==1:
                st.warning("Medium Stress")
            else:
                st.success("Low Stress")

        st.markdown("### Ask AI Assistant")

        user_input=st.text_input("Ask something...")
        if user_input:
            reply=get_response(user_input)
            st.session_state.chat_history.append(reply)
            st.write(reply)

# =================================================
# SOLUTIONS
# =================================================
elif st.session_state.page=="Solutions":

    st.title("Stress Relief Solutions")

    st.write("""
Yoga, meditation and exercise reduce cortisol levels and improve emotional balance.
Daily practice enhances focus, sleep and mental resilience.
""")

    st.video("https://www.youtube.com/watch?v=v7AYKMP6rOE")

    st.subheader("Healing Music Therapy")

    st.audio("https://cdn.pixabay.com/audio/2022/03/15/audio_115b9b6f0f.mp3")

    st.video("https://www.youtube.com/watch?v=2OEL4P1Rz04")

# =================================================
# DASHBOARD
# =================================================
elif st.session_state.page=="Dashboard":

    st.title("Student Stress Visualization Dashboard")

    st.write("""
This dashboard visualizes previous stress records to help students understand emotional patterns.
""")

    if st.session_state.stress_history:

        df=pd.DataFrame({"Stress":st.session_state.stress_history})
        fig=px.line(df,y="Stress",title="Stress Trend")
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("""
### Recommendation
Follow these steps:
• Maintain sleep schedule  
• Practice meditation  
• Stay socially connected  
• Exercise regularly
""")
    else:
        st.info("No stress data yet.")

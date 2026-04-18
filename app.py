import streamlit as st
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# UI improvements
st.markdown("### 🚀 Your Mental Health Companion")
st.divider()  

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Stress Detector", layout="wide")

st.title("🎓 AI Student Stress Analyzer")

# Sidebar
st.sidebar.header("About")
st.sidebar.write("AI आधारित Stress Detection System")

# Inputs
st.subheader("Enter Your Details")

anxiety = st.slider("Anxiety Level", 0, 10)
self_esteem = st.slider("Self Esteem", 0, 10)
mental_health = st.slider("Mental Health History", 0, 10)
depression = st.slider("Depression", 0, 10)
headache = st.slider("Headache", 0, 10)
bp = st.slider("Blood Pressure", 0, 10)
sleep = st.slider("Sleep Quality", 0, 10)
breathing = st.slider("Breathing Problem", 0, 10)
noise = st.slider("Noise Level", 0, 10)
living = st.slider("Living Conditions", 0, 10)
safety = st.slider("Safety", 0, 10)
basic = st.slider("Basic Needs", 0, 10)
academic = st.slider("Academic Performance", 0, 10)
study_load = st.slider("Study Load", 0, 10)
teacher = st.slider("Teacher-Student Relationship", 0, 10)
future = st.slider("Future Career Concerns", 0, 10)
social = st.slider("Social Support", 0, 10)
peer = st.slider("Peer Pressure", 0, 10)
extra = st.slider("Extracurricular Activities", 0, 10)
bullying = st.slider("Bullying", 0, 10)

input_data = np.array([[anxiety, self_esteem, mental_health, depression,
                        headache, bp, sleep, breathing, noise, living,
                        safety, basic, academic, study_load, teacher,
                        future, social, peer, extra, bullying]])

# Prediction
if st.button("🔍 Predict Stress Level"):
    result = model.predict(input_data)[0]

    st.subheader("Result")

    if result == 2:
        st.error("🔴 High Stress")
        suggestion = "Meditation, sleep improve, reduce study load"
    elif result == 1:
        st.warning("🟡 Medium Stress")
        suggestion = "Improve time management & social support"
    else:
        st.success("🟢 Low Stress")
        suggestion = "Maintain your routine 👍"

    st.write("💡 Suggestion:", suggestion)

    # Save history
    data = {
        "date": datetime.datetime.now(),
        "stress": result
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv("history.csv")
        df = pd.concat([old, df])
    except:
        pass

    df.to_csv("history.csv", index=False)

# 📊 GRAPH
st.subheader("📊 Stress Trend")

try:
    history = pd.read_csv("history.csv")
    plt.plot(history["stress"])
    plt.xlabel("Time")
    plt.ylabel("Stress Level")
    st.pyplot(plt)
except:
    st.write("No history yet")

# Adding chatbot
st.subheader("💬 AI Assistant")

user_input = st.text_input("Ask about stress...")

if user_input:
    if "stress" in user_input.lower():
        st.write("Try meditation, exercise, and proper sleep.")
    elif "sleep" in user_input.lower():
        st.write("Maintain 7-8 hours sleep daily.")
    else:
        st.write("I am here to help you manage stress 😊")


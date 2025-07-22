import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import webbrowser
import time
import random
import os
import pyautogui
import pygetwindow as gw

# Load the emotion detection model
model_path = os.path.join(os.getcwd(), "_mini_XCEPTION.102-0.66.hdf5")
if not os.path.exists(model_path):
    raise FileNotFoundError("⚠ '_mini_XCEPTION.102-0.66.hdf5' file not found in your project folder.")

model = load_model(model_path, compile=False)
print("✅ Model loaded successfully!")

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Telugu Movie suggestions for each emotion
telugu_movie_suggestions = {
    'Happy': ['Ala Vaikunthapurramuloo', 'Fidaa', 'Geetha Govindam'],
    'Sad': ['Jersey', 'Dear Comrade', 'Manasantha Nuvve'],
    'Angry': ['Arjun Reddy', 'Pushpa', 'Temper'],
    'Surprise': ['Evaru', 'Kshanam', 'Goodachari'],
    'Fear': ['Avunu', 'Gruham', 'Rakshasudu'],
    'Disgust': ['Garudavega', 'Vikramarkudu', 'Bhadra'],
    'Neutral': ['Maharshi', 'Nuvvu Nenu', 'Sita Ramam']
}

def search_and_play_youtube(movie_name):
    query = f"{movie_name} Telugu official trailer"
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    # Open YouTube in browser
    webbrowser.open(url)
    time.sleep(6)

    # Bring browser window to front (for Chrome or Edge)
    for window in gw.getWindowsWithTitle("YouTube"):
        try:
            window.activate()
            break
        except:
            pass

    time.sleep(3)
    
    # Click on the top video thumbnail
    pyautogui.moveTo(400, 350, duration=0.5)  # Approximate top-left video location
    pyautogui.click()
    print("▶ Automatically clicked top video to play the trailer.")

def predict_emotion(roi_gray):
    roi = cv2.resize(roi_gray, (64, 64))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    prediction = model.predict(roi, verbose=0)[0]
    return emotion_labels[np.argmax(prediction)]

while True:
    cap = cv2.VideoCapture(0)
    time.sleep(1)

    detected_emotion = None
    detected_movie = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            emotion = predict_emotion(roi_gray)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            text = f"You are looking {emotion}"
            movie_choice = random.choice(telugu_movie_suggestions[emotion])
            suggestion = f"I suggest: {movie_choice}"

            detected_emotion = emotion
            detected_movie = movie_choice

            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 0), 2)
            cv2.putText(frame, suggestion, (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 255), 2)

            cv2.imshow("Mood Detector", frame)
            cv2.waitKey(3000)
            cap.release()
            cv2.destroyAllWindows()
            break

        cv2.imshow("Mood Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            print("👋 Exiting program.")
            exit()

        if detected_emotion:
            break

    cap.release()
    cv2.destroyAllWindows()

    if detected_movie:
        print(f"\n🎭 You seem: {detected_emotion}")
        print(f"🎬 Movie suggestion: {detected_movie}")
        print("📽 Opening YouTube trailer...")
        search_and_play_youtube(detected_movie)

    user_input = input("\n▶ After watching trailer, press Enter to scan your emotion again or type 'q' to quit: ")
    if user_input.strip().lower() == 'q':
        print("👋 Exiting program.")
        break
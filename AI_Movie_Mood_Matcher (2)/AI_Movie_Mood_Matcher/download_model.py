import requests

url = "https://github.com/omar178/Emotion-recognition/releases/download/v1.0/emotion_model.hdf5"
r = requests.get(url)

with open("emotion_model.hdf5", "wb") as f:
    f.write(r.content)

print("Model downloaded successfully!")
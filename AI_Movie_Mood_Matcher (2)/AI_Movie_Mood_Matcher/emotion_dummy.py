import cv2
import random

# Simulated emotions list
emotions = ['Happy', 'Sad', 'Angry', 'Neutral', 'Excited', 'Bored']

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Choose a random emotion to simulate
    emotion = random.choice(emotions)

    # Display the emotion on screen
    cv2.putText(frame, f"Emotion: {emotion}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("AI Mood Matcher - Dummy Emotion", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
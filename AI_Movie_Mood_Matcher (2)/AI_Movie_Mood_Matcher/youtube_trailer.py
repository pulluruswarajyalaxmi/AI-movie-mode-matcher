import cv2
import random
import webbrowser

# Simulated emotions
emotions = ['Happy', 'Sad', 'Angry', 'Neutral', 'Excited', 'Bored']

# Emotion → Movie Map
mood_movie_map = {
    "Happy": ["Zindagi Na Milegi Dobara", "The Pursuit of Happyness"],
    "Sad": ["Dear Zindagi", "The Fault in Our Stars"],
    "Angry": ["John Wick", "Gladiator"],
    "Neutral": ["The Social Network", "Inception"],
    "Excited": ["Spiderman: No Way Home", "Avengers Endgame"],
    "Bored": ["The Office", "Brooklyn Nine-Nine"]
}

# Track emotion change
current_emotion = None

# Webcam setup
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Pick random emotion
    emotion = random.choice(emotions)

    # Display on video
    cv2.putText(frame, f"Emotion: {emotion}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("AI Mood Matcher - YouTube Trailer", frame)

    # When emotion changes
    if emotion != current_emotion:
        current_emotion = emotion
        movie = random.choice(mood_movie_map[emotion])
        print(f"🎬 Emotion: {emotion} → Try Watching: {movie}")
        
        # Search for movie trailer on YouTube
        search_url = f"https://www.youtube.com/results?search_query={movie} trailer"
        webbrowser.open(search_url)

    # Exit key
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from audio import BeepSoundManager  # Import BeepSoundManager from audio.py
from feedback import check_posture, speak_feedback  # Import the feedback logic

# Initialize MediaPipe Pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Constants
SIMILARITY_THRESHOLD = 0.7  # Threshold for pose similarity
FEEDBACK_COOLDOWN = 5  # Cooldown period for feedback in seconds

# Initialize the beep manager
beep_manager = BeepSoundManager()

def calculate_similarity(landmarks_1, landmarks_2):
    """
    Compare two sets of pose landmarks and calculate similarity.
    We'll use Euclidean distance as a simple similarity measure here.
    """
    if not landmarks_1 or not landmarks_2:
        return 0  # If any of the landmarks are missing, return no similarity.

    # Extract x, y coordinates of landmarks from both sets
    landmarks_1 = np.array([[lm.x, lm.y] for lm in landmarks_1.landmark])
    landmarks_2 = np.array([[lm.x, lm.y] for lm in landmarks_2.landmark])

    # Calculate Euclidean distance between corresponding landmarks
    distances = np.linalg.norm(landmarks_1 - landmarks_2, axis=1)
    similarity_score = 1 - (np.mean(distances) / 0.5)  # Normalize the similarity
    similarity_score = max(0, similarity_score)  # Ensure similarity isn't negative
    return similarity_score

def detect_pose_image(image_path):
    """
    Detect pose landmarks from a reference image and return them for comparison.
    """
    try:
        # Load and process the image
        image = cv2.imread(image_path)
        if image is None:
            print("Error: Could not read the image.")
            return None, None

        # Resize for consistent comparison
        image = cv2.resize(image, (400, 400))
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect pose on the image
        result = pose.process(rgb_image)
        if result.pose_landmarks:
            print("Reference image landmarks detected successfully.")
            return image, result.pose_landmarks
        else:
            print("No landmarks detected in the reference image.")
            return None, None
    except Exception as e:
        print(f"Error processing reference image: {e}")
        return None, None

def process_frame(frame, reference_landmarks):
    """
    Process a single frame from the webcam feed, detect landmarks, and compare with reference.
    """
    # Resize the frame
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect landmarks in the frame
    result = pose.process(rgb_frame)

    if result.pose_landmarks:
        # Draw landmarks on the frame
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Calculate similarity with the reference image
        similarity = calculate_similarity(reference_landmarks, result.pose_landmarks)

        # Overlay similarity score on the frame
        cv2.putText(
            frame,
            f"Similarity: {similarity:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
        )

        # Trigger feedback if similarity is below the threshold
        if similarity < SIMILARITY_THRESHOLD:
            beep_manager.play_beep()
            feedback_messages = check_posture(result.pose_landmarks.landmark)
            for index, message in enumerate(feedback_messages):
                cv2.putText(
                    frame,
                    message,
                    (10, 60 + index * 30),  # Display feedback at an offset
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )
            if feedback_messages:
                speak_feedback(feedback_messages)
        else:
            print("Pose matched. No feedback needed.")

    return frame

def compare_webcam_to_reference(reference_image, reference_landmarks):
    """
    Start a webcam feed, compare detected landmarks with the reference image landmarks in real time,
    and show webcam feed and reference image on different windows.
    """
    cap = cv2.VideoCapture(0)  # Open webcam feed
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading webcam frame.")
                continue

            # Process the frame
            processed_frame = process_frame(frame, reference_landmarks)

            # Show the live webcam feed
            cv2.imshow("Live Webcam Feed", processed_frame)

            # Show the reference image in another window
            cv2.imshow("Reference Image", reference_image)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Stopping webcam comparison...")
                break

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Exiting.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Allow user to select the reference image
    Tk().withdraw()  # Hide the tkinter root window
    print("Select a reference image for comparison...")
    reference_image_path = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if not reference_image_path:
        print("No file selected. Exiting.")
    else:
        print("Processing reference image for landmarks...")
        reference_image, reference_landmarks = detect_pose_image(reference_image_path)
        if reference_landmarks is not None:
            print("Starting webcam feed for pose comparison...")
            compare_webcam_to_reference(reference_image, reference_landmarks)
        else:
            print("Could not detect landmarks from the reference image. Exiting.")
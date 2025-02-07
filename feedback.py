import pyttsx3
import threading
from collections import namedtuple

# Initialize text-to-speech engine
try:
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 150)  # Set speech rate
except Exception as e:
    print(f"Error initializing text-to-speech engine: {e}")
    tts_engine = None

# Define thresholds for posture checks
SHOULDER_THRESHOLD = 0.05  # Threshold for shoulder alignment
HIP_THRESHOLD = 0.05       # Threshold for hip alignment
BACK_THRESHOLD = 0.1       # Threshold for back straightness
HEAD_THRESHOLD = 0.2       # Threshold for head alignment
KNEE_THRESHOLD = 0.1       # Threshold for knee alignment
FEET_THRESHOLD = 0.15      # Threshold for feet alignment

# Define a namedtuple for landmarks
Landmark = namedtuple("Landmark", ["x", "y"])

def speak_feedback(feedback_messages):
    """
    Convert a list of feedback messages into speech asynchronously.
    """
    if not feedback_messages:
        print("No feedback to speak.")
        return

    def speak():
        if tts_engine:
            print(f"Speaking feedback: {feedback_messages}")  # Debugging message
            for message in feedback_messages:
                tts_engine.say(message)
            tts_engine.runAndWait()
        else:
            print("Text-to-speech engine not available.")

    # Run the speak function in a separate thread
    speech_thread = threading.Thread(target=speak)
    speech_thread.daemon = True  # Daemon thread to exit with the main program
    speech_thread.start()

def check_shoulders(left_shoulder, right_shoulder, feedback):
    """Check if shoulders are level."""
    if abs(left_shoulder.y - right_shoulder.y) > SHOULDER_THRESHOLD:
        if left_shoulder.y > right_shoulder.y:
            feedback.append("Your left shoulder is lower than your right. Straighten up.")
        else:
            feedback.append("Your right shoulder is lower than your left. Straighten up.")

def check_hips(left_hip, right_hip, feedback):
    """Check if hips are level."""
    if abs(left_hip.y - right_hip.y) > HIP_THRESHOLD:
        if left_hip.y < right_hip.y:
            feedback.append("Your left hip is higher than your right. Adjust your stance.")
        else:
            feedback.append("Your right hip is higher than your left. Adjust your stance.")

def check_back(shoulder, hip, feedback):
    """Check if back is straight."""
    if abs(shoulder.x - hip.x) > BACK_THRESHOLD:
        feedback.append("Your back is not straight. Keep your torso aligned with your hips.")

def check_head(head, shoulder, feedback):
    """Check for slouching (head too far forward)."""
    if head.x < shoulder.x - HEAD_THRESHOLD:
        feedback.append("You are slouching. Pull your head back to align with your shoulders.")

def check_knees(left_knee, right_knee, feedback):
    """Check if knees are bent unevenly."""
    if abs(left_knee.y - right_knee.y) > KNEE_THRESHOLD:
        feedback.append("Your knees are uneven. Stand with your legs balanced.")

def check_feet(left_foot, right_foot, feedback):
    """Check if feet are misaligned."""
    if abs(left_foot.x - right_foot.x) > FEET_THRESHOLD:
        feedback.append("Your feet are misaligned. Place them parallel to each other.")

def check_posture(landmarks):
    """Check posture based on landmarks and provide feedback."""
    feedback = []

    # Extract landmarks
    head = landmarks[0]
    left_shoulder = landmarks[1]
    right_shoulder = landmarks[2]
    left_hip = landmarks[3]
    right_hip = landmarks[4]
    left_knee = landmarks[5]
    right_knee = landmarks[6]
    left_foot = landmarks[7]
    right_foot = landmarks[8]

    # Perform posture checks
    check_shoulders(left_shoulder, right_shoulder, feedback)
    check_hips(left_hip, right_hip, feedback)
    check_back(left_shoulder, left_hip, feedback)
    check_head(head, left_shoulder, feedback)
    check_knees(left_knee, right_knee, feedback)
    check_feet(left_foot, right_foot, feedback)

    # Call text-to-speech for feedback
    if feedback:
        speak_feedback(feedback)
    else:
        print("No posture issues detected.")  # Debugging message

    return feedback

if __name__ == "__main__":
    try:
        while True:
            # Simulate landmarks data for testing
            landmarks = [
                Landmark(x=0.5, y=0.1),  # Head
                Landmark(x=0.5, y=0.5),  # Left shoulder
                Landmark(x=0.6, y=0.5),  # Right shoulder
                Landmark(x=0.5, y=0.8),  # Left hip
                Landmark(x=0.6, y=0.8),  # Right hip
                Landmark(x=0.5, y=1.0),  # Left knee
                Landmark(x=0.6, y=1.0),  # Right knee
                Landmark(x=0.5, y=1.2),  # Left foot
                Landmark(x=0.6, y=1.2),  # Right foot
            ]
            check_posture(landmarks)
    except KeyboardInterrupt:
        print("\nPose detection interrupted. Exiting gracefully.")
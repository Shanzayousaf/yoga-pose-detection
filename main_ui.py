import cv2
import mediapipe as mp
from tkinter import Tk, Button, Label, Frame, Canvas, Scale, HORIZONTAL, messagebox
from tkinter.filedialog import askopenfilename
from threading import Thread
import numpy as np
from PIL import Image, ImageTk
from audio import BeepSoundManager
from feedback import check_posture
import time
import os 
import random

# Initialize MediaPipe Pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Initialize the beep manager
beep_manager = BeepSoundManager()

# Global variables
is_webcam_running = False
reference_landmarks = None
reference_image = None
webcam_frame = None
last_feedback_time = 0  # Track the last time feedback was triggered
feedback_delay = 2  # Delay for feedback in seconds
similarity_threshold = 0.7  # Default similarity threshold
pose_match_start_time = None  # Track when the pose starts matching

# Function to detect pose from image
def detect_pose_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image.")
        return None, None

    # Resize the reference image to match the webcam feed size
    image = cv2.resize(image, (640, 480))  # Make sure it's the same size as webcam
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = pose.process(rgb_image)
    if result.pose_landmarks:
        print("Reference image landmarks detected successfully.")
        return image, result.pose_landmarks
    else:
        print("No landmarks detected in the reference image.")
        return None, None

# Function to calculate similarity between two sets of pose landmarks
def calculate_similarity(landmarks_1, landmarks_2):
    if not landmarks_1 or not landmarks_2:
        return 0  # If any of the landmarks are missing, return no similarity.

    landmarks_1 = np.array([[lm.x, lm.y] for lm in landmarks_1.landmark])
    landmarks_2 = np.array([[lm.x, lm.y] for lm in landmarks_2.landmark])

    distances = np.linalg.norm(landmarks_1 - landmarks_2, axis=1)
    similarity_score = 1 - (np.mean(distances) / 0.5)  # Normalize the similarity
    similarity_score = max(0, similarity_score)
    return similarity_score

# Function to compare webcam pose with reference
def compare_webcam_to_reference(reference_landmarks):
    global is_webcam_running, reference_image, webcam_frame, last_feedback_time, similarity_threshold, pose_match_start_time
    is_webcam_running = True

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while is_webcam_running:
        ret, frame = cap.read()
        if not ret:
            print("Error reading webcam frame.")
            continue

        # Resize webcam feed to match reference image size
        webcam_frame = cv2.resize(frame, (640, 480))  # Same size as reference image
        rgb_frame = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2RGB)

        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(webcam_frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            similarity = calculate_similarity(reference_landmarks, result.pose_landmarks)

            cv2.putText(webcam_frame, f"Similarity: {similarity:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Check if the pose is correct (below threshold) and trigger feedback only after the delay
            if similarity < similarity_threshold:
                current_time = time.time()
                if current_time - last_feedback_time >= feedback_delay:
                    beep_manager.play_beep()
                    feedback_messages = check_posture(result.pose_landmarks.landmark)
                    display_feedback(feedback_messages)
                    last_feedback_time = current_time
                pose_match_start_time = None  # Reset the pose match timer
            else:
                display_congrats_message()
                if pose_match_start_time is None:
                    pose_match_start_time = time.time()  # Start the timer when pose matches
                elif time.time() - pose_match_start_time >= 10:  # Check if pose matched for 10 seconds
                    pose_match_start_time = None  # Reset the timer
                    root.after(0, prompt_upload_new_image)  # Prompt to upload new image

        # Update canvas every frame
        root.after(0, update_canvas)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Stopping webcam comparison...")
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to prompt the user to upload a new image
def prompt_upload_new_image():
    global reference_landmarks, reference_image
    image_folder = "pictures"  # Folder containing images
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_files:
        random_image_path = os.path.join(image_folder, random.choice(image_files))
        print(f"Auto-loading new reference image: {random_image_path}")
        reference_image, reference_landmarks = detect_pose_image(random_image_path)
        if reference_landmarks:
            print("New reference image loaded successfully!")
        else:
            print("No landmarks detected in the new image.")
    else:
        print("No images found in the 'pictures' folder.")

# Function to update the canvas with webcam feed and reference image
def update_canvas():
    global webcam_frame
    if webcam_frame is not None:
        frame_rgb = cv2.cvtColor(webcam_frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame_rgb)
        frame_image_tk = ImageTk.PhotoImage(frame_image)
        canvas.create_image(0, 0, anchor="nw", image=frame_image_tk)
        canvas.image = frame_image_tk

    if reference_image is not None:
        ref_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        ref_image_pil = Image.fromarray(ref_image)
        ref_image_tk = ImageTk.PhotoImage(ref_image_pil)
        canvas.create_image(640, 0, anchor="nw", image=ref_image_tk)
        canvas.ref_image = ref_image_tk

    canvas.update()

# Function to display feedback
def display_feedback(messages):
    feedback_label.config(text="Feedback: " + "\n".join(messages), fg="red")
    root.after(2000, reset_feedback)

# Function to display the congrats message
def display_congrats_message():
    feedback_label.config(text="Congrats! Your pose matches! You are doing great 🎉💪", fg="green")
    root.after(2000, reset_feedback)

# Reset the feedback text after 2 seconds
def reset_feedback():
    feedback_label.config(text="")

# Start webcam in a new thread
def start_webcam():
    global reference_landmarks
    if reference_landmarks:
        Thread(target=compare_webcam_to_reference, args=(reference_landmarks,)).start()

def stop_webcam():
    global is_webcam_running
    is_webcam_running = False
    print("Stopping webcam...")

# Function to select image
def on_select_image():
    global reference_landmarks, reference_image
    reference_image_path = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if reference_image_path:
        print("Processing reference image for landmarks...")
        reference_image, reference_landmarks = detect_pose_image(reference_image_path)
        if reference_landmarks:
            print("Reference image processed successfully!")
        else:
            print("No landmarks detected.")
    else:
        print("No file selected.")

# Function to update similarity threshold
def update_threshold(value):
    global similarity_threshold
    similarity_threshold = float(value)
    threshold_label.config(text=f"Similarity Threshold: {similarity_threshold:.2f}")

# Create the Tkinter window
root = Tk()
root.title("Pose Detection")
root.geometry("1280x800")  # Larger size for better view

# Background color for window
root.configure(bg='#f0f0f0')

# Frame for buttons
button_frame = Frame(root, bg='#f0f0f0')
button_frame.pack(pady=10)

# Buttons with colors
select_image_button = Button(button_frame, text="Select Reference Image", command=on_select_image, bg="#4CAF50", fg="white", font=("Helvetica", 12))
select_image_button.grid(row=0, column=0, padx=20)

webcam_button = Button(button_frame, text="Start Webcam", command=start_webcam, bg="#2196F3", fg="white", font=("Helvetica", 12))
webcam_button.grid(row=0, column=1, padx=20)

stop_button = Button(button_frame, text="Stop Webcam", command=stop_webcam, bg="#f44336", fg="white", font=("Helvetica", 12))
stop_button.grid(row=0, column=2, padx=20)

# Slider for similarity threshold
threshold_label = Label(button_frame, text=f"Similarity Threshold: {similarity_threshold:.2f}", bg='#f0f0f0', font=("Helvetica", 12))
threshold_label.grid(row=1, column=0, columnspan=3, pady=10)

threshold_slider = Scale(button_frame, from_=0.1, to=1.0, resolution=0.05, orient=HORIZONTAL, command=update_threshold)
threshold_slider.set(similarity_threshold)
threshold_slider.grid(row=2, column=0, columnspan=3, pady=10)

# Create a Canvas for displaying webcam and reference image side by side
canvas = Canvas(root, width=1280, height=480, bg="white")
canvas.pack()

# Frame for feedback
feedback_frame = Frame(root, bg='#f0f0f0')
feedback_frame.pack(pady=10)

# Label for feedback
feedback_label = Label(feedback_frame, text="Feedback will appear here", bg='#f0f0f0', fg="black", font=("Helvetica", 14))
feedback_label.pack()

root.mainloop()
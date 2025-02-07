import cv2
import mediapipe as mp
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize MediaPipe Pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Counter to track how many times the image has been detected
detection_counter = 0


def detect_pose_image(image_path):
    """
    Detect pose landmarks on a selected image and count detections.
    """
    global detection_counter

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image.")
        return

    while True:
        # Convert the image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image for pose detection
        result = pose.process(rgb_image)

        # If landmarks are detected
        if result.pose_landmarks:
            detection_counter += 1
            mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            print(f"Pose Detected! Detection count: {detection_counter}")
        else:
            print("No pose detected.")

        # Display the image with landmarks
        cv2.imshow("Pose Detection - Image", image)

        # Wait for a key press to exit or allow repeated detection
        print("Press 'd' to recheck the image, 'r' to reset counter, or 'q' to quit.")
        key = cv2.waitKey(0) & 0xFF
        if key == ord('d'):  # Re-detect pose in the same image
            print("Rechecking image for pose detection...")
            continue
        elif key == ord('r'):  # Reset detection counter
            detection_counter = 0
            print("Detection counter reset.")
        elif key == ord('q'):  # Quit the loop
            print("Stopping image detection loop...")
            break

    # Close the display window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Tk().withdraw()  # Hide the main tkinter window
    print("Select an image file...")
    file_path = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    if not file_path:
        print("No file selected. Exiting.")
    else:
        print("Starting detection...")
        detect_pose_image(file_path)
        print(f"Total detections: {detection_counter}")
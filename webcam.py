import cv2
import mediapipe as mp

# Initialize MediaPipe Pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Counter to track how many times a pose has been detected
detection_counter = 0


def detect_pose_webcam():
    """
    Detect pose from the webcam feed, track detection counts, and allow user to quit with 'q'.
    """
    global detection_counter

    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    print("Press 'q' to exit, 'r' to reset the detection counter.")

    try:
        frame_skip = 2  # Process every nth frame to improve performance
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame from webcam.")
                break

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue  # Skip frames to improve performance

            # Convert the frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for pose detection
            result = pose.process(rgb_frame)

            # If landmarks are detected, draw them and increment the counter
            if result.pose_landmarks:
                detection_counter += 1
                mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                print(f"Pose Detected! Count: {detection_counter}")

            # Display the detection count on the frame
            cv2.putText(frame, f"Detections: {detection_counter}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Pose Detection - Webcam", frame)

            # Break the loop on 'q' key press or reset counter on 'r'
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Stopping webcam detection loop...")
                break
            elif key == ord('r'):
                detection_counter = 0
                print("Detection counter reset.")

    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Exiting the webcam detection loop.")
    finally:
        # Release the webcam and destroy windows
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total poses detected: {detection_counter}")


if __name__ == "__main__":
    detect_pose_webcam()
    pose.close()
    print("Program terminated gracefully.")
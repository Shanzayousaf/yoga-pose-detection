# **Yoga Pose Detection 🧘‍♀️📷**  

A real-time **Yoga Pose Detection** system using **MediaPipe, OpenCV, and Tkinter**. This project compares a user's pose with a reference image, provides feedback, and plays a beep sound if the posture needs correction.  

## **🔹 Features**  

✅ **Pose Comparison** – Detects body landmarks and compares them with a reference pose.

✅ **Real-Time Feedback** – Provides corrective feedback if posture is incorrect.  

✅ **Beep Sound Alert** – Plays a beep sound when posture deviates from the reference pose.  

✅ **Random Image Selection** – Automatically selects a new reference image after a correct pose is held for **10 seconds**.  

✅ **Adjustable Threshold** – Users can tweak the similarity threshold using a slider.  

✅ **Graphical Interface** – Built using Tkinter for ease of use.  

---

## **📂 Folder Structure**  

📦 Yoga-Pose-Detection

┣ 📂 pictures # Folder containing reference images

┣ 📜 main_ui.py # Main UI script for pose detection

┣ 📜 webcam.py # Pose detection using a webcam

┣ 📜 image.py # Pose detection in static images

┣ 📜 audio.py # Manages beep sound alerts

┣ 📜 feedback.py # Provides voice feedback on posture

┣ 📜 compare.py # Combines detection, comparison, and feedback

┣ 📜 requirements.txt # Required dependencies

┗ 📜 README.md # Project documentation


---

## **📦 Installation**  

# **1️⃣ Clone the Repository**  

git clone https://github.com/your-username/yoga-pose-detection.git  
cd yoga-pose-detection  
2️⃣ Install Dependencies
pip install -r requirements.txt  
3️⃣ Run the Program
python main_ui.py



# **🛠 Dependencies**
opencv-python
mediapipe
numpy
pygame
tkinter
Pillow


Install all dependencies using:

pip install -r requirements.txt 

# **🎯 How It Works**

Select a Reference Pose – The program loads an image from the pictures folder.
Start Webcam – The system detects your pose in real-time.
Pose Matching – If your pose matches the reference for 10 seconds, a new random image is loaded.
Feedback System – If the pose deviates, a beep sound and text feedback are provided.

# **📸 Demo**

✅ Correct Pose
❌ Incorrect Pose

# **🤝 Contribution**

Want to improve this project? Feel free to fork, star, and submit a PR!

# **📞 Contact**

If you have any questions, feel free to reach out:
📧 shanzayousaf2002@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/shanza-yousaf-a52a9a267/)

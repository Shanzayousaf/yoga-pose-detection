import pyttsx3

# Initialize the pyttsx3 engine
tts_engine = pyttsx3.init()

# Set the speech rate (optional, adjust as needed)
tts_engine.setProperty("rate", 150)

# Test the text-to-speech engine by saying a message
tts_engine.say("Testing text-to-speech engine.")
tts_engine.runAndWait()

# Print a confirmation message
print("Text-to-speech test complete!")

import subprocess
import cv2
import os

# Path to the input video file
input_video = "Flag.mp4"

# Path to the output directory to save frames
output_directory = "frames2/"
output_directory_text = "frames_with_text/"

# Create the output directories if they don't exist
os.makedirs(output_directory, exist_ok=True)
os.makedirs(output_directory_text, exist_ok=True)

# Use ffmpeg to extract frames from the video
subprocess.run(["ffmpeg", "-i", input_video, "-vf", "fps=1", f"{output_directory}frame_%d.jpg"])

# Function to check if an image contains text
def contains_text(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to binarize the image
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Check if there are contours in the image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If there are contours, there's likely text
    return len(contours) > 0

# Iterate through extracted frames and check for text
for i in range(1, 3601):  # Assuming 1 frame per second for 1 hour
    frame_path = f"{output_directory}frame_{i}.jpg"
    frame = cv2.imread(frame_path)
    if frame is not None:
        if contains_text(frame):
            print("Text detected in frame", i)
            # Save frames containing text to the output directory
            cv2.imwrite(f"{output_directory_text}frame_{i}.jpg", frame)


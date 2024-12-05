import yt_dlp as youtube_dl
import cv2
import numpy as np
import os

# Download the video using yt-dlp
def download_video(url, download_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_path, '%(id)s.%(ext)s'),
        'noplaylist': True
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return os.path.join(download_path, f"{info_dict['id']}.{info_dict['ext']}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Process the video and annotate with "night", "dawn", and "morning"
def process_and_display_video(video_path, playback_speed=0.9, scale=1.5):
    # Open video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Define video writer for output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = "output_annotated_video.mp4"
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate new dimensions for resizing
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    # Calculate delay for slowed playback
    original_delay = int(1000 / fps)  # Delay for normal playback in ms
    slowed_delay = int(original_delay / playback_speed)  # Adjust delay by speed factor

    # Initialize variables for brightness tracking
    dawn_threshold = 70  # Threshold for transition to dawn
    morning_threshold = 120  # Threshold for transition to morning

    # Process and display each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame
        frame = cv2.resize(frame, (new_width, new_height))

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate average brightness
        brightness = np.mean(gray)

        # Determine the state based on brightness
        if brightness < dawn_threshold:
            label = "Night"
            color = (0, 0, 255)  # Red
        elif dawn_threshold <= brightness < morning_threshold:
            label = "Dawn"
            color = (255, 165, 0)  # Orange
        else:
            label = "Morning"
            color = (0, 255, 0)  # Green

        # Annotate the frame with the label
        cv2.putText(frame, label, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

        # Show the frame
        cv2.imshow('Video', frame)

        # Write the annotated frame to the output video
        out.write(frame)

        # Slow down the video by increasing the delay
        if cv2.waitKey(slowed_delay) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Annotated video saved to {output_path}")

# Main function to download and process the video
def main():
    video_url = 'https://www.youtube.com/watch?v=sfPo9MHOIG0'
    download_path = 'path_to_downloaded_videos'  # Modify this to your desired download folder
    playback_speed = 0.9  # Adjust playback speed (1.0 = normal speed, <1 = slower, >1 = faster)
    scale = 2.3  # Scale factor for resizing the video (1.0 = original size, >1.0 = upscale)

    print("Downloading video...")
    video_path = download_video(video_url, download_path)

    if video_path:
        print(f"Video downloaded to {video_path}")
        process_and_display_video(video_path, playback_speed=playback_speed, scale=scale)
    else:
        print("Error: Video could not be downloaded or processed.")

if __name__ == "__main__":
    main()

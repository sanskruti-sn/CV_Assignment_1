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
            video_url = info_dict['formats'][0]['url']
            return os.path.join(download_path, f"{info_dict['id']}.{info_dict['ext']}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Process the video to count frames and categorize them into day, evening, and night
def process_video(video_path):
    # Open video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Initialize counters
    day_count = 0
    evening_count = 0
    night_count = 0

    # Define thresholds for brightness
    day_threshold = 150  # Arbitrary threshold value for "day"
    night_threshold = 50  # Arbitrary threshold value for "night"

    # Loop through video frames and classify based on brightness
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate average brightness
        brightness = np.mean(gray)

        # Categorize based on brightness
        if brightness > day_threshold:
            day_count += 1
        elif brightness < night_threshold:
            night_count += 1
        else:
            evening_count += 1

    cap.release()

    # Calculate percentages for each category
    total_frames = day_count + evening_count + night_count
    if total_frames > 0:
        day_percentage = (day_count / total_frames) * 100
        evening_percentage = (evening_count / total_frames) * 100
        night_percentage = (night_count / total_frames) * 100
    else:
        day_percentage = evening_percentage = night_percentage = 0

    return day_count, evening_count, night_count, day_percentage, evening_percentage, night_percentage

# Main function to download and process the video
def main():
    video_url = 'https://www.youtube.com/watch?v=sfPo9MHOIG0'
    download_path = 'path_to_downloaded_videos'  # Modify this to your desired download folder

    print("Downloading video...")
    video_path = download_video(video_url, download_path)

    if video_path:
        print(f"Video downloaded to {video_path}")
        day_count, evening_count, night_count, day_percentage, evening_percentage, night_percentage = process_video(video_path)

        print(f"Day Count: {day_count}")
        print(f"Evening Count: {evening_count}")
        print(f"Night Count: {night_count}")
        print(f"Day Percentage: {day_percentage:.2f}%")
        print(f"Evening Percentage: {evening_percentage:.2f}%")
        print(f"Night Percentage: {night_percentage:.2f}%")
    else:
        print("Error: Video could not be downloaded or processed.")

if __name__ == "__main__":
    main()

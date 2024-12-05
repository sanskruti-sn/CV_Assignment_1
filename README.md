Problem Statement:

The task is to analyze a video to classify frames into three distinct time-of-day categories: Day, Evening, and Night. The goal is to determine the number of frames falling into each category and compute their respective percentages. This analysis will be useful for applications like video indexing, scene detection, or event categorization based on the time of day.

Solution:

To solve this problem, we used a combination of tools and libraries:

YouTube Video Download: The video is first downloaded using the yt-dlp library.
Frame Extraction: The video is then processed using OpenCV to extract individual frames.
Time-of-Day Classification: Each frame is analyzed to classify it as a day, evening, or night frame based on its brightness or lighting conditions. The classification uses a thresholding technique where bright frames are classified as day, dark frames as night, and intermediate frames as evening.
Percentage Calculation: After classifying all frames, the total number of frames in each category is calculated along with the percentage of day, evening, and night frames.

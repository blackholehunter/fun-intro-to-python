# fun-intro-to-python
This repo contains some code and data for a fun intro to Python with a little bit of text analytics on messy data.

The main script here is soupYouTube.py, which extracts video titles from my YouTube watch history list and runs a little bit of text analytics on it to get top bigrams from the video titles to check if there is anything I watch repeatedly on YouTube. Spoiler: I do, I am obsessed with the Yuri on Ice anime, which features strongly in my watch history (over 50% of the videos are related to this anime).

First install all the required Python libraries by running pip install -r requirements.txt with the requirements.txt file provided in this repo.

In the Data folder you will find an HTML file with my YouTube watch history. Note I didn't bother including the images with this HTML file so expect the HTML file to look ugly. However, it contains all the info we need for processing.

When you run the soupYouTube.py you might get errors from the Natural Language Toolkit if you have some missing additional resources. Depending on your Python setup on your laptop, following the error message instructions might or might not work. If it doesn't, run the nltkDownload.py to get yourself the resources required for this exercise.

There is an accompanying video for this code here: https://youtu.be/H-iomo3pDbc.

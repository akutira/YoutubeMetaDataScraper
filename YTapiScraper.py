# from googleapiclient.discovery import build
# import json

# API_KEY = 'AIzaSyBl7uFVPOjSezFUjNqJhtaIRiWf5sqRQyg'  # Replace with your API key
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def get_video_details(video_id):
#     request = youtube.videos().list(
#         part='snippet,statistics',
#         id=video_id
#     )
#     response = request.execute()
#     return response['items']

# def get_comments(video_id):
#     comments = []
#     request = youtube.commentThreads().list(
#         part='snippet',
#         videoId=video_id,
#         textFormat='plainText'
#     )
#     while request:
#         response = request.execute()
#         for item in response['items']:
#             comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
#         request = youtube.commentThreads().list_next(request, response)
#     return comments

# def main(video_id):
#     video_details = get_video_details(video_id)
#     comments = get_comments(video_id)

#     # Write output to a file
#     with open('youtube_output.txt', 'w', encoding='utf-8') as f:
#         f.write("Video Details:\n")
#         for video in video_details:
#             f.write(f"Title: {video['snippet']['title']}\n")
#             f.write(f"Description: {video['snippet']['description']}\n")
#             f.write(f"Likes: {video['statistics']['likeCount']}\n")
#             f.write(f"Views: {video['statistics']['viewCount']}\n")
#             f.write('-' * 50 + '\n')
        
#         f.write("Comments:\n")
#         for comment in comments:
#             f.write(comment + '\n')
    
#     print("Scraping complete! Check 'youtube_output.txt' for the results.")

# if __name__ == "__main__":
#     # Replace 'VIDEO_ID' with the actual video ID you want to scrape
#     main('hDmfZ_UjDqM')


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time

# class YouTubeScraper:
#     def __init__(self, keywords, max_videos_per_keyword=3, output_file='output.txt'):
#         self.keywords = keywords
#         self.max_videos_per_keyword = max_videos_per_keyword
#         self.videos = []
        
#         self.output_file = output_file

#         # Configure Chrome options
#         self.options = Options()
#         self.options.add_argument("--headless")  # Run in headless mode if desired

#         # Prepare the output file (clear any previous content)
#         with open(self.output_file, 'w') as f:
#             f.write("YouTube Scraper Results\n")
#             f.write("="*30 + "\n\n")

#     def setup_driver(self):
#         # Initialize the WebDriver
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')  # run in headless mode
#         self.driver = webdriver.Chrome(options=options)

#     def fetch_videos(self, keyword):
#         # Start Chrome WebDriver and open YouTube search page for the keyword
#         search_url = f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}"
#         self.driver.get(search_url)
        
#         # Scroll to load more videos
#         scroll_count = 0
#         videos_for_keyword = []
        
#         while len(videos_for_keyword) < self.max_videos_per_keyword:
#             self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#             time.sleep(2)  # Pause to allow videos to load
            
#             # Collect video URLs
#             video_elements = self.driver.find_elements(By.XPATH, '//*[@id="video-title"]')
#             for video in video_elements:
#                 video_url = video.get_attribute("href")
#                 if video_url and video_url not in videos_for_keyword:
#                     videos_for_keyword.append(video_url)
#                     print(f"Found video for '{keyword}': {video_url}")
#                 # Stop if we have reached the maximum number of videos
#                 if len(videos_for_keyword) >= self.max_videos_per_keyword:
#                     break
#             scroll_count += 1
#             if scroll_count > 10:  # Safety break to prevent infinite scrolling
#                 print("Max scroll limit reached")
#                 break
        
#         self.videos.extend(videos_for_keyword)
#         print(f"Total videos found for '{keywords}': {len(videos_for_keyword)}")

#     def scrape_comments(self, video_url):
#         # Placeholder for comments scraping
#         comments = ["Example comment 1", "Example comment 2"]  # Dummy comments
#         with open(self.output_file, 'a') as f:
#             f.write(f"Comments for video: {video_url}\n")
#             for comment in comments:
#                 f.write(f" - {comment}\n")
#             f.write("\n")


#     def start_scraping(self):
#         # Setup the driver
#         self.setup_driver()
        
#         # Fetch videos for each keyword
#         for topic, keywords in self.keywords.items():
#             print(f"Searching for videos related to: {topic}")
#             for keyword in keywords:
#                 self.fetch_videos(keyword)
        
#         # Close the driver after collection
#         self.driver.quit()

#         # Scrape comments for each video URL collected
#         for video_url in self.videos:
#             print(f"Scraping comments for video: {video_url}")
#             self.scrape_comments(video_url)

# # Define the keywords and initialize the scraper
# keywords = {
#     'Nuclear safety': ['risk', 'dangerous', 'accident', 'radiation'],
#     'Nuclear economy': ['affordable', 'cheap', 'expensive', 'pricy'],
#     'Nuclear technology': ['fusion', 'advanced', 'future', 'SMR'],
#     'Nuclear waste': ['radiotoxic', 'disposal', 'spent-fuel', 'contamination'],
#     'Nuclear energy': ['green', 'carbon-free', 'eco-friendly']
# }

# scraper = YouTubeScraper(keywords, max_videos_per_keyword=5)
# scraper.start_scraping()


#make it a class, figure out the optimal keyword combination, how many calls you hae to make every 10/20/30 mins


import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
from threading import Timer

class YouTubeScraper:
    """
    Class to cal 
    api_key: 
    """
    def __init__(self, api_key, channel_url, max_videos=10, max_comments=10, interval=30):
        self.api_key = api_key
        self.channel_url = channel_url
        self.max_videos = max_videos
        self.max_comments = max_comments
        self.interval = interval
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_used = 0
        self.setup_browser()

    def setup_browser(self):
        """Initialize the Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # run in headless mode
        self.driver = webdriver.Chrome(options=options)

    def scroll_and_collect_video_ids(self):
        """Scroll through the channel page and collect video IDs."""
        self.driver.get(self.channel_url)
        time.sleep(2)  # Wait for page load
        video_ids = set()
        
        while len(video_ids) < self.max_videos:
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)  # Wait for new videos to load

            videos = self.driver.find_elements(By.CSS_SELECTOR, 'a#video-title')
            for video in videos:
                video_url = video.get_attribute('href')
                if video_url:
                    video_id = re.search(r"v=([^&]+)", video_url)
                    if video_id:
                        video_ids.add(video_id.group(1))

            if len(video_ids) >= self.max_videos:
                break
        
        return list(video_ids)

    def fetch_video_metadata(self, video_id):
        """Fetch metadata for a single video."""
        request = self.youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()
        self.quota_used += 5  # Each video metadata call costs 5 units
        
        if "items" in response and len(response["items"]) > 0:
            video_data = response["items"][0]
            metadata = {
                "title": video_data["snippet"]["title"],
                "description": video_data["snippet"]["description"],
                "published_at": video_data["snippet"]["publishedAt"],
                "channel_title": video_data["snippet"]["channelTitle"],
                "tags": video_data["snippet"].get("tags", []),
                "view_count": video_data["statistics"].get("viewCount"),
                "like_count": video_data["statistics"].get("likeCount"),
                "comment_count": video_data["statistics"].get("commentCount"),
                "duration": video_data["contentDetails"]["duration"]
            }
            return metadata
        return {}

    def fetch_comments(self, video_id):
        """Fetch comments for a video."""
        comments = []
        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=self.max_comments
        )
        response = request.execute()
        self.quota_used += 1 

        for item in response.get("items", []):
            comment_data = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment_data["authorDisplayName"],
                "author_channel_id": comment_data["authorChannelId"].get("value"),
                "text": comment_data["textDisplay"],
                "published_at": comment_data["publishedAt"],
                "like_count": comment_data["likeCount"]
            })
        
        return comments

    def scrape(self):
        """Main method to scrape videos and comments."""
        video_ids = self.scroll_and_collect_video_ids()
        print(f"Collected {len(video_ids)} video IDs from the channel.")
        
        all_data = []
        for video_id in video_ids:
            print(f"Fetching data for video ID: {video_id}")
            metadata = self.fetch_video_metadata(video_id)
            comments = self.fetch_comments(video_id)
            video_data = {
                "video_id": video_id,
                "metadata": metadata,
                "comments": comments
            }
            all_data.append(video_data)
        
        # Save data to JSON
        with open("youtube_scraper_output.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print("Data saved to youtube_scraper_output.json")

    def schedule_scraping(self):
        """Schedules scraping at regular intervals."""
        self.scrape()
        print(f"Quota used so far: {self.quota_used} units.")
        
        if self.quota_used < 10000:  # Check if within quota
            Timer(self.interval * 60, self.schedule_scraping).start()
        else:
            print("Quota limit reached. Pausing further scraping.")

    def close_browser(self):
        """Close the Selenium WebDriver."""
        self.driver.quit()

if __name__ == "__main__":
    api_key = 'AIzaSyBl7uFVPOjSezFUjNqJhtaIRiWf5sqRQyg'
    channel_url = 'https://www.youtube.com/@kurzgesagt'
    
    scraper = YouTubeScraper(api_key=api_key, channel_url=channel_url, max_videos=5, max_comments=10, interval=30)
    try:
        scraper.schedule_scraping()  # Begin scheduled scraping
    finally:
        scraper.close_browser()  # Ensure browser is closed after use


#main block, merge in one main file, in harmonious way
# one main script, be able to get posts n such from all different platforms under one pipeline
# start my mine to design the github, make them submit a push
# continue on the storage and save file like .csv files. 
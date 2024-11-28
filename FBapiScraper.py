import requests
import time

# class FacebookScraper:
#     def __init__(self, access_token, base_url="https://graph.facebook.com/v17.0/"):
#         self.access_token = access_token
#         self.base_url = base_url
    
#     def get_facebook_posts(self, page_id, limit=10):
#         url = f"{self.base_url}{page_id}/posts"
#         params = {
#             'access_token': self.access_token,
#             'limit': limit
#         }
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json().get('data', [])
#         else:
#             print(f"Error: {response.status_code}")
#             return None

#     def get_facebook_comments(self, post_id, limit=10):
#         url = f"{self.base_url}{post_id}/comments"
#         params = {
#             'access_token': self.access_token,
#             'limit': limit
#         }
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json().get('data', [])
#         else:
#             print(f"Error: {response.status_code}")
#             return None

# # Example usage
# if __name__ == "__main__":
#     ACCESS_TOKEN = 'YOUR_FACEBOOK_ACCESS_TOKEN'
#     PAGE_ID = 'facebook_page_id_or_user_id'  # Replace with actual Page ID or User ID

#     scraper = FacebookScraper(access_token=ACCESS_TOKEN)

#     # Get posts from the page
#     posts = scraper.get_facebook_posts(PAGE_ID, limit=5)
#     if posts:
#         for post in posts:
#             post_id = post['id']
#             post_message = post.get('message', 'No content')
#             print(f"Post: {post_message}")
            
#             # Get comments for each post
#             comments = scraper.get_facebook_comments(post_id, limit=3)
#             if comments:
#                 for comment in comments:
#                     comment_message = comment.get('message', 'No comment')
#                     print(f"  Comment: {comment_message}")
 

# if __name__ == "__main__":
#     ACCESS_TOKEN = 'YOUR_FACEBOOK_ACCESS_TOKEN'
#     PAGE_ID = 'facebook_page_id_or_user_id'

#     scraper = FacebookScraper(access_token=ACCESS_TOKEN)
    
#     while True:
#         print("Fetching posts...")
#         posts = scraper.get_facebook_posts(PAGE_ID, limit=5)
#         if posts:
#             for post in posts:
#                 post_id = post['id']
#                 post_message = post.get('message', 'No content')
#                 print(f"Post: {post_message}")

#                 # Fetch comments for each post
#                 comments = scraper.get_facebook_comments(post_id, limit=3)
#                 if comments:
#                     for comment in comments:
#                         comment_message = comment.get('message', 'No comment')
#                         print(f"  Comment: {comment_message}")
#         print("Waiting 1 minute before fetching again...")
#         time.sleep(60)


from facebook_scraper import get_posts

def scrape_facebook_posts(page_name, max_posts=10):
    try:
        # Open a file to write the output
        with open('facebook_posts_output.txt', 'w', encoding='utf-8') as f:
            # Scrape posts, increasing 'pages' argument for more posts
            post_count = 0
            for post in get_posts(page_name, pages=5):
                # If no posts are fetched, print and break the loop
                if not post['text']:
                    print("No posts found.")
                    break
                
                # Write the scraped post details to the file
                f.write(f"Post ID: {post['post_id']}\n")
                f.write(f"Post Text: {post['text']}\n")
                f.write(f"Post Time: {post['time']}\n")
                f.write(f"Likes: {post['likes']}\n")
                f.write(f"Comments: {post['comments']}\n")
                f.write(f"Shares: {post['shares']}\n")
                f.write('-' * 50 + '\n')  # Separate posts with dashes

                # Print to console for debugging
                print(f"Post {post_count+1}: {post['post_id']} - {post['text'][:50]}...")

                # Increment post count and check if max_posts limit is reached
                post_count += 1
                if post_count >= max_posts:
                    break

            # Check if no posts were scraped at all
            if post_count == 0:
                print("No posts scraped from the page.")
                
        print("Scraping complete! Check 'facebook_posts_output.txt' for the results.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrape_facebook_posts('nytimes', max_posts=5)




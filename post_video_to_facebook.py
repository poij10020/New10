import requests
import pandas as pd
import os

# Facebook API credentials
page_access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
page_id = os.getenv('FACEBOOK_PAGE_ID')

def post_video_to_facebook(video_url):
    url = f"https://graph.facebook.com/{page_id}/videos"
    video_file = requests.get(video_url, stream=True)
    
    if video_file.status_code == 200:
        files = {'source': video_file.raw}
        payload = {
            'access_token': page_access_token,
            'description': 'Automatically posted video'
        }
        response = requests.post(url, data=payload, files=files)
        return response.json()
    else:
        return {'error': 'Failed to download video'}

def schedule_posts():
    # Path to CSV file
    video_urls_path = 'video_urls.csv'
    
    # Read video URLs from CSV
    video_urls_df = pd.read_csv(video_urls_path)
    video_urls = video_urls_df['Video_URL']

    for video_url in video_urls:
        # Post video to Facebook
        response = post_video_to_facebook(video_url)
        print(f"Posted video URL: {video_url}")
        print(f"Response: {response}")

if __name__ == "__main__":
    schedule_posts()

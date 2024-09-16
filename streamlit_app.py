import requests
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
from io import BytesIO

# Function to extract image URLs from a webpage
def extract_image_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error(f"Error fetching page: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')
        image_urls = [img['src'] for img in images if 'src' in img.attrs]
        return image_urls

    except Exception as e:
        st.error(f"Error parsing the page: {e}")
        return []

# Function to download and display the image
def download_and_display_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        st.image(img)
    except Exception as e:
        st.error(f"Failed to download or display image: {e}")

# Streamlit App
st.title("Image Extractor and Viewer")

page_url = st.text_input("Enter the URL of the webpage:")

if st.button("Extract Images"):
    if page_url:
        image_urls = extract_image_urls(page_url)
        if image_urls:
            for img_url in image_urls:
                st.write(f"Image URL: {img_url}")
                download_and_display_image(img_url)
        else:
            st.write("No images found.")

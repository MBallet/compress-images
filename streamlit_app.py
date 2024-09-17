import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

# Function to download image from URL
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img, url
        else:
            st.error(f"Failed to download image from {url}. Status code: {response.status_code}")
            return None, None
    except Exception as e:
        st.error(f"Error downloading image from {url}: {e}")
        return None, None

# Function to extract filename from URL
def get_filename_from_url(url):
    filename = os.path.basename(url.split("?")[0])  # Removes any query parameters and extracts the filename
    return filename if filename else "image"

# Function to compress image
def compress_image(image, quality=50):
    img_format = image.format if image.format else "JPEG"
    img_bytes = BytesIO()
    image.save(img_bytes, format=img_format, optimize=True, quality=quality)
    img_bytes.seek(0)
    return img_bytes

# Initialize session state for storing images and filenames
if "images" not in st.session_state:
    st.session_state.images = []
if "filenames" not in st.session_state:
    st.session_state.filenames = []

# Streamlit app layout
st.title("Image Downloader and Compressor from URLs")

# Text input for image URLs
image_urls_input = st.text_area("Enter the image URLs (one per line):")

# Slider for compression quality
compression_quality = st.slider("Select compression quality (higher means better quality but larger file size)", 10, 95, 85)

# Button to trigger the image download and compression
if st.button("Download Images"):
    if image_urls_input:
        # Split the URLs into a list
        image_urls = image_urls_input.split("\n")
        image_urls = [url.strip() for url in image_urls if url.strip()]  # Clean up the list
        
        # Clear session state to avoid duplicates on multiple downloads
        st.session_state.images = []
        st.session_state.filenames = []
        
        # Download and display each image
        for idx, url in enumerate(image_urls):
            img, original_url = download_image(url)
            if img:
                # Display the image
                st.image(img, caption=f"Image {idx + 1}", use_column_width=True)
                
                # Extract original filename
                original_filename = get_filename_from_url(original_url)
                img_format = img.format.lower() if img.format else "jpeg"
                file_extension = os.path.splitext(original_filename)[1] or f".{img_format}"
                full_filename = original_filename if file_extension else f"{original_filename}.{img_format}"

                # Store the original image and its filename in session state
                st.session_state.images.append({
                    "original": img,
                    "compressed": compress_image(img, quality=compression_quality),
                    "filename": full_filename,
                    "format": img_format
                })
    else:
        st.error("Please enter at least one image URL.")

# If images are stored in session state, display download buttons
if st.session_state.images:
    for idx, image_data in enumerate(st.session_state.images):
        original_img = image_data["original"]
        compressed_img_bytes = image_data["compressed"]
        original_filename = image_data["filename"]
        img_format = image_data["format"]

        # Provide a download button for the original image
        st.download_button(
            label=f"Download {original_filename}",
            data=BytesIO(original_img.tobytes()),
            file_name=original_filename,
            mime=f"image/{img_format}"
        )

        # Provide a download button for the compressed image
        compressed_filename = f"compressed_{original_filename}"
        st.download_button(
            label=f"Download Compressed {compressed_filename}",
            data=compressed_img_bytes,
            file_name=compressed_filename,
            mime=f"image/{img_format}"
        )

import streamlit as st
import tinify
import os
import zipfile
import io

# Set your Tinify API key
tinify.key = 'kW1hRH2j31ndX4d6CY0bMmRdrgsn32Gn'  # Replace with your actual API key

st.title('Image Compressor using Tinify API')
st.write('Upload image(s) to compress them using the Tinify API.')

# File uploader allows multiple files
uploaded_files = st.file_uploader(
    "Choose image(s)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    compressed_files = []  # List to store compressed file info
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        try:
            # Compress the image using Tinify API
            source = tinify.from_buffer(file_bytes)
            compressed_data = source.to_buffer()
            
            # Add compressed data to the list
            compressed_files.append((filename, compressed_data))
            st.success(f'Compressed {filename}')
        except tinify.Error as e:
            st.error(f'An error occurred while compressing {filename}: {e}')
    
    if compressed_files:
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, data in compressed_files:
                zip_file.writestr(filename, data)
        zip_buffer.seek(0)
        
        # Provide a download button for the zip file
        st.download_button(
            label="Download All Compressed Images",
            data=zip_buffer,
            file_name="compressed_images.zip",
            mime="application/zip"
        )
else:
    st.info('Please upload at least one image file.')

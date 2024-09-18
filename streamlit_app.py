import streamlit as st
import tinify
import os

# Set your Tinify API key
tinify.key = 'kW1hRH2j31ndX4d6CY0bMmRdrgsn32Gn'  # Replace with your actual API key

st.title('Image Compressor')
st.write('Upload image(s) to compress them using the Tinify API.')

# File uploader allows multiple files
uploaded_files = st.file_uploader(
    "Choose image(s)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    output_dir = 'compressed_images'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        try:
            # Compress the image using Tinify API
            source = tinify.from_buffer(file_bytes)
            compressed_data = source.to_buffer()
            
            # Save the compressed image
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as out_file:
                out_file.write(compressed_data)
            
            st.success(f'Compressed and saved {filename} to {output_path}')
            
            # Provide a download button for the compressed image
            st.download_button(
                label=f"Download {filename}",
                data=compressed_data,
                file_name=filename,
                mime='image/png' if filename.endswith('.png') else 'image/jpeg'
            )
        except tinify.Error as e:
            st.error(f'An error occurred while compressing {filename}: {e}')
else:
    st.info('Please upload at least one image file.')

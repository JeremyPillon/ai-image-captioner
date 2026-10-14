"""Pennywise LensText AI - Streamlit Cloud Web Interface."""

from io import BytesIO
import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from PIL import Image
import requests
import streamlit as st
from transformers import AutoProcessor, BlipForConditionalGeneration

# Page Configuration
st.set_page_config(
    page_title="Pennywise LensText AI",
    page_icon="🖼️",
    layout="wide",
)

LOGO_PATH = "icon.png"
if not os.path.exists(LOGO_PATH) and os.path.exists("assets/icon.png"):
    LOGO_PATH = "assets/icon.png"

# Model Caching for Fast Cloud Performance
@st.cache_resource
def load_blip_model():
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_blip_model()

def generate_caption(image: Image.Image) -> str:
    raw_image = image.convert("RGB")
    inputs = processor(images=raw_image, text="a photo of", return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)
    return processor.decode(out[0], skip_special_tokens=True).strip()

# Header
col1, col2 = st.columns([1, 8])
with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=64)
    else:
        st.write("🖼️")
with col2:
    st.title("Pennywise LensText AI")
    st.caption("Automated alt-text generation to enhance publishing workflows, accessibility, and SEO.")

tab1, tab2 = st.tabs(["Single Photo Parsing", "Batch Web Extractor"])

with tab1:
    st.subheader("Upload Photo or Use Camera")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
    camera_file = st.camera_input("Or take a photo")
    
    input_img = uploaded_file or camera_file
    if input_img:
        image = Image.open(input_img)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Caption", type="primary"):
            with st.spinner("Generating alt text..."):
                caption = generate_caption(image)
                st.text_area("Generated Alt Text", value=caption, height=100)

with tab2:
    st.subheader("Scrape & Caption Webpage Images")
    target_url = st.text_input("Target Web URL", placeholder="https://en.wikipedia.org/wiki/IBM")
    if st.button("Extract & Process Images", type="primary"):
        if target_url:
            st.info("Scraping webpage images...")
            # Add scraping logic here
        else:
            st.error("Please enter a valid URL.")
            
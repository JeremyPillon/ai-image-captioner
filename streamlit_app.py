"""Pennywise LensText AI Suite - Streamlit Web Application."""

from io import BytesIO
import logging
import os
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from PIL import Image
import requests
import streamlit as st
from transformers import AutoProcessor, BlipForConditionalGeneration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "Salesforce/blip-image-captioning-base"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AssetCaptioner/1.0"
REQUEST_TIMEOUT = 10  # Seconds
MIN_IMAGE_PIXELS = 200

# Logo Path Discovery
LOGO_PATH = "icon.png"
if not os.path.exists(LOGO_PATH) and os.path.exists("assets/icon.png"):
    LOGO_PATH = "assets/icon.png"

# Streamlit Page Setup
st.set_page_config(
    page_title="Pennywise LensText AI",
    page_icon="🖼️",
    layout="wide",
)


@st.cache_resource
def load_blip_model():
    """Loads and caches the BLIP processor and model in cloud memory."""
    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    return processor, model


processor, model = load_blip_model()


def process_pil_image(image: Image.Image, prompt: str = "a photo of") -> str:
    """Processes a PIL image through BLIP and returns a caption string."""
    raw_image = image.convert("RGB")
    inputs = processor(images=raw_image, text=prompt, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)
    caption: str = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip()


def validate_url(url: str) -> bool:
    """Validates HTTP/HTTPS URL scheme."""
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def scrape_and_caption_url(target_url: str) -> Tuple[str, Optional[str]]:
    """Scrapes web images, generates captions, and creates downloadable log text."""
    if not validate_url(target_url):
        return (
            "Error: Invalid URL. Provide a valid 'http://' or 'https://' address.",
            None,
        )

    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(
            target_url, headers=headers, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
    except requests.RequestException as err:
        logger.error("HTTP request failed for %s: %s", target_url, err)
        return f"Failed to fetch webpage: {str(err)}", None

    soup = BeautifulSoup(response.text, "html.parser")
    img_elements = soup.find_all("img")

    if not img_elements:
        return "No <img> tags found on the target webpage.", None

    caption_results: List[str] = []
    output_filename = "webpage_captions.txt"

    with open(output_filename, "w", encoding="utf-8") as caption_file:
        for idx, img_element in enumerate(img_elements, start=1):
            img_src = img_element.get("src") or img_element.get("data-src")
            if not img_src and img_element.has_attr("srcset"):
                img_src = img_element["srcset"].split()[0]

            if not img_src or ".svg" in img_src.lower():
                continue

            full_img_url = urljoin(target_url, img_src)

            try:
                img_response = requests.get(
                    full_img_url, headers=headers, timeout=REQUEST_TIMEOUT
                )
                img_response.raise_for_status()
                raw_image = Image.open(BytesIO(img_response.content))

                width, height = raw_image.size
                if width * height < MIN_IMAGE_PIXELS:
                    continue

                caption = process_pil_image(raw_image, prompt="a photo of")
                log_entry = f"[{idx}] {full_img_url}\nCaption: {caption}\n\n"

                caption_results.append(log_entry)
                caption_file.write(log_entry)

            except (requests.RequestException, OSError) as err:
                logger.warning("Skipped image %s: %s", full_img_url, err)
                continue

    if not caption_results:
        return "Found image tags, but could not process valid photos.", None

    return "".join(caption_results), output_filename


# Interface Layout
header_col1, header_col2 = st.columns([1, 8])
with header_col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=64)
    else:
        st.markdown("## 🖼️")

with header_col2:
    st.title("Pennywise LensText AI")
    st.caption(
        "Automated alt-text generation to enhance publishing workflows, "
        "accessibility (WCAG compliance), and SEO."
    )

tab1, tab2 = st.tabs(["Single Photo Parsing", "Batch Web Extractor"])

with tab1:
    st.subheader("Upload Photo or Use Camera")
    uploaded_file = st.file_uploader(
        "Choose an image file...", type=["jpg", "jpeg", "png", "webp"]
    )
    camera_file = st.camera_input("Or take a live photo")

    selected_image = uploaded_file or camera_file

    if selected_image:
        image = Image.open(selected_image)
        st.image(image, caption="Input Image", use_column_width=True)

        if st.button("Generate Caption", type="primary", key="single_btn"):
            with st.spinner("Generating alt text..."):
                caption_text = process_pil_image(image)
                st.text_area(
                    "Generated Alt Text",
                    value=caption_text,
                    height=120,
                )

with tab2:
    st.subheader("Scrape & Caption Webpage Images")
    target_url = st.text_input(
        "Target Web URL",
        placeholder="https://en.wikipedia.org/wiki/IBM",
    )

    if st.button("Extract & Process Images", type="primary", key="batch_btn"):
        if target_url:
            with st.spinner("Scraping webpage and parsing images..."):
                log_content, file_path = scrape_and_caption_url(target_url)

                st.text_area(
                    "Extraction Log",
                    value=log_content,
                    height=250,
                )

                if file_path and os.path.exists(file_path):
                    with open(file_path, "rb") as download_file:
                        st.download_button(
                            label="Download Scraped Captions (.txt)",
                            data=download_file,
                            file_name="webpage_captions.txt",
                            mime="text/plain",
                        )
        else:
            st.warning("Please enter a valid URL first.")
            
"""Pennywise LensText AI Suite.

Provides local drag-and-drop image captioning, live webcam capture, and web scraping capabilities
using Hugging Face BLIP and Gradio built-in themes.
"""

from io import BytesIO
import logging
import os
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import gradio as gr
import numpy as np
from PIL import Image
import requests
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

# Global Model & Processor Initialization
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)


def process_pil_image(image: Image.Image, prompt: str = "a photo of") -> str:
    """Processes a PIL image through BLIP and returns a caption string."""
    raw_image = image.convert("RGB")
    inputs = processor(images=raw_image, text=prompt, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)
    caption: str = processor.decode(out[0], skip_special_tokens=True)
    return caption.strip()


def caption_single_image(input_image: np.ndarray | None) -> str:
    """Gradio handler for single image uploads and webcam captures."""
    if input_image is None:
        return "Error: Please upload or capture an image first."

    try:
        raw_image = Image.fromarray(input_image)
        return process_pil_image(raw_image)
    except Exception as err:
        logger.error("Error processing local image: %s", err)
        return f"Error processing image: {str(err)}"


def validate_url(url: str) -> bool:
    """Validates HTTP/HTTPS URL scheme."""
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def scrape_and_caption_url(target_url: str) -> tuple[str, str | None]:
    """Scrapes web images, generates captions, and outputs a downloadable text file."""
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

    caption_results: list[str] = []
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


def build_interface() -> gr.Blocks:
    """Constructs the Gradio interface using native high-contrast themes."""
    # Native Slate Theme handles WCAG contrast automatically
    theme = gr.themes.Soft(
        primary_hue="orange",
        neutral_hue="slate",
    )

    with gr.Blocks(title="Pennywise LensText AI", theme=theme) as app:

        # Header Row with Logo
        with gr.Row():
            if os.path.exists(LOGO_PATH):
                gr.Image(
                    value=LOGO_PATH,
                    show_label=False,
                    container=False,
                    width=64,
                    height=64,
                    interactive=False,
                )
            else:
                gr.Markdown("## 🖼️")

            with gr.Column(scale=8):
                gr.Markdown("# Pennywise LensText AI")
                gr.Markdown(
                    "Automated alt-text generation to enhance publishing workflows, "
                    "accessibility (WCAG compliance), and SEO."
                )

        with gr.Tab("Single Photo Parsing"):
            gr.Markdown("### Upload Photo or Use Webcam")
            with gr.Row():
                img_input = gr.Image(
                    type="numpy",
                    label="Input Image",
                    sources=["upload", "webcam", "clipboard"],
                )
                caption_output = gr.Textbox(
                    label="Generated Alt Text",
                    lines=4,
                    interactive=False,
                )
            submit_btn = gr.Button("Generate Caption", variant="primary")
            submit_btn.click(
                fn=caption_single_image,
                inputs=img_input,
                outputs=caption_output,
            )

        with gr.Tab("Batch Web Extractor"):
            gr.Markdown("### Scrape & Caption Webpage Images")
            url_input = gr.Textbox(
                label="Target Web URL",
                placeholder="https://en.wikipedia.org/wiki/IBM",
            )
            scrape_btn = gr.Button(
                "Extract & Process Images", variant="primary"
            )
            scrape_text_out = gr.Textbox(
                label="Extraction Log",
                lines=10,
                interactive=False,
            )
            file_download_out = gr.File(
                label="Download Scraped Captions (.txt)",
            )

            scrape_btn.click(
                fn=scrape_and_caption_url,
                inputs=url_input,
                outputs=[scrape_text_out, file_download_out],
            )

    return app


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
    
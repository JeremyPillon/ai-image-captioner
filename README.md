# Pennywise LensText AI 🖼️✨

An accessible (WCAG AAA compliant), high-contrast AI image captioning and alt-text generation suite. Designed to streamline digital publishing, web accessibility workflows, and automated SEO image indexing using Hugging Face BLIP and Gradio.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-5.0+-orange.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-BLIP-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌟 Key Features

- **Single Photo Parsing:** Drag-and-drop file upload, live webcam capture, or clipboard pasting with automated BLIP caption generation.
- **Batch Web Extractor:** Automated web scraper using BeautifulSoup4 to extract all images from a web URL, auto-generate captions, and display a downloadable log file (`webpage_captions.txt`).
- **WCAG AAA Accessibility:** High-contrast Navy/Slate theme (`#1e293b`) with clear typography, accessible tab navigation, and optimized readability across input/output components.
- **Local Brand Integration:** Configurable logo display (`icon.png`) with automatic fallbacks for open-source distributions.

---

## 🛠️ Tech Stack

- **Framework:** Python 3.11+, Gradio
- **AI Model:** `Salesforce/blip-image-captioning-base` (PyTorch & Hugging Face Transformers)
- **Web Scraping:** BeautifulSoup4, Requests
- **Image Processing:** Pillow (PIL)

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.11 or higher installed on your system.

### 2. Installation & Setup
Bash
pip install -r requirements.txt

3. Running the App locally
Start the Gradio application:
Bash
python app.py

Open your browser and navigate to http://127.0.0.1:7860.

📁 Repository Structure
Plaintext
ai-image-captioner/
├── app.py              # Main Gradio application code
├── requirements.txt    # Python dependencies
├── icon.png            # App header logo icon
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules for venv & cache

📜 License
This project is open-source and available under the MIT License.

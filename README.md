# Pennywise LensText AI 🖼️✨

An accessible (WCAG AAA compliant), high-contrast AI image captioning and alt-text generation suite. Designed to streamline digital publishing, web accessibility workflows, and automated SEO image indexing using Hugging Face BLIP.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B.svg)
![Gradio](https://img.shields.io/badge/Gradio-Local%20Suite-orange.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-BLIP-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

🌐 **Live Web Application:** https://pennywise-lens2text-ai.streamlit.app/

---

## 🚀 Two Ways to Run

This repository supports both zero-install web usage and local execution:

1. **Live Cloud App (Streamlit Interface):** Access the web app instantly via [Streamlit Cloud](https://pennywise-lens2text-ai.streamlit.app/). Powered by `streamlit_app.py`.
2. **Local Studio Suite (Gradio Interface):** Run the standalone desktop UI locally with native webcam, clipboard, and WCAG AAA styling controls. Powered by `app.py`.

---

## 🛠️ Local Installation & Setup

### 1. Clone the Repository
git clone [https://github.com/JeremyPillon/ai-image-captioner.git](https://github.com/JeremyPillon/ai-image-captioner.git)
cd ai-image-captioner

### 2. Set Up Virtual Environment
On Windows:
python -m venv venv
.\venv\Scripts\activate

On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Choose Your Interface to Launch

* **Option A: Launch Local Gradio Studio (Desktop/Local Mode)**
  python app.py
  (Opens locally at [http://127.0.0.1:7860](http://127.0.0.1:7860))

* **Option B: Launch Local Streamlit Web UI**
  streamlit run streamlit_app.py
  (Opens locally at http://localhost:8501)

---

## 📁 Repository Structure

* `app.py` - Local Gradio application with WCAG AAA custom theme
* `streamlit_app.py` - Streamlit Cloud entrypoint for the live web application
* `requirements.txt` - Shared Python dependencies
* `icon.png` - App header branding asset
* `README.md` - Project documentation
* `.gitignore` - Version control ignore rules

---

## 📜 License

This project is open-source and available under the MIT License.

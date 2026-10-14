---
title: Pennywise LensText AI
emoji: 🖼️
colorFrom: gray
colorTo: black
sdk: gradio
sdk_version: 4.35.0
app_file: app.py
pinned: false
license: mit
---

# 🖼️ Pennywise LensText AI

An automated, enterprise-grade AI image captioning and alt-text generation engine designed for digital publishing, news media, and e-commerce platforms.

Built on **Salesforce BLIP (Bootstrapping Language-Image Pre-training)** and **Gradio**, this tool streamlines editorial workflows, accelerates search engine optimization (SEO), and ensures full **WCAG 2.1 accessibility compliance**.

---

## 🌟 Key Features

- **Single Photo Drag & Drop:** Local image upload for instant, precise alt-text creation.
- **Batch Web Scraping & Captioning:** Extract and caption images from any target webpage URL in a single pass.
- **Downloadable Logs:** Automatically generates a `.txt` file containing image URLs and generated captions for easy editorial review.
- **Custom Minimalist UI:** Styled with a clean, high-contrast dark theme.
- **Enterprise Ready:** Fully type-hinted, PEP 8 compliant, and containerized for cloud or Kubernetes deployment.

---

## 📐 System Architecture

```text
[ Target Web Page / Local Image ]
               │
               ▼
   [ BeautifulSoup4 / PIL ]
               │
               ▼
 [ BLIP Vision Transformer Model ]
               │
               ▼
  [ Generated Alt Text & Caption ]
               │
  ┌────────────┴────────────┐
  ▼                         ▼
[ Web UI ]       [ Downloadable Report (.txt) ]

1. Web Accessibility (WCAG 2.1)
Screen readers rely on descriptive alt text to assist visually impaired readers. Pennywise LensText AI automates this process to ensure online media meets global accessibility standards.

2. Search Engine Optimization (SEO)
Search engine crawlers index image alt attributes to rank visual content. Automated keyword-rich captioning helps drive organic search traffic to web articles and media catalogs.

🛠️ Local Installation & Development
Prerequisites
Python 3.10+

Virtual environment (venv)

Setup Instructions
# Clone the repository
git clone [https://github.com/JeremyPillon/ai-image-captioner.git](https://github.com/JeremyPillon/ai-image-captioner.git)
cd ai-image-captioner

# Create and activate virtual environment
# On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows (Command Prompt / PowerShell):
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch application
python app.py

Access the local web interface at http://127.0.0.1:7860.

🧪 Code Quality & Testing
This project adheres to PEP 8 standard conventions and includes automated unit tests.
# Run linter and code formatter
flake8 app.py
black app.py

# Run unit tests
pytest
👤 Author
Jeremy Pillon

Founder & Product Architect | Pennywise 2.0[cite: 1, 2]

GitHub: github.com/JeremyPillon[cite: 1]

LinkedIn: linkedin.com/in/jeremy-pillon-a407b520[cite: 1]

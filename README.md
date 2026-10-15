Pennywise LensText AI 🖼️✨
An accessible (WCAG AAA compliant), high-contrast AI image captioning and alt-text generation suite. Designed to streamline digital publishing, web accessibility workflows, and automated SEO image indexing using Hugging Face BLIP.

🌐 Live Streamlit App: https://pennywise-lens2text-ai.streamlit.app/

🚀 Live Enterprise Kubernetes App: https://pennywise-lens2text-ai.2fzp01bj017h.ca-tor.codeengine.appdomain.cloud

🚧 Work in Progress: This project is actively under development! Check back regularly or ⭐ Star / Follow this repository to stay updated on upcoming feature releases.

🚀 Enterprise Deployment Options
This application is built for multi-cloud and containerized deployment models:

Kubernetes Serverless (IBM Cloud Code Engine): Containerized deployment running on managed Kubernetes infrastructure. Pulled directly from IBM Container Registry (ca.icr.io) with automated scaling and secret management.

Streamlit Community Cloud: Zero-install web application running directly off the production repository branch (streamlit_app.py).

Local Desktop Studio (Gradio Interface): Standalone local desktop UI running app.py with custom high-contrast WCAG AAA styling controls.

🛠️ Local Installation & Running with Docker
Run via Local Python Environment
git clone [https://github.com/JeremyPillon/ai-image-captioner.git](https://github.com/JeremyPillon/ai-image-captioner.git)

cd ai-image-captioner

python -m venv venv

.\venv\Scripts\activate (On macOS/Linux: source venv/bin/activate)

pip install -r requirements.txt

python app.py

Run via Docker Container
docker build -t pennywise-lenstext-ai:v1 .

docker run -p 8080:8080 pennywise-lenstext-ai:v1

🗺️ Product Roadmap & Upcoming Features
⚡ Enter Key Auto-Submission: Instant caption generation upon pressing Enter in input fields.

📁 Bulk Local Directory Ingestion: Multi-image file uploads and direct local directory path scanning.

💾 Universal Export Options: Direct file downloads for generated captions across both single and batch modes.

📸 Continuous Accumulation Capture: Sequential webcam/photo accumulation log that preserves captures until explicitly cleared.

🧹 Workspace Clear Controls: One-click workspace reset and clear controls.

📁 Repository Structure
Dockerfile - Multi-stage container build with pre-baked BLIP model weights

.dockerignore - Excludes virtual environments and build cache from image layers

app.py - Local Gradio application (WCAG AAA custom theme)

streamlit_app.py - Streamlit Cloud and IBM Code Engine Kubernetes entry point

requirements.txt - Shared Python dependencies

icon.png - Header branding asset

README.md - Project documentation

📜 License
This project is open-source and available under the MIT License.

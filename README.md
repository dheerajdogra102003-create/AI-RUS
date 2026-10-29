# AI-RUS — AI-Powered Report Understanding System

AI-RUS is a Python-based application that combines Optical Character Recognition (OCR) with Generative AI to extract text from documents and help transform unstructured information into readable reports.

🌐 **Live Application:** [Try AI-RUS](https://ai-rus.streamlit.app/)

📂 **Source Code:** [GitHub Repository](https://github.com/dheerajdogra102003-create/AI-RUS)

## ✨ Features

- **Document ingestion:** Accepts supported document and image inputs through the application.
- **OCR-based text extraction:** Integrates EasyOCR and PaddleOCR to extract text from visual documents.
- **PDF processing:** Includes a dedicated PDF-reading module.
- **AI-powered report generation:** Uses a language-model integration to help generate structured reports from extracted information.
- **Interactive web interface:** Built with Streamlit for browser-based use.
- **Modular architecture:** Separates document ingestion, OCR processing, and AI report generation into dedicated modules.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| EasyOCR | Optical character recognition |
| PaddleOCR | OCR and text extraction |
| OpenCV | Image-processing support |
| PyMuPDF | PDF processing |
| Pillow | Image handling |
| NumPy and Pandas | Data processing |
| Google Gen AI SDK | Generative AI integration |
| python-dotenv | Environment-variable management |

## 🏗️ Project Structure

```text
AI-RUS/
├── App/
│   └── app.py
├── Fileingest/
│   ├── __init__.py
│   └── ingest.py
├── FileReader/
│   ├── image_scanner.py
│   └── pdf_reader.py
├── llm/
│   ├── __init__.py
│   └── llm.py
├── requirements.txt
├── packages.txt
├── README.md
└── .gitignore
```

### Module Overview

- **`App/app.py`** — Streamlit application entry point and user interface.
- **`Fileingest/ingest.py`** — Handles document input and ingestion.
- **`FileReader/image_scanner.py`** — Supports image text extraction using OCR.
- **`FileReader/pdf_reader.py`** — Handles PDF reading.
- **`llm/llm.py`** — Contains the language-model and report-generation logic.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/dheerajdogra102003-create/AI-RUS.git
cd AI-RUS
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

OCR libraries may download model files on their first run. Installation requirements can vary by operating system and Python version.

### 4. Configure environment variables

If the application requires a Google Gen AI API key, configure it using a local `.env` file, following the variable name expected by `llm/llm.py`.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the example with your own valid key. Never commit `.env` files, API keys, or other credentials to GitHub.

### 5. Launch the application

From the repository root, run:

```bash
streamlit run App/app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`.

## ☁️ Deployment

AI-RUS is deployed using **Streamlit Community Cloud**.

Visit the live application:

**[https://ai-rus.streamlit.app/](https://ai-rus.streamlit.app/)**

The deployed application uses `App/app.py` as its entry point and `requirements.txt` for Python dependencies. System-level Linux dependencies, when required, can be specified in `packages.txt`.

## 🔐 Security and Privacy

- Keep API keys and credentials out of source code.
- Store deployment secrets using Streamlit's Secrets management.
- Avoid uploading confidential or personally identifiable documents unless you understand how the application processes and stores their contents.
- Review third-party service policies before submitting sensitive documents.

## 🔮 Future Improvements

Potential areas for further development include:

- Improved handling of low-quality scans and complex layouts.
- More robust extraction of tables and structured fields.
- Validation of AI-generated reports against extracted source text.
- Downloadable report formats and additional document-processing options.
- Better error handling and processing-status feedback.

## 👨‍💻 Author

**Dheeraj Kumar**

- GitHub: [@dheerajdogra102003-create](https://github.com/dheerajdogra102003-create)
- LinkedIn: [dheerajkumar00](https://www.linkedin.com/in/dheerajkumar00/)

---

*AI-RUS brings together document processing, OCR, and Generative AI to make extracting and understanding document information more convenient.*

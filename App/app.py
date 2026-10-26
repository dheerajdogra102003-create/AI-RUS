

# ```text
# medical-timeline/
# ├── app.py                # ├── requirements.txt               # Python dependencies
# ├── .gitignore                     # Excludes local data, uploads, and secrets
# ├── models/
# │   └── event.py                   # Timeline event data structure
# ├── extractors/
# │   ├── pdf_reader.py              # Digital PDF extraction and page rendering
# │   └── image_reader.py            # PaddleOCR for images and scanned pages
# ├── processing/
# │   ├── clinical_events.py         # Medication, disease, and symptom candidates
# │   ├── dates.py                   # Date detection and normalization
# │   └── timeline.py                # Review filtering and chronological ordering
# ├── services/
# │   ├── ingestion.py               # Coordinates upload and extraction pipeline
# │   └── export.py                  # CSV generation
# └── data/                           # Local runtime data; do not commit                # Optional temporary uploaded files



# from file_reader.image_scanner import PdfReader
# from ingest.ingest import collect_user_input

# ls=[]
# input_paths=[
#     r"D:\AI-RUS\images (2).jpg",
#     r"D:\AI-RUS\images (1).jpg",
#     r"D:\AI-RUS\images (3).jpg",
#     r"D:\AI-RUS\images.jpg",
#     r"D:\AI-RUS\sample_prescription.webp",
#     r"D:\AI-RUS\screen-13.png"
# ]
# path_pdf,image_path=collect_user_input(input_paths)
# for path in path_pdf:
#     text=PdfReader(path)
#     ls.append(f"pdf {path} : {text}\n\n")

# for path in image_path:
#     text=PdfReader(path)
#     ls.append(f"image {path} : {text}\n\n")

# print(ls)









import streamlit as st
from pathlib import Path
import tempfile
import os


# Import your existing functions
from Ingest.ingest import collect_user_input
from FileReader.image_scanner import PdfReader
from LLM.llm import llmReportGenerator
# Replace the imports above if your actual module paths differ.




# import inspect
# st.write("Scanner file:", inspect.getfile(PdfReader))
# st.code(inspect.getsource(PdfReader))




st.set_page_config(
    page_title="AI-RUS Document Scanner",
    page_icon="📄",
    layout="wide"
)

st.title("AI Powered - Read User Summary")
st.caption("Upload medical reports, prescriptions, PDFs and images.")

# Store uploaded files in Streamlit session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# File uploader
new_files = st.file_uploader(
    "Attach your files",
    type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "webp"],
    accept_multiple_files=True,
    key="file_uploader"
)

# Keep uploaded files staged until Scan is pressed
if new_files:
    existing_names = {
        (f.name, f.size)
        for f in st.session_state.uploaded_files
    }

    for file in new_files:
        if (file.name, file.size) not in existing_names:
            st.session_state.uploaded_files.append(file)
            existing_names.add((file.name, file.size))

# Display staged attachments
st.subheader("📎 Attached files")

if st.session_state.uploaded_files:
    for i, file in enumerate(st.session_state.uploaded_files):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")

        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.uploaded_files.pop(i)
                st.rerun()
else:
    st.info("No files attached yet.")

# Clear all attachments
if st.session_state.uploaded_files:
    if st.button("🗑️ Clear all files"):
        st.session_state.uploaded_files = []
        st.rerun()

st.divider()

# Process only after the user clicks Scan
if st.button("🔍 Scan files", type="primary",
             disabled=not st.session_state.uploaded_files):

    pdf_paths = []
    image_paths = []

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Save staged uploads temporarily
            for file in st.session_state.uploaded_files:
                file_path = Path(temp_dir) / Path(file.name).name

                file_path.write_bytes(file.getvalue())

            # Classify PDFs and images using your existing function
            all_paths = [
                Path(temp_dir) / Path(f.name).name
                for f in st.session_state.uploaded_files
            ]

            pdf_paths, image_paths = collect_user_input(all_paths)

            st.subheader("📝 Scanning results")

            # Scan images using your existing OCR function
            for image_path in image_paths:
                st.markdown(f"### 🖼️ {Path(image_path).name}")

                try:
                    with st.spinner(f"Scanning {Path(image_path).name}..."):
                        extracted_text = PdfReader(image_path)
                        # st.write("DEBUG:", repr(extracted_text), type(extracted_text))

                    if extracted_text:
                        st.text_area(
                            "Extracted text",
                            value=extracted_text,
                            height=250,
                            key=f"result_{Path(image_path).name}"
                        )


                        st.text_area("Extracted OCR Text", value=extracted_text, height=200)
                        # Send to Gemini LLM:
                        with st.spinner("Generating Medical Timeline with AI..."):
                            timeline = llmReportGenerator(extracted_text)
                            st.markdown("### 📋 Medical History Timeline")
                            st.markdown(timeline)

                    
                    else:
                        st.warning(
                            "No text detected in this image."
                        )

                except Exception as e:
                    st.error(f"Image scanning failed: {e}")

            # PDFs need your existing PDF reader integration
            for pdf_path in pdf_paths:
                st.warning(
                    f"PDF detected: {Path(pdf_path).name}. "
                    "Connect your PDF-reading function here."
                )

        except Exception as e:
            st.error(f"Could not process files: {e}")

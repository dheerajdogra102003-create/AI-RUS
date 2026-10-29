

# # # ```text
# # # medical-timeline/
# # # ├── app.py                # ├── requirements.txt               # Python dependencies
# # # ├── .gitignore                     # Excludes local data, uploads, and secrets
# # # ├── models/
# # # │   └── event.py                   # Timeline event data structure
# # # ├── extractors/
# # # │   ├── pdf_reader.py              # Digital PDF extraction and page rendering
# # # │   └── image_reader.py            # PaddleOCR for images and scanned pages
# # # ├── processing/
# # # │   ├── clinical_events.py         # Medication, disease, and symptom candidates
# # # │   ├── dates.py                   # Date detection and normalization
# # # │   └── timeline.py                # Review filtering and chronological ordering
# # # ├── services/
# # # │   ├── ingestion.py               # Coordinates upload and extraction pipeline
# # # │   └── export.py                  # CSV generation
# # # └── data/                           # Local runtime data; do not commit                # Optional temporary uploaded files


















# import sys
# import streamlit as st
# from pathlib import Path
# import tempfile

# # Project root: assuming app.py is inside D:\AI-RUS
# ROOT_DIR = Path(__file__).resolve().parent

# if str(ROOT_DIR) not in sys.path:
#     sys.path.insert(0, str(ROOT_DIR))

# from Ingest.ingest import collect_user_input
# from FileReader.image_scanner import scan_image
# from FileReader.pdf_reader import read_pdf
# from LLM.llm import llmReportGenerator


# st.set_page_config(
#     page_title="AI-RUS Document Scanner",
#     page_icon="📄",
#     layout="wide"
# )

# st.title("AI Powered - Read User Summary")
# st.caption("Upload medical reports, prescriptions, PDFs and images.")

# # Store uploaded files
# if "uploaded_files" not in st.session_state:
#     st.session_state.uploaded_files = []

# # File uploader
# new_files = st.file_uploader(
#     "Attach your files",
#     type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "webp"],
#     accept_multiple_files=True,
#     key="file_uploader"
# )

# # Stage uploaded files
# if new_files:
#     existing = {
#         (f.name, f.size)
#         for f in st.session_state.uploaded_files
#     }

#     for file in new_files:
#         if (file.name, file.size) not in existing:
#             st.session_state.uploaded_files.append(file)
#             existing.add((file.name, file.size))

# # Display attachments
# st.subheader("📎 Attached files")

# if st.session_state.uploaded_files:
#     for i, file in enumerate(st.session_state.uploaded_files):
#         col1, col2 = st.columns([5, 1])

#         with col1:
#             st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")

#         with col2:
#             if st.button("Remove", key=f"remove_{i}"):
#                 st.session_state.uploaded_files.pop(i)
#                 st.rerun()

#     if st.button("🗑️ Clear all files"):
#         st.session_state.uploaded_files = []
#         st.rerun()
# else:
#     st.info("No files attached yet.")

# st.divider()

# # Scan all files and generate ONE combined report
# if st.button(
#     "🔍 Scan Files & Generate Combined Report",
#     type="primary",
#     disabled=not st.session_state.uploaded_files
# ):

#     # Fresh content for every scan
#     all_extracted_text = []
#     combined_text_file = None

#     with tempfile.TemporaryDirectory() as temp_dir:
#         temp_path = Path(temp_dir)

#         try:
#             all_paths = []

#             # Save uploaded files temporarily
#             for i, file in enumerate(st.session_state.uploaded_files):
#                 saved_path = temp_path / f"{i}_{Path(file.name).name}"
#                 saved_path.write_bytes(file.getvalue())
#                 all_paths.append(saved_path)

#             # Classify files using your existing function
#             pdf_paths, image_paths = collect_user_input(all_paths)

#             st.subheader("📝 Extracted Text")

#             # Process all images
#             for image_path in image_paths:
#                 filename = Path(image_path).name

#                 try:
#                     with st.spinner(f"Extracting text from {filename}..."):
#                         text = scan_image(str(image_path))

#                     if text and text.strip():
#                         # Keep the source filename with the extracted text
#                         file_text = (
#                             f"\n\n{'=' * 60}\n"
#                             f"SOURCE FILE: {filename}\n"
#                             f"{'=' * 60}\n"
#                             f"{text.strip()}\n"
#                         )

#                         all_extracted_text.append(file_text)

#                         # Show text extracted from this file
#                         # with st.expander(f"📄 {filename}"):
#                         #     st.text_area(
#                         #         "Extracted text",
#                         #         value=text,
#                         #         height=250,
#                         #         key=f"text_{filename}"
#                         #     )

#                     else:
#                         st.warning(f"No text detected in {filename}.")

#                 except Exception as e:
#                     st.error(f"Image scanning failed for {filename}: {e}")

#             # PDFs are classified but no PDF reader is connected yet
#             for pdf_path in pdf_paths:
#                 st.warning(
#                     f"PDF detected: {Path(pdf_path).name}. "
#                     "PDF text extraction is not connected. "
#                     "This PDF will not be included in the report."
#                 )

#             # Combine all successful extractions into one string
#             combined_text = "\n".join(all_extracted_text).strip()

#             if not combined_text:
#                 st.error("No text was extracted. Cannot generate a report.")

#             else:
#                 # Save all extracted text into one file
#                 combined_text_file = temp_path / "combined_extracted_text.txt"
#                 combined_text_file.write_text(
#                     combined_text,
#                     encoding="utf-8"
#                 )

#                 st.success(
#                     f"Combined text created from "
#                     f"{len(all_extracted_text)} file(s)."
#                 )

#                 # Preview the complete combined text
#                 # with st.expander("📚 View complete combined text"):
#                 #     st.text_area(
#                 #         "All extracted text",
#                 #         value=combined_text,
#                 #         height=350,
#                 #         key="combined_text_preview"
#                 #     )

#                 # Generate one report from ALL extracted text
#                 with st.spinner("Generating combined medical timeline..."):
#                     report = llmReportGenerator(combined_text)

#                 if report.startswith("Report generation failed:"):
#                     st.error(report)
#                 else:
#                     st.subheader("📋 Combined Medical History Timeline")
#                     st.markdown(report)

#                     # st.download_button(
#                     #     "⬇️ Download Combined Report",
#                     #     data=report,
#                     #     file_name="combined_medical_timeline.md",
#                     #     mime="text/markdown"
#                     # )

#                 # Download the complete OCR text too
#                 st.download_button(
#                     "⬇️ Download All Extracted Text",
#                     data=combined_text,
#                     file_name="combined_extracted_text.txt",
#                     mime="text/plain"
#                 )

#         except Exception as e:
#             st.error(f"Could not process files: {e}")





import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))



import streamlit as st
import tempfile
from Fileingest.ingest import collect_user_input
from FileReader.image_scanner import scan_image
from FileReader.pdf_reader import read_pdf
# pyrefly: ignore[missing-import]
from llm.llm import llmReportGenerator

# Streamlit page configuration
st.set_page_config(
    page_title="AI-RUS Document Scanner",
    page_icon="📄",
    layout="wide"
)

st.title("AI Powered - Read User Summary")
st.caption("Upload medical reports, prescriptions, PDFs and images.")


# Initialize uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# Upload files
new_files = st.file_uploader(
    "Attach your files",
    type=["pdf", "png", "jpg", "jpeg", "tif", "tiff", "webp"],
    accept_multiple_files=True,
    key="file_uploader"
)


# Store uploaded files without duplicates
if new_files:
    existing = {
        (f.name, f.size)
        for f in st.session_state.uploaded_files
    }

    for file in new_files:
        if (file.name, file.size) not in existing:
            st.session_state.uploaded_files.append(file)
            existing.add((file.name, file.size))


# Display attachments
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

    if st.button("🗑️ Clear all files"):
        st.session_state.uploaded_files = []
        st.rerun()

else:
    st.info("No files attached yet.")


st.divider()


# Scan files and generate one combined report
if st.button(
    "🔍 Scan Files & Generate Combined Report",
    type="primary",
    disabled=not st.session_state.uploaded_files
):

    # Store extracted text from all files
    all_extracted_text = []

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        try:
            all_paths = []

            # Save uploaded files temporarily
            for i, file in enumerate(st.session_state.uploaded_files):

                saved_path = temp_path / f"{i}_{Path(file.name).name}"
                saved_path.write_bytes(file.getvalue())

                all_paths.append(saved_path)

            # Classify PDFs and images
            pdf_paths, image_paths = collect_user_input(all_paths)

            st.subheader("📝 Extracted Text")

            # -------------------------------------------------
            # STEP 1: READ PDF FILES USING read_pdf()
            # -------------------------------------------------
            for pdf_path in pdf_paths:

                filename = Path(pdf_path).name

                try:
                    with st.spinner(
                        f"Reading PDF: {filename}..."
                    ):
                        text = read_pdf(str(pdf_path))

                    if text and text.strip():

                        file_text = (
                            f"\n\n{'=' * 60}\n"
                            f"SOURCE FILE: {filename}\n"
                            f"FILE TYPE: PDF\n"
                            f"{'=' * 60}\n"
                            f"{text.strip()}\n"
                        )

                        all_extracted_text.append(file_text)

                        st.success(
                            f"PDF text extracted: {filename}"
                        )

                        with st.expander(
                            f"📄 View extracted PDF text: {filename}"
                        ):
                            st.text_area(
                                "Extracted PDF text",
                                value=text,
                                height=250,
                                key=f"pdf_text_{filename}"
                            )

                    else:
                        st.warning(
                            f"No text extracted from PDF: {filename}"
                        )

                except Exception as e:
                    st.error(
                        f"PDF reading failed for {filename}: {e}"
                    )

            # -------------------------------------------------
            # STEP 2: READ IMAGE FILES USING scan_image()
            # -------------------------------------------------
            for image_path in image_paths:

                filename = Path(image_path).name

                try:
                    with st.spinner(
                        f"Scanning image: {filename}..."
                    ):
                        text = scan_image(str(image_path))

                    if text and text.strip():

                        file_text = (
                            f"\n\n{'=' * 60}\n"
                            f"SOURCE FILE: {filename}\n"
                            f"FILE TYPE: IMAGE\n"
                            f"{'=' * 60}\n"
                            f"{text.strip()}\n"
                        )

                        all_extracted_text.append(file_text)

                        st.success(
                            f"Image text extracted: {filename}"
                        )

                        with st.expander(
                            f"🖼️ View extracted image text: {filename}"
                        ):
                            st.text_area(
                                "Extracted image text",
                                value=text,
                                height=250,
                                key=f"image_text_{filename}"
                            )

                    else:
                        st.warning(
                            f"No text detected in image: {filename}"
                        )

                except Exception as e:
                    st.error(
                        f"Image scanning failed for {filename}: {e}"
                    )

            # -------------------------------------------------
            # STEP 3: COMBINE PDF AND IMAGE TEXT
            # -------------------------------------------------
            combined_text = "\n".join(
                all_extracted_text
            ).strip()

            if not combined_text:

                st.error(
                    "No text was extracted from the uploaded files. "
                    "Cannot generate the report."
                )

            else:

                # Save combined extracted text temporarily
                combined_text_file = (
                    temp_path / "combined_extracted_text.txt"
                )

                combined_text_file.write_text(
                    combined_text,
                    encoding="utf-8"
                )

                st.success(
                    f"Combined text extracted from "
                    f"{len(all_extracted_text)} file(s)."
                )

                # Preview all extracted text
                with st.expander("📚 View complete extracted text"):

                    st.text_area(
                        "Combined extracted text",
                        value=combined_text,
                        height=350,
                        key="combined_text_preview"
                    )

                # -------------------------------------------------
                # STEP 4: GENERATE ONE COMBINED MEDICAL REPORT
                # -------------------------------------------------
                try:
                    with st.spinner(
                        "Generating combined medical timeline..."
                    ):
                        report = llmReportGenerator(combined_text)

                    if (
                        not report
                        or report.startswith("Report generation failed:")
                    ):
                        st.error(
                            report or "Report generation returned no output."
                        )

                    else:
                        st.subheader(
                            "📋 Combined Medical History Timeline"
                        )

                        st.markdown(report)

                        st.download_button(
                            "⬇️ Download Combined Medical Report",
                            data=report,
                            file_name="combined_medical_timeline.md",
                            mime="text/markdown"
                        )

                except Exception as e:
                    st.error(
                        f"Medical report generation failed: {e}"
                    )

                # Download extracted text
                st.download_button(
                    "⬇️ Download All Extracted Text",
                    data=combined_text,
                    file_name="combined_extracted_text.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Could not process files: {e}")

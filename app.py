

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



from file_reader.image_scanner import PdfReader
from ingest.ingest import collect_user_input

ls=[]
input_paths=[
    r"D:\AI-RUS\images (2).jpg",
    r"D:\AI-RUS\images (1).jpg",
    r"D:\AI-RUS\images (3).jpg",
    r"D:\AI-RUS\images.jpg",
    r"D:\AI-RUS\sample_prescription.webp",
    r"D:\AI-RUS\screen-13.png"
]
path_pdf,image_path=collect_user_input(input_paths)
for path in path_pdf:
    text=PdfReader(path)
    ls.append(f"pdf {path} : {text}\n\n")

for path in image_path:
    text=PdfReader(path)
    ls.append(f"image {path} : {text}\n\n")

print(ls)
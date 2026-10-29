import cv2
import easyocr
import numpy as np
from pathlib import Path
import pymupdf  # PyMuPDF


def read_pdf(pdf_path: str) -> str:
    # 1. Check whether the PDF exists
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # 2. Open the PDF
    doc = pymupdf.open(pdf_path)

    # 3. Load EasyOCR reader (for scanned pages)
    reader = easyocr.Reader(["en"], gpu=False)

    extracted_pages = []

    print("\n--- Reading PDF Pages ---\n")

    for page_num, page in enumerate(doc, start=1):
        print(f"--- Page {page_num} ---")

        # Step A: Try extracting digital text directly
        page_text = page.get_text().strip()

        # Step B: If page is a scan/image (no digital text), extract text using OCR
        if not page_text:
            print(f"Page {page_num} has no digital text. Scanning with OCR...")
            
            # Render page to an image
            pix = page.get_pixmap(dpi=200)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))

            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            elif pix.n == 1:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            # OCR text extraction
            results = reader.readtext(img, detail=1, paragraph=False)
            detected_text = []

            for bbox, text, confidence in results:
                print(f"{text} | Confidence: {confidence:.2f}")
                if confidence >= 0.25:
                    detected_text.append(text)

            page_text = "\n".join(detected_text)
        else:
            print(page_text)

        if page_text.strip():
            extracted_pages.append(page_text.strip())

    doc.close()

    print("\n_____________________Filtered Text________________________\n")
    extracted_text = "\n\n".join(extracted_pages)
    print(extracted_text)

    return extracted_text


# Example usage:
# pdf_path = r"D:\AI-RUS\sample.pdf"
# read_pdf(pdf_path)





# read_pdf(r"D:\AI-RUS\Resume__.pdf")   
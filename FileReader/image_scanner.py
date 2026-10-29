
# from file_reader import pdf_reader
# from app import extracted_text
import easyocr
import cv2
# import matplotlib.pyplot as plt
from pathlib import Path

# 1. Set the path of your medicine image
# image_path = r"D:\AI-RUS\sample_prescription.webp"
def scan_image(image_path:str) ->str:
        
    # 2. Check whether the image exists
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 3. Load the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read the image. Check its format and path.")

    # 4. Load the free OCR model
    # gpu=False works on laptops without a configured CUDA GPU.
    reader = easyocr.Reader(["en"], gpu=False)

    # 5. Extract text
    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    # 6. Print recognized text
    detected_text = []

    print("\n--- Detected Text ---\n")
    for bbox, text, confidence in results:
        print(f"{text} | Confidence: {confidence:.2f}")

        if confidence >= 0.25:
            detected_text.append(text)

    
    print("_____________________Filtered Text________________________\n")
    
    extracted_text="\n".join(detected_text)
    print(extracted_text)

    return extracted_text
    

    # # 7. Display the image
    # plt.figure(figsize=(12, 8))
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.axis("off")
    # plt.title("Uploaded Medicine Image")
    # plt.show()




# PdfReader(image_path)
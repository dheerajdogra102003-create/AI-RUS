# from PIL import GimpGradientFile
from pathlib import Path

def collect_user_input(file_paths:list[str|Path]):
    pdf_files = []
    image_files = []

    for file_path in file_paths:

        path=Path(file_path)
        extension=path.suffix.lower()

        if extension==".pdf":
            pdf_files.append(str(path))
        elif extension in {".png", ".jpg", ".jpeg", ".tif", ".tiff",".webp"}:
            image_files.append(str(path))
        else:
            raise ValueError(f"Unrecognised file type {extension} for {path}")
    
    return pdf_files,image_files    

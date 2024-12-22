import cv2
import numpy as np
from PIL import Image
import pytesseract
from io import BytesIO

class ImageProcessor:
    @staticmethod
    async def process_image(image_bytes: bytes) -> str:
        """
        Process the image to improve OCR accuracy
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # # Apply bilateral filter to remove noise while preserving edges
            # denoised = cv2.bilateralFilter(gray, 9, 75, 75)

            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            
            # # Increase contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
            # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            # contrasted = clahe.apply(denoised)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                15,  # reduced block size
                8    # adjusted C constant
            )
            
            # Remove small noise using morphological operations
            kernel = np.ones((2,2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
            
            # Convert back to PIL Image for Tesseract
            pil_image = Image.fromarray(cleaned)
            
            # Enhanced OCR Configuration
            custom_config = r'''--oem 3 --psm 6 
                -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz&.,:$()-@ "
                -c tessedit_write_images=true
                -c textord_heavy_nr=1
                -c textord_min_linesize=2.5'''
            
            text = pytesseract.image_to_string(
                pil_image,
                config=custom_config
            )
            
            # Post-process the text
            lines = text.split('\n')
            cleaned_lines = [
                line.strip() 
                for line in lines 
                if line.strip() and not line.strip().startswith('=') and not line.strip().startswith('-')
            ]
            
            return '\n'.join(cleaned_lines)
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    @staticmethod
    def debug_save_image(image: np.ndarray, filename: str):
        """
        Helper method to save intermediate processing steps for debugging
        """
        cv2.imwrite(f"debug_{filename}.png", image)

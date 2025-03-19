from transformers import pipeline

class ImageOCR:
    def __init__(self, model_name='Salesforce/blip-image-captioning-base'):
        self.ocr_pipeline = pipeline('image-to-text', model=model_name)

    def extract_text(self, image_path):
        return self.ocr_pipeline(image_path)

# Example usage
if __name__ == "__main__":
    ocr = ImageOCR()
    text = ocr.extract_text(r"C:\Users\madha\Pictures\Steve-Jobs-PNG-Clipart.png")
    print(text)

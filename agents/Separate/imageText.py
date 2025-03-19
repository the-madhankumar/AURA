from transformers import pipeline
ocr = pipeline('image-to-text', model='Salesforce/blip-image-captioning-base')
print(ocr(r"C:\Users\madha\Pictures\Steve-Jobs-PNG-Clipart.png"))
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.image_processing import ImageProcessor
from app.services.receipt_parser import ReceiptParser

app = FastAPI()

@app.post("/parse-receipt")
async def parse_receipt(file: UploadFile = File(...)):
    try:
        # Read the file
        contents = await file.read()
        
        # Process the image
        text = await ImageProcessor.process_image(contents)
        
        # Parse the text
        receipt_data = ReceiptParser.parse_text(text)
        
        return {
            "receipt_data": receipt_data,
            "text": text
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

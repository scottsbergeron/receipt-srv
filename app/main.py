from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/parse-receipt")
async def parse_receipt(file: UploadFile = File(...)):
    try:
        # TODO: Implement receipt parsing logic
        return {"message": "Receipt parsed successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error processing receipt: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

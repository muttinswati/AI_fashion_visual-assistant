import os
import shutil
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import user_helper 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(BASE_DIR, "temp")
IMAGES_PATH = os.path.join(BASE_DIR, "images")

os.makedirs(TEMP_PATH, exist_ok=True)
os.makedirs(IMAGES_PATH, exist_ok=True)

app.mount("/temp", StaticFiles(directory=TEMP_PATH), name="temp")
app.mount("/images", StaticFiles(directory=IMAGES_PATH), name="images")

@app.get("/")
async def root():
    return {"status": "AI Server is Running"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        temp_file_path = os.path.join(TEMP_PATH, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        result = user_helper.handle_user_request(temp_file_path)
        return result

    except Exception as e:
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
import anthropic
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from analyser import analyse_skin

ALLOWED_TYPES = {
    "image/jpeg": "image/jpeg",
    "image/jpg": "image/jpeg",
    "image/png": "image/png",
    "image/gif": "image/gif",
    "image/webp": "image/webp",
}

app = FastAPI(title="Skin Analyser")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")


@app.post("/analyse")
async def analyse(file: UploadFile = File(...)):
    content_type = file.content_type or ""
    media_type = ALLOWED_TYPES.get(content_type.split(";")[0].strip())
    if not media_type:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a JPEG, PNG, GIF, or WebP image.")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large. Max 10 MB.")

    try:
        result = analyse_skin(image_bytes, media_type)
    except anthropic.BadRequestError as e:
        raise HTTPException(status_code=422, detail=f"Claude rejected the image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    return JSONResponse(content=result)

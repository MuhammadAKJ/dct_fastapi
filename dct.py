from fastapi import FastAPI, request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import numpy as np
from scipy.spatial import distance

"""
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
"""



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.post("/upload/")
async def upload_images(file1: UploadFile, file2: UploadFile):
    # Process and compare the uploaded images here

    # Convert UploadFile to PIL Image
    img1 = Image.open(file1.file)
    img2 = Image.open(file2.file)

    # Perform image similarity analysis using DCT 
    result = compare_images_using_dct(img1, img2)

    return {"similarity_score": result}
    # return templates.TemplateResponse("result.html", {"request": request, "similarity_score": result})

def compare_images_using_dct(img1, img2):
        
    hash1 = image_hash(img1)
    hash2 = image_hash(img2)

    result = distance.hamming(hash1, hash2)
    return result 

def image_hash(img):
    img = Image.open(img)
    resized_image = img.convert("L").resize((8,8), Image.ANTIALIAS)
    pixel_total = 0
    for x_pix in range(8):
        for y_pix in range(8):
            pixel_total += resized_image.getpixel((x_pix, y_pix))
    pixel_average = pixel_total / 64

    binbits = ""

    pixel = np.asarray(resized_image)
    average = np.mean(pixel)
    if pixel_average == average:
        newList = pixel.tolist()

    for x_pix in range(8):
        for y_pix in range(8):
            if newList[x_pix][y_pix] < average:
                binbits += "0"
            else:
                binbits += "1"
    hash_ = hex(int(binbits, 2))
    return hash_


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

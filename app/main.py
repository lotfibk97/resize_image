import os
import io
import uuid
import logging
from typing import List

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import inspect

import aiofiles

from . import models, schemas, crud
from .database import SessionLocal, engine
from .image_processing import csv_to_image, resize_image, apply_custom_colormap

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.makedirs("temp", exist_ok=True)

inspector = inspect(engine)
logger.info(f"Existing tables before creation: {inspector.get_table_names()}")

models.Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
logger.info(f"Existing tables after creation: {inspector.get_table_names()}")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload_csv/")
async def upload_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> StreamingResponse:
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV file."
        )

    unique_id = uuid.uuid4()
    csv_filename = f"{unique_id}_{file.filename}"
    csv_path = os.path.join("temp", csv_filename)
    image_filename = f"{unique_id}_{os.path.splitext(file.filename)[0]}.png"
    image_path = os.path.join("temp", image_filename)

    MAX_FILE_SIZE = 10 * 1024 * 1024

    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large.")

        async with aiofiles.open(csv_path, "wb") as f:
            await f.write(contents)

        depth_min, depth_max = csv_to_image(csv_path, image_path)

        resized_path = f"{os.path.splitext(image_path)[0]}_resized.png"
        resize_image(image_path, resized_path)

        colored_path = f"{os.path.splitext(image_path)[0]}_colored.png"
        apply_custom_colormap(resized_path, colored_path)

        async with aiofiles.open(resized_path, "rb") as f:
            resized_image_data = await f.read()

        image_create = schemas.ImageCreate(
            data=resized_image_data,
            depth_min=depth_min,
            depth_max=depth_max,
            filename=file.filename,
        )
        db_image = crud.create_image(db, image_create)

        async with aiofiles.open(colored_path, "rb") as f:
            colored_image_data = await f.read()

        return StreamingResponse(io.BytesIO(colored_image_data), media_type="image/png")

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        for path in [csv_path, image_path, resized_path, colored_path]:
            if os.path.exists(path):
                os.remove(path)


@app.get("/images/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)) -> StreamingResponse:
    db_image = crud.get_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return StreamingResponse(io.BytesIO(db_image.data), media_type="image/png")


@app.get("/images/", response_model=List[schemas.ImageOut])
def get_images_by_depth(
    depth_min: float, depth_max: float, db: Session = Depends(get_db)
) -> List[schemas.ImageOut]:
    images = crud.get_images_by_depth(db, depth_min, depth_max)
    return images

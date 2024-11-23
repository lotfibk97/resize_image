from sqlalchemy.orm import Session
from . import models, schemas


def get_image(db: Session, image_id: int) -> models.Image:
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_images_by_depth(db: Session, depth_min: float, depth_max: float) -> list:
    return (
        db.query(models.Image)
        .filter(
            models.Image.depth_min >= depth_min, models.Image.depth_max <= depth_max
        )
        .all()
    )


def create_image(db: Session, image: schemas.ImageCreate) -> models.Image:
    db_image = models.Image(
        data=image.data,
        depth_min=image.depth_min,
        depth_max=image.depth_max,
        filename=image.filename,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

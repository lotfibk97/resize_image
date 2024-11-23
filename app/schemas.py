from pydantic import BaseModel


class ImageCreate(BaseModel):
    data: bytes
    depth_min: float
    depth_max: float
    filename: str


class ImageOut(BaseModel):
    id: int
    depth_min: float
    depth_max: float
    filename: str

    class Config:
        from_attributes = True

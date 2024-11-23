from sqlalchemy import Column, Integer, LargeBinary, String, Float, Index
from .database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(LargeBinary, nullable=False)
    depth_min = Column(Float, nullable=False, index=True)
    depth_max = Column(Float, nullable=False, index=True)
    filename = Column(String, nullable=False)

    __table_args__ = (
        Index("idx_depth_min", "depth_min"),
        Index("idx_depth_max", "depth_max"),
    )

from sqlalchemy import Column, Integer, String
from app.infrastructure.config.database import Base

class CarModel(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=False)
    plate = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<CarModel id={self.id} plate='{self.plate}'>"

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class InputInfo(BaseModel):
    __tablename__ = "InputInfo"
    
    text = Column('Text', String, nullable=False)
    font_size = Column('FontSize', Integer, nullable=False)
    font_family = Column('FontFamily', String, nullable=False)
    x_coordinate = Column('XCoordinate', Integer, nullable=False)
    y_coordinate = Column('YCoordinate', Integer, nullable=False)

class IconInfo(BaseModel):
    __tablename__ = "IconInfo"
    
    base64_string = Column('Base64String', Text, nullable=True)
    x_coordinate = Column('XCoordinate', Integer, nullable=False)
    y_coordinate = Column('YCoordinate', Integer, nullable=False)
    width = Column('Width', Integer, nullable=False)
    height = Column('Height', Integer, nullable=False)

class BarcodeInfo(BaseModel):
    __tablename__ = "BarcodeInfo"
    
    x_coordinate = Column('XCoordinate', Integer, nullable=False)
    y_coordinate = Column('YCoordinate', Integer, nullable=False)
    width = Column('Width', Integer, nullable=False)
    height = Column('Height', Integer, nullable=False)
    barcode_sequence = Column('BarcodeSequence', Integer, nullable=False)
    barcode_format = Column('BarcodeFormat', String, nullable=False)
    text_alignment = Column('TextAlignment', String, nullable=False)
    text_font_size = Column('TextFontSize', Integer, nullable=False)
    text_font_family = Column('TextFontFamily', String, nullable=False)

class LabelSetting(BaseModel):
    __tablename__ = "LabelSetting"
    
    width = Column('Width', Float, nullable=False)
    height = Column('Height', Float, nullable=False)
    dpi = Column('DPI', Integer, nullable=False) 
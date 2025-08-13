from dataclasses import dataclass
from typing import List, Optional
from marshmallow import Schema, fields

# Data Transfer Objects
@dataclass
class InputValuePair:
    input: str
    value: str
    font_family: str
    font_size: int
    x_coordinate: int
    y_coordinate: int

@dataclass
class BarcodeData:
    id: int
    data: str

@dataclass
class IconInfos:
    name: str
    x_coordinate: int
    y_coordinate: int
    width: int
    height: int

@dataclass
class UserInputModel:
    input_value_pairs: Optional[List[InputValuePair]] = None
    barcode_data_list: Optional[List[BarcodeData]] = None
    icon_info_list: Optional[List[IconInfos]] = None

# Marshmallow Schemas for serialization
class InputValuePairSchema(Schema):
    input = fields.Str(required=True)
    value = fields.Str(required=True)
    font_family = fields.Str(required=True)
    font_size = fields.Int(required=True)
    x_coordinate = fields.Int(required=True)
    y_coordinate = fields.Int(required=True)

class BarcodeDataSchema(Schema):
    id = fields.Int(required=True)
    data = fields.Str(required=True)

class IconInfosSchema(Schema):
    name = fields.Str(required=True)
    x_coordinate = fields.Int(required=True)
    y_coordinate = fields.Int(required=True)
    width = fields.Int(required=True)
    height = fields.Int(required=True)

class UserInputModelSchema(Schema):
    input_value_pairs = fields.List(fields.Nested(InputValuePairSchema), required=False)
    barcode_data_list = fields.List(fields.Nested(BarcodeDataSchema), required=False)
    icon_info_list = fields.List(fields.Nested(IconInfosSchema), required=False)

# Additional DTOs
@dataclass
class BarcodeInfoDto:
    id: int
    x_coordinate: int
    y_coordinate: int
    width: int
    height: int
    barcode_sequence: int
    barcode_format: str
    text_alignment: str
    text_font_size: int
    text_font_family: str

@dataclass
class IconInfoDto:
    id: int
    base64_string: str
    x_coordinate: int
    y_coordinate: int
    width: int
    height: int

@dataclass
class InputInfoDto:
    id: int
    text: str
    font_size: int
    font_family: str
    x_coordinate: int
    y_coordinate: int

@dataclass
class LabelSettingDto:
    id: int
    name: str
    value: str

@dataclass
class ToastMessage:
    message: str
    type: str  # 'success', 'error', 'warning', 'info' 
from pydantic import BaseModel
from typing import Optional
from enum import Enum 

# |______________|
# property type

class PropertyType (str, Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    TOWNHOUSE = "townhouse"
    TWIN_HOUSE = "twin_house"
    CHALET ="chalet"
    OFFICE ="office"
    LAND = "land"
    UNKNOWN = "unknown"

# |______________|
# finishing type

class FinishingType(str, Enum):
    FINISHED = "finished"
    SEMI_FINISHED = "semi_finished"
    UNFINISHED = "unfinished"
    ANY = "any"
    UNKNOWN = "unknown"

# |______________|
# lead model

class Lead(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    property_type: PropertyType = PropertyType.UNKNOWN
    location: Optional[str] = None
    budget : Optional[float] = None
    bedrooms : Optional[int] = None
    finishing : FinishingType = FinishingType.UNKNOWN
    timeline : Optional[str] = None 
    intent: Optional[str] = None
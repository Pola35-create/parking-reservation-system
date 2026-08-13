from pydantic import BaseModel

class PersonCreate(BaseModel):
    name: str
    email: str
    can_use_electric: bool
    can_use_accessible: bool
    can_use_dedicated: bool

class PersonResponse(BaseModel):
    id: int
    name: str
    email: str
    can_use_electric: bool
    can_use_accessible: bool
    can_use_dedicated: bool

    model_config = {
        "from_attributes": True
    }
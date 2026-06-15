from pydantic import BaseModel,Field,field_validator
from typing import Annotated
class user_data(BaseModel):
    name:Annotated[str,Field(...,title='name',min_length=1)]
    fname:Annotated[str,Field(...,title='name',min_length=1)]
    mname:Annotated[str,Field(...,title='name',min_length=1)]
    phone_no:Annotated[str,Field(...,title='phone no',pattern=r"^[6-9]\d{9}$")]
    city:Annotated[str,Field(...,title='city',min_length=1)]
    aadhar:Annotated[str,Field(...,title='aadhar',pattern=r"^\d{12}$")]
    
        

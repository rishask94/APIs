from pydantic import BaseModel

class URLBase(BaseModel):
    target_url: str
    term: str

class URLInfo(URLBase):
    url: str
    

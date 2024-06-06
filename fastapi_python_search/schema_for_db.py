from pydantic import BaseModel

class URLSearchInfo(BaseModel):
    url: str
    term_present: bool
    term: str
    links: list[str]
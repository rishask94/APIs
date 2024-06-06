import validators

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from starlette.datastructures import URL

import crud, schemas, schema_for_db

app = FastAPI()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/")
def read_root():
    return "Welcome to the site specific search API :)"

@app.post("/url", response_model=schema_for_db.URLSearchInfo)
def create_url_item(url: schemas.URLBase):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    url_item = crud.create_search_info(url=url)
    return url_item

#query parameter
@app.get("/url")
async def get_url_info(url:str):
   if url_item := crud.get_url_info_db(url=url):
        return url_item
   else:
        raise HTTPException(status_code = 404, detail="Item not found")

@app.get("/url/{term}")
async def get_url_info_by_term(url:str, term: str):
   if url_item := crud.get_url_term_info_db(url=url, term=term):
        return url_item
   else:
        raise HTTPException(status_code = 404, detail="Item not found")

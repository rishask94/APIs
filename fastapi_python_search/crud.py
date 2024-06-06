
import schema_for_db, schemas, search, dynamo_db

def create_search_info( url: schemas.URLBase) -> schema_for_db.URLSearchInfo:
    data = search.siteSpecificSearch(url.target_url, url.term)
    print(data)
    UrlInfo_obj = dynamo_db.get_dynamodb()
    response_info = schema_for_db.URLSearchInfo(
        url=url.target_url, term_present=data['content_present_bool'], term=data['content_present'],  links=data['links']
    )
    UrlInfo_obj.save_to_dynamodb(data)
    return response_info

def get_url_info_db(url: str):
    obj = dynamo_db.get_dynamodb()
    response_item = obj.get_all_entries_url(url)
    return response_item

def get_url_term_info_db (url: str, term: str):
    obj = dynamo_db.get_dynamodb()
    response_item = obj.get_info_by_url_term(url, term)
    return response_item
  

"""

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.secret_key == secret_key, models.URL.is_active)
        .first()
    )


def update_db_clicks(db: Session, db_url: schemas.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(
    db: Session, secret_key: str
) -> models.URL:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url

"""

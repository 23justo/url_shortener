"""
Main execution file for url shorten project
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, Path
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aiohttp
from bs4 import BeautifulSoup
import secrets

app = FastAPI()
SQL_DB_URL = "sqlite:///./url_shortner.db"
engine = create_engine(SQL_DB_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

class ShortUrl(base):
    __tablename__ = "short_urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True,unique=True)
    shortened_url = Column(String, unique=True, index=True)
    title = Column(String)
    visits = Column(Integer, default=0)

base.metadata.create_all(bind=engine)

class URLShortenRequest(BaseModel):
    url: str


class URLShortenReponse(BaseModel):
    short_url: str

async def fetch_title_and_store(original_url: str, shortened_url: str):
    async with aiohttp.ClientSession() as aio_session:
        async with aio_session.get(original_url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title else 'N/A'

    db = session()
    url_entry = db.query(ShortUrl).filter_by(shortened_url=shortened_url).first()
    url_entry.title = title
    db.commit()
    db.close()

@app.post("/shorten-url/", response_model=URLShortenReponse)
async def shorten_url(request: URLShortenRequest, background_tasks: BackgroundTasks):
    """
    create a shortened url with the given url on the param
    params:
        url: str
    returns:
        dict:
            short_url: str with the new shortened url
    """
    db = session()
    original_url = request.url
    url_data = ShortUrl(original_url=request.url)
    db.add(url_data)
    db.commit()
    db.refresh(url_data)
    short_url = str(url_data.id)
    url_data.shortened_url = f"http://localhost:8000/{short_url}"
    db.commit()
    background_tasks.add_task(fetch_title_and_store, original_url, f"http://localhost:8000/{short_url}")
    return {"short_url": f"http://localhost:8000/{short_url}"}

@app.get("/redirect")
async def redirect_to_url(short_url: str):
    db = session()
    url_data_entry = db.query(ShortUrl).filter_by(shortened_url=short_url).first()
    if url_data_entry is None:
        raise HTTPException(status_code=404, detail="URL not found")
    url_data_entry.visits += 1
    original_url = url_data_entry.original_url
    db.commit()
    db.close()
    
    return {"original_url": original_url}


@app.get("/top-100")
async def get_top_100():
    db = session()
    data = db.query(ShortUrl).order_by(ShortUrl.visits.desc()).limit(100).all()
    result = []
    for value in data:
        result.append({
            'id': value.id,
            'url': value.original_url,
            'visits': value.visits,
            'title': value.title
        })
    db.close()
    return {'response': result}




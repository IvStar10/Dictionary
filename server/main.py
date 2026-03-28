import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from handlers.data import WordsStore, JSON, Date


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

words_store = WordsStore(JSON('../data/words.json'), logger)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    with open('index.html', 'r') as f:
        return f.read()


@app.get("/words")
async def get_all_words():
    return words_store.get_all_words()


@app.get("/words/{date}")
async def get_words(date: str):
    return words_store.get_words(Date.parse(date))

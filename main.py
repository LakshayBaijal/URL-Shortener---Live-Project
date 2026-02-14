from fastapi import FastAPI, HTTPException
from storage import read_urls, write_urls, read_meta, write_meta
from utils import is_valid_url, encode_base62
from fastapi.responses import RedirectResponse

app = FastAPI()

BASE_URL = "https://url-shortener-live-project.onrender.com/"


@app.get("/")
def home():
    return {"message": "URL Shortener is running"}


@app.post("/shorten")
def shorten_url(original_url: str):

    # validate URL
    if not is_valid_url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # read existing data
    urls = read_urls()
    meta = read_meta()

    counter = meta["counter"]

    # generate short id
    short_id = encode_base62(counter)

    # store mapping
    urls[short_id] = {
        "original_url": original_url,
        "clicks": 0
    }

    # update counter
    meta["counter"] = counter + 1

    # save data
    write_urls(urls)
    write_meta(meta)

    # return short URL
    short_url = BASE_URL + short_id

    return {
        "short_url": short_url,
        "short_id": short_id
    }


@app.get("/stats/{short_id}")
def get_stats(short_id: str):

    urls = read_urls()

    if short_id not in urls:
        raise HTTPException(status_code=404, detail="Short URL not found")

    data = urls[short_id]

    return {
        "short_id": short_id,
        "original_url": data["original_url"],
        "clicks": data["clicks"]
    }




@app.get("/all_urls")
def get_all_urls():

    urls = read_urls()

    result = []

    for short_id, data in urls.items():

        result.append({
            "short_id": short_id,
            "original_url": data["original_url"],
            "clicks": data["clicks"]
        })

    return result

@app.get("/top_urls")

def get_top_urls():

    urls = read_urls()

    sorted_urls = sorted(
        urls.items(),
        key=lambda item: item[1]["clicks"],
        reverse=True
    )

    result = []

    for short_id, data in sorted_urls:

        result.append({
            "short_id": short_id,
            "original_url": data["original_url"],
            "clicks": data["clicks"]
        })

    return result


@app.post("/shorten_custom")
def shorten_custom(original_url: str, custom_alias: str):

    # validate URL
    if not is_valid_url(original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    urls = read_urls()

    # check if alias already exists
    if custom_alias in urls:
        raise HTTPException(status_code=400, detail="Alias already exists")

    # store custom alias
    urls[custom_alias] = {
        "original_url": original_url,
        "clicks": 0
    }

    write_urls(urls)

    short_url = BASE_URL + custom_alias

    return {
        "short_url": short_url,
        "custom_alias": custom_alias
    }

@app.delete("/delete/{short_id}")
def delete_url(short_id: str):

    urls = read_urls()

    if short_id not in urls:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # delete entry
    del urls[short_id]

    write_urls(urls)

    return {
        "message": f"{short_id} deleted successfully"
    }



@app.get("/{short_id}")
def redirect_to_original(short_id: str):

    urls = read_urls()

    # check if short id exists
    if short_id not in urls:
        raise HTTPException(status_code=404, detail="Short URL not found")

    original_url = urls[short_id]["original_url"]

    # increment click count
    urls[short_id]["clicks"] += 1
    write_urls(urls)

    # redirect
    return RedirectResponse(original_url)


import os

PORT = int(os.environ.get("PORT", 8000))


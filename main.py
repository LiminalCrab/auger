from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def sync_urls(urls: dict):
    return urls


@app.get("/feed/{post_id}")
def feed(
    post_id: int,
    feed_url: str,
    article_link: str,
    article_title: str,
    article_desc: str,
    article_date: str,
) -> dict:

    return {
        f"{post_id}": {
            "feed": f"{feed_url}",
            "article_link": f"{article_link}",
            "article_title": f"{article_title}",
            "article_description": f"{article_desc}",
            "article_date": f"{article_date}",
        }
    }

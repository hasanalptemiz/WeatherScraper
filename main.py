from fastapi import FastAPI
from app.handlers import get_router
from app.services import multithread_scrape_and_insert


multithread_scrape_and_insert()

app = FastAPI()
app.include_router(get_router())



@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Scraper API!"}


if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
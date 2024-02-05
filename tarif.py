from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis

redis_client = Redis(
    host='localhost',
    port=6379, 
    db=0, 
    decode_responses=True 
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def tarifs():
    return HTMLResponse(
        content=open(
            "static/templates_delivery_pvz_no_house/index.html", "r", encoding="utf-8"
        ).read()
    )


@app.post("/get_inputs")
async def get_data( data: str = Form(...)):
    print(data)
    return {"message": "Data received successfully"}


@app.get("/search_points", response_class=JSONResponse)
async def search_cities(query: str):
    cities_data = [
        "ул. Расковой, 10с4, 103 1-й Ботанический пр., 5",
        "ул. Автозаводский 3-й проезд, 4",
        "ул. Лермонтовский пр-т., 6 Нагатинская набережная, 54",
        "ул. Куусинена, 11, корп. 3"
    ]
    starts_with_query = []
    for city_data in cities_data:
        if query.lower() in city_data.lower():
            starts_with_query.append(city_data)
            if len(starts_with_query) == 5:
                break
    return JSONResponse(content={"data": starts_with_query})
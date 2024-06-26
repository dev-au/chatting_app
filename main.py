from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from config import api_routes

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

for route in api_routes:
    app.include_router(route)


@app.on_event('startup')
async def start_project():
    register_tortoise(
        app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ['data.models']},
        generate_schemas=True
    )

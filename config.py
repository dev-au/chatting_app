from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

main_router = APIRouter(include_in_schema=False)
user_router = APIRouter(prefix='/api', tags=['user'])

api_routes = (main_router, user_router,)

render = Jinja2Templates(directory='templates').TemplateResponse

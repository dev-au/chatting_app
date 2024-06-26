from fastapi import Request

from config import main_router, render


@main_router.get("/")
async def index(request: Request):
    return render(request, "index.html")


@main_router.get("/signup")
async def signup(request: Request):
    return render(request, "signup.html")


@main_router.get("/login")
async def login(request: Request):
    return render(request, "login.html")


@main_router.get('/chat/{username}')
async def chat(request: Request, username: str):
    return render(request, "chat.html", {"username": username})

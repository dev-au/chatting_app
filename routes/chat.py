from fastapi import WebSocket

from config import main_router
from resource.auth import *
from resource.chatting import Chat


@main_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    headers = websocket.headers
    access_token = headers.get('Authorization')
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return await websocket.close()
    except InvalidTokenError:
        return await websocket.close()
    user = await User.get_or_none(username=username)
    if user is None:
        return await websocket.close()

    async with Chat(websocket, user) as session_user:
        await session_user.run_handler()

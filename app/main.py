from typing import Optional

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse

from .routes import gallery
from .routes import users
from .routes import picture

app = FastAPI(
    title="Picture Gallery",
    description="My best project",
    version="0.1.1"
)
app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:3000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(users.router)
app.include_router(gallery.router)
app.include_router(picture.router)


# TODO: expect a JWT token for each endpoint excluding login
# TODO: validate expiration time of a JWT token


@app.get("/")
async def homepage():
    return RedirectResponse(url="/docs",
                            status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .routes import galleries
from .routes import users
from .routes import pictures

# Initialization of the web framework
app = FastAPI(
    title="Picture Gallery",
    description="My best project",
    version="1.0.0"
)


@app.exception_handler(500)
async def custom_http_exception_handler(request, exc):
    # error = ErrorResponse(error="Something went wrong")
    # error = jsonable_encoder(error.dict())

    response = Response("Internal server error", status_code=500)

    # Since the CORSMiddleware is not executed when an unhandled server exception
    # occurs, we need to manually set the CORS headers ourselves if we want the FE
    # to receive a proper JSON 500, opposed to a CORS error.
    # Setting CORS headers on server errors is a bit of a philosophical topic of
    # discussion in many frameworks, and it is currently not handled in FastAPI.
    # See dotnet core for a recent discussion, where ultimately it was
    # decided to return CORS headers on server failures:
    # https://github.com/dotnet/aspnetcore/issues/2378
    origin = request.headers.get('origin')

    if origin:
        # Have the middleware do the heavy lifting for us to parse
        # all the config, then update our response headers
        cors = CORSMiddleware(
            app=app,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"])

        # Logic directly from Starlette's CORSMiddleware:
        # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

        response.headers.update(cors.simple_headers)
        has_cookie = "cookie" in request.headers

        # If request includes any cookie headers, then we must respond
        # with the specific origin instead of '*'.
        if cors.allow_all_origins and has_cookie:
            response.headers["Access-Control-Allow-Origin"] = origin

        # If we only allow specific origins, then we have to mirror back
        # the Origin header in the response.
        elif not cors.allow_all_origins and cors.is_allowed_origin(
                origin=origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")

    return response


# Middleware to catch and log exceptions
# This way server not crashes and is able to send all CORS headers
# async def catch_exceptions_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as e:
#         print("=========> Exception: ", e)
#         # you probably want some kind of logging here
#         return Response("Internal server error", status_code=500)
#
#
# app.middleware('http')(catch_exceptions_middleware)

# Permit Cross Origin requests to everyone from everywhere
app.add_middleware(CORSMiddleware,
                   allow_origins=["*", "http://localhost:3000"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
# Initialize router with routes for different parts of application:
app.include_router(users.router)
app.include_router(galleries.router)
app.include_router(pictures.router)

# Read port number from environment; default: 8000
port = int(os.environ.get('PORT', 8000))
if __name__ == "__main__":
    # Run server based on application (app)
    uvicorn.run(app, host="0.0.0.0", port=port)

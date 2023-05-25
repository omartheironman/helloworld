import asyncio
from http import HTTPStatus

from fastapi import FastAPI
from starlette.responses import RedirectResponse



app = FastAPI()


@app.get("/hello")
def get_hello_world():
    return "Hello from OMAAR"

    
@app.get("/", include_in_schema=False)
async def get():
    # Redirect to the docs page
    response = RedirectResponse(url="docs")
    return response

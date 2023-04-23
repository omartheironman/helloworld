import asyncio
import os
import redis
from fastapi import FastAPI, HTTPException, status, Request
from typing import Dict
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse



app = FastAPI()
# ready = True

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
redis_client = redis.Redis(host=redis_host, port=redis_port)

def is_redis_available() -> bool:
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False

def get_redis_response() -> Dict:
    return {"code": 400, "message": "Redis is offline"}

def check_redis() -> None:
    if not is_redis_available():
        raise HTTPException(status_code=status.HTTP_200_OK, detail=get_redis_response())

@app.get("/healthz")
def healthz():
    check_redis()
    return {"status": "OK"}

@app.get("/readyz")
def readyz():
    check_redis()
    print(app.state.ready)
    if not app.state.ready:
        return {"status": "not ready"}
    return {"status": "ready"}

@app.get("/readyz/enable", status_code=status.HTTP_202_ACCEPTED )
def enable_readyz():
    check_redis()
    if app.state.ready:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Instance is already ready")
    app.state.ready = True
    return {"status": "Instance will start receiving traffic soon."}, status.HTTP_202_ACCEPTED

@app.get("/readyz/disable")
def disable_readyz():
    check_redis()
    if not app.state.ready:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Instance is already disabled")
    app.state.ready = False
    return {"status": "Instance will stop receiving traffic soon."}, status.HTTP_202_ACCEPTED

@app.get("/env")
def env():
    check_redis()
    return dict(os.environ), status.HTTP_200_ACCEPTED

@app.get("/headers")
def headers(request: Request):
    check_redis()
    return dict(request.headers), status.HTTP_200_ACCEPTED

@app.get("/delay/{seconds}")
async def delay(seconds: int):
    check_redis()
    await asyncio.sleep(seconds)
    return {"delay": seconds}

@app.put("/cache/{key}")
@app.post("/cache/{key}")
async def cache(key: str, request: Request):
    value = await request.body()
    check_redis()
    redis_client.set(key, value)
    return {"status": "OK"}, status.HTTP_202_ACCEPTED

@app.get("/cache/{key}")
async def get_cache(key: str):
    check_redis()
    value = redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": 404, "message": "Key not found"})

    return jsonable_encoder(value), status.HTTP_200_ACCEPTED

@app.delete("/cache/{key}")
def delete_key(key: str):
    check_redis()
    redis_client.delete(key)
    return "", status.HTTP_202_ACCEPTED

@app.on_event("startup")
async def startup_event():
    app.state.ready = False  # Set ready to False initially
    await asyncio.sleep(10)  # Add a delay to allow Redis service to start up properly
    app.state.ready = True  # Set ready to True after the delay
    
    
@app.get("/", include_in_schema=False)
async def get():
    # Redirect to the docs page
    response = RedirectResponse(url="docs")
    return response
from fastapi import FastAPI

import fastapi

app = fastapi.FastAPI(
    title=advertisement API,
    version=0.1.0,
    description=API for advertisement,
    lifespan=lifespan,
)


@app.post("/advertisement", response_model=)

async def create_advertisement():
    return response

@app.patch('/advertisement/{advertisement_id}')

async def update_advertisement():
    return response


@app.delete('/advertisement/{advertisement_id}')

async def delete_advertisement():
    return response

@app.get('/advertisement/{advertisement_id}')


@app.get('/advertisement?{query_string}')
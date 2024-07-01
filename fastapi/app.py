from fastapi import FastAPI
from get_token import router as get_token_route
from get_records import router as get_records_routes

app = FastAPI()

app.include_router(get_token_route)
app.include_router(get_records_routes)
from fastapi import FastAPI
from crude import product_crude,file_crude

app = FastAPI()

app.include_router(product_crude.router)
app.include_router(file_crude.router)

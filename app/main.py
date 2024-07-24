
import init_db
import uvicorn

from fastapi import FastAPI
from account_details import router

from starlette.middleware.cors import CORSMiddleware

from custom_middleware import TraceabilityMiddleware, LoggingMiddleware


init_db.init_db()

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],),


app.include_router(router, prefix="/api")
app.add_middleware(TraceabilityMiddleware)
app.add_middleware(LoggingMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app= "main:app", port=8000, reload=True)

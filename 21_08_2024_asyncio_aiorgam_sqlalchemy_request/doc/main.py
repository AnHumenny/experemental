from router import router as task_router
from fastapi import FastAPI


app = FastAPI()


app.include_router(task_router)




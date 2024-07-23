from fastapi import FastAPI
# from database import create_table, delete_table
# from contextlib import asynccontextmanager
from router import router as task_router

#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await delete_table()
#     print('the tables was been deleted!')
#     await create_table()
#     print('the table was been created!')
#     yield
#     print('Exit!')
#
#
# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(task_router)



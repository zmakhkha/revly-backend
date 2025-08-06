from db_config import get_session, create_db_and_tables
from db_models import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from schemas import *

create_db_and_tables()
server = FastAPI()

origins = [ "*"]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],
)

import crud

from db_config import get_session, create_db_and_tables
from db_models import *
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import *
from typing import List

create_db_and_tables()
server = FastAPI()
import crud

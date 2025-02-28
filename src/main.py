from fastapi import FastAPI
from pydantic import BaseModel
from hashlib import sha256
from typing import List, Optional
from time import time
from uuid import uuid4
import httpx

# FastAPI Setup
app = FastAPI()

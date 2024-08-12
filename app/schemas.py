from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class User(BaseModel):
    email : EmailStr
    password : str
    

class responseUser(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime


class Post(BaseModel):
    title : str
    description : str
    publish : Optional[bool] = False


class responsePost(BaseModel):
    title : str
    content : str
    created_at : datetime
    user_id : int
    email : EmailStr


class createPost(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    created_at : datetime
    user_id : int
    email : EmailStr
    


class updatePost(BaseModel):
    title : Optional[str] = "Post"
    description : Optional[str] = "Posted via X"
    publish : Optional[bool] = True
    

class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[str] = None


class Like(BaseModel):
    post_id : int
    dir : conint(le=1)


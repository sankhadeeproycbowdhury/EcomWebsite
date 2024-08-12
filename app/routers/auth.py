from fastapi import APIRouter,HTTPException,Response,status,Depends
from .. import schemas,database,utils,Oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags = ['Athentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends()):
    database.cur.execute("SELECT * FROM users WHERE email = %s", (user_credentials.username,))
    user = database.cur.fetchone()

    if not user or not utils.verify(user_credentials.password, user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = Oauth2.create_access_token(data={"user_id" : user['id']})

    return {"access_token" : access_token, "token_type" : "bearer"}

    

    
    
    
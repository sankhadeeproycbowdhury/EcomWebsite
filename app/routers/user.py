from .. import schemas,database,utils
from fastapi import HTTPException,status,APIRouter

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/" , status_code=status.HTTP_201_CREATED, response_model=schemas.responseUser)
def create_user(user : schemas.User):
    database.cur.execute("SELECT * FROM users WHERE email = %s", (str(user.email),))
    user_check = database.cur.fetchone()
    
    if not user_check:
        database.cur.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * ",
        (user.email, utils.hash(user.password)))
        new_user = database.cur.fetchone()
        database.conn.commit()
        return new_user

    raise HTTPException(status_code = status.HTTP_226_IM_USED, detail="Email already in Use")
        
          
@router.get("/{id}", response_model=schemas.responseUser)
def get_post(id : int):
    database.cur.execute("SELECT * FROM users WHERE id = %s", (str(id),))
    res = database.cur.fetchone()
    if res != None:
        return res

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Unknown user-Id, Id-{id} not found")
    
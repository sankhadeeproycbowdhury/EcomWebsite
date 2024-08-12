from .. import schemas,database,Oauth2
from fastapi import HTTPException,status,APIRouter,Depends
from typing import List,Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[schemas.responsePost] )
def get_post(curr_user : dict=Depends(Oauth2.get_current_user), limit : int=5, skip : int=0, search : Optional[str] = ""):
    database.cur.execute("SELECT posts.*,users.email FROM posts JOIN users ON users.id = posts.user_id WHERE published = true AND title ILIKE %s LIMIT %s OFFSET %s ",
    ('%'+search+'%',limit,skip))
    post = database.cur.fetchall()

    return post


@router.get("/{id}", response_model=schemas.responsePost)
def get_post(id : int, curr_user : dict = Depends(Oauth2.get_current_user)):
    database.cur.execute("SELECT posts.*,users.email FROM posts JOIN users ON users.id = posts.user_id WHERE  posts.id = %s AND published = true", (str(id),))
    res = database.cur.fetchone()
    if res != None:
        return res

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Unknown post-Id, Id-{id} not found")


@router.post("/" , status_code=status.HTTP_201_CREATED, response_model=schemas.createPost)
def create_post(post : schemas.Post, curr_user : dict = Depends(Oauth2.get_current_user)):
    database.cur.execute("INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING * ",
    (post.title, post.description, post.publish, curr_user['id']))
    new_post = database.cur.fetchone()
    database.conn.commit()

    database.cur.execute("SELECT email FROM users WHERE id = %s", (curr_user['id'],))
    email = database.cur.fetchone()
    new_post['email'] = email['email']

    return new_post


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, curr_user : dict = Depends(Oauth2.get_current_user)):
    database.cur.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    del_post = database.cur.fetchone()
    if del_post != None:
        if del_post['user_id'] != curr_user['id']:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the request action")
        database.cur.execute("DELETE FROM posts WHERE id = %s", (str(id),))
        database.conn.commit()
        return

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Unknown post-Id, Id-{id} not found")


@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED, response_model=schemas.createPost)
def update_post(id : int, post : schemas.updatePost, curr_user : dict = Depends(Oauth2.get_current_user)):
    database.cur.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    updated_post = database.cur.fetchone()
    if update_post != None:
        if updated_post['user_id'] != curr_user['id']:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the request action")
        database.cur.execute("UPDATE posts SET title = %s, content =%s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.description, post.publish, str(id),))
        updated_post = database.cur.fetchone()
        database.conn.commit()

        database.cur.execute("SELECT email FROM users WHERE id = %s", (curr_user['id'],))
        email = database.cur.fetchone()
        updated_post['email'] = email['email']
        
        return updated_post

    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Unknown post-Id, Id-{id} not found")


    
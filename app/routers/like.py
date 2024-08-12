from fastapi import HTTPException,status,APIRouter,Depends
from .. import database,schemas,Oauth2

router = APIRouter(
    prefix="/like",
    tags=['like']
)


@router.post("/", status_code= status.HTTP_201_CREATED)
def like(vote : schemas.Like, curr_user : dict=Depends(Oauth2.get_current_user)):
    database.cur.execute("SELECT * FROM posts WHERE id = %s AND published = true", (str(vote.post_id),))
    post = database.cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does't exists")

    database.cur.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (str(vote.post_id), curr_user['id']))
    like = database.cur.fetchone()
    if int(vote.dir) == 1:
        if like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {curr_user['id']} already liked the post {vote.post_id}")
        database.cur.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s) RETURNING *", (vote.post_id, curr_user['id']))
        new_like = database.cur.fetchone()
        database.conn.commit()

        return {"message" : "Like added successfully"}
    else:
        if not like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not found")
        database.cur.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (str(vote.post_id), curr_user['id']))
        database.conn.commit()
        
        return {"message" : "Like removed successfully"}
from fastapi import FastAPI
from .routers import post,user,auth,like

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)


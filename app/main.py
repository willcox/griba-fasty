from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote

# creation et mise a jour de la BD facon SQLACHEMY
# Ce dernier perd son utilité face a l'outil de migration `alembic`
# models.Base.metadata.create_all(bind=engine);

app = FastAPI();

# ********************* CORS *********************
# origins = ["*"]
origins = [
    "https://www.google.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
];
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
);


# ********************* POST *********************
app.include_router(post.router)

# ********************* USER *********************
app.include_router(user.router)

# ********************* AUTH *********************
app.include_router(auth.router)

# ********************* VOTE *********************
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello"};

# @app.post("/add/posts/py")
# async def add_posts(post: Post):
#     print(post);
#     print(post.dict());

#     return {"data": post};


from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import article
# from api import user, notification, questions, auth, like, answer, following, tag

#  Description of Context Aggregrator Api

description = """

Content Aggregator does the following functions

## Auth
This endpoint will handle all authorization requests including sign up, sign in, change password etc.

## Users 
These endpoint perform CRUD operations involving the user 

##  Article
These endpoint perform CRUD operations involving Articles 

Other Endpoints are implemented below 

## HTTP Methods
The following methods are used in this api :- 

* **GET** 
* **POST** 
* **UPDATE** 
* **DELETE** 
* **PATCH** 

"""

app = FastAPI(
    title="NEWS PODCAST",
    description=description
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

app.include_router(auth.router)
app.include_router(article.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}



from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2 # use to dots since going to app folder, so outside router 
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['Posts']) # instead of app = Fastapi.
#also add prefix to avoid wrting URL - posts, all the time.use Tags to separate url docs into diff sections

#GETTING ALL POSTS
#@router.get("/", response_model= List[schemas.Post]) # bracket is URL path. List ensures you get all the posts not just one.
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #put limit - query parameter, to determine how many posts user can get
                                                                    #skip to skip posts to get. set default to zero. Search query parameter
    
    print(limit)
    #posts = db.query(models.Post).all() 
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # limit the number of results (posts) with built in method and skip some
                                                            #contains is a method. allows to search for key word in the title.
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # to get only your post at 830hrs
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #print(results)   # count the number of votes. sqlalchemy is inner left join by default but we want outer.

    return posts # fastapi will convert posts to Jason


#@app.post("/createposts") # bracket is URL path
#def create_posts(payload: dict = Body(...)): #extract fields from Body, convert to "dict" and store in variable payload
 #    print(payload)
  #   return {"new post": f"title {payload['title']} content: {payload['content']}"}

# CREATING A POST and saving to memory with ID. whenever create a post http status 201 should be sent.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)): # post is a pydantic model that data is stored in. add oauth2 dependency to force user to log in b4 they can create a post
    
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **dict(post)) # 5:14hrs instead of - title =post.title,content = post.content, published = post.published # create new post
                            #add owner_id at 8:20 here instead of in schemas.py

    db.add(new_post) # adds the new post to database
    db.commit() # saving to database
    db.refresh(new_post) # similar to returning
    return new_post



#GETTING A SPECIFIC POST
#@app.get("/posts/{id}") # bracket is URL path. id is path parameter and is always a string. user is going to provide a ID of specific post they are interested in
#def get_post(id: int, response: Response): #add int as validation in case an error occursfrom the userthen no needfor int in next line. response so that clear error message is given
    #post = find_post(int(id)) # convert id to integer using int
    #post = find_post(id)
    #if not post:
     #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    #print(id)
    #return {"post_detail": f"here is post {id}"} 
    #return {"post_detail": post} 

#cleaner version of HTTP exception
@router.get("/{id}", response_model=schemas.PostOut) # bracket is URL path. id is path parameter and is always a string. user is going to provide a ID of specific post they are interested in
def get_post(id: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)): #add int as validation in case an error occursfrom the userthen no needfor int in next line. response so that clear error message is given
    #post = db.query(models.Post).filter(models.Post.id == id).first() # filter is similar to WHERE
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    return post 


#DELETING A POST. find the index in the arrray that has required ID; my_post
@router.delete("/{id}") # bracket is URL path
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)): 
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") # if ID is incorrect
    
    # to make sure user can only delete his post and not that of other users
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) # for 204 you do not want to send any data back

# UPDATING POSTS at 2:16hrs
@router.put("/{id}", response_model=schemas.Post) # bracket is URL path
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
Depends(oauth2.get_current_user)): # add Post here to follow the criteria defined in class Post above
    post_query = db.query(models.Post).filter(models.Post.id == id) # quesry to find post with specific id
    
    post = post_query.first() # grab the post and save in post
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist") # if ID is incorrect
    # to make sure user can only update his post and not that of other users
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
    
    post_query.update(dict(updated_post), synchronize_session = False) # instead of this= 
                        #{'title': 'this is my updated title', 'content': 'this is updated content'}. updates the query
    db.commit()
    return post_query.first() # sends back to the user

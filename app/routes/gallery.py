import io
from typing import List, Optional

from PIL import Image
from fastapi import APIRouter, Cookie, Form, status, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session

from ..database import crud, schemas, database

router = APIRouter(
    tags=["gallery"],
    prefix="/galleries"
)


@router.get('', response_model=Optional[List[schemas.Gallery]])
def get_all_galleries(db: Session = Depends(database.get_db)):
    galleries = crud.get_galleries(db)
    return galleries


@router.post('', response_model=schemas.Gallery)
def create_gallery(gallery: schemas.GalleryCreate,
                   db: Session = Depends(database.get_db)):
    return crud.create_gallery(db, gallery=gallery)

#
# @router.get('/img/{name}')
# async def img(name: str, logged_in: Optional[str] = Cookie(None)):
#     if logged_in is None:
#         return redirect_to_login()
#     d = database.get_db()
#     image = d.get_image(name)
#     return StreamingResponse(io.BytesIO(image['content']), media_type=image['content_type'])
#
#
# @router.get("/{username}")
# async def gallery(username: str, logged_in: Optional[str] = Cookie(None)):
#     if logged_in is None:
#         return redirect_to_login()
#     d = database.get_db()
#     images = d.get_images()
#     img = ""
#     for key in images:
#         image = images[key]
#         ratio = image['width'] / image['height']
#         height = int(200 * ratio)
#         img += f"""
#         <div style="border: 2px solid black; padding: 10px; margin: 10px; float: left;">
#             <img src="/gallery/img/{image['filename']}" alt="{image['title']}"
#                 style="width: 200px; height: {height}px; float: left" />
#             <h3 style="float: left; clear: left; margin: 5px 0;">{image['title']}</h3>
#             <h4 style="float: left; clear: left; margin: 0;">{image['subtitle']}</h4>
#         </div>
#         """
#
#     content = f"""
#     <h1>Picture Gallery</h1>
#     <p>Hello <b>{username}</b>,<br/><br/>Welcome to the best gallery in the whole world!!!</p>
#     <br/><br/>
#     {img}
#     <div style="clear: both"></div>
#     <br/><br/>
#     <div style="border: 1px solid black;">
#         <form action="/gallery/upload/" enctype="multipart/form-data" method="post" style="float: left">
#             Title: <input name="title" type="input">
#             <br/><br/>
#             Subtitle: <input name="subtitle" type="input">
#             <br/><br/>
#             File: <input name="file" type="file">
#             <br/><br/>
#             <input type="submit">
#         </form>
#         <div style="clear: both"></div>
#     </div>
#     <br/><br/><br/><br/>
#     <form method="post" action="/users/logout"><input type="button" onclick="submit()" value="Logout"/></form>
#     """
#     return HTMLResponse(content=content)
#
#
# class ImageInParams:
#     def __init__(self, title: str = Form(...), subtitle: str = Form(...)):
#         if not title:
#             raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Title must present")
#         self.title = title
#         self.subtitle = subtitle
#
#
# # https://fastapi.tiangolo.com/tutorial/request-files/
# @router.post("/upload/",
#              summary="Upload picture",
#              description="Upload picture and its title",
#              )
# async def upload_file(file: UploadFile = File(...),
#                       picture: ImageInParams = Depends(ImageInParams),
#                       logged_in: Optional[str] = Cookie(None)):
#     if logged_in is None:
#         return redirect_to_login()
#
#     content = await file.read()
#     await file.close()
#     image = Image.open(io.BytesIO(content))
#     width, height = image.size
#     d = database.get_db()
#     d.add_image({
#         "title": picture.title,
#         "subtitle": picture.subtitle,
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "file_size": len(content),
#         "content": content,
#         "width": width,
#         "height": height,
#     })
#     return RedirectResponse(url="/gallery/" + logged_in, status_code=status.HTTP_302_FOUND)

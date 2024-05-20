from fastapi import FastAPI, Request, Depends, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from singleton import DataBase
from utils import register_form_validator, login_form_validar, check_if_account_exists
import hashlib as hs
from auth import *

app = FastAPI()
app.mount('/static', StaticFiles(directory='../static'), name='static')
templates = Jinja2Templates('../templates')
db = DataBase()
auth_checker = AuthChecker()


@app.get('/', response_class= HTMLResponse)
async def load_main(request: Request):
    example_books = db.select_books_main()
    context = {'request': request, 'results': example_books}
    return templates.TemplateResponse('index.html', context)


@app.post('/search')
async def search_for_book(request: Request):
    form = await request.form()
    search = form.get('fraze')
    results = DataBase().select_search(search)
    context = {'request': request, 'results': results}
    return templates.TemplateResponse('search_temp.html', context)


@app.get('/my_books', response_class= HTMLResponse)
async def my_books(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('mybooks.html', context)


@app.get('/contact', response_class=HTMLResponse)
async def contact(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('contacts.html', context)


@app.get('/book-details/{id}', response_class=HTMLResponse)
async def book_details(request: Request, id: int):
    results = db.select_book_detail(id)
    context = {'request': request, 'results': results, 'id': id}
    return templates.TemplateResponse('book_info.html', context)


@app.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('register.html', context)


@app.post('/register')
async def get_register_data(request: Request):
    form = await request.form()
    first_name = form.get('name')
    last_name = form.get('lastname')
    email = form.get('email')
    password = form.get('password')
    password_hash = hs.sha1(password.encode()).hexdigest()
    phone = form.get('phone')
    if register_form_validator(first_name, last_name, email, password, phone):
        if check_if_account_exists(password_hash, email):
            context = {'request': request, 'message': 'account already exists'}
            return templates.TemplateResponse('register.html', context)
        DataBase().insert_user(first_name, last_name, email, phone, password_hash)
        return RedirectResponse('/', status_code=302)
    else:
        context = {'request' : request, 'message': 'wrong data, try again'}
        return templates.TemplateResponse('register.html', context)


@app.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)


@app.post('/login')
async def get_login_data(request: Request):
    user = None
    form = await request.form()
    email = form.get('email')
    password = form.get('password')
    password_hashed = hs.sha1(password.encode()).hexdigest()
    print(email, password_hashed)
    
    if login_form_validar(email, password):
        if DataBase().data_valid_login(password_hashed, email):
            token = auth_checker.encode_token(email)
            response = RedirectResponse(url="/", status_code=302)
            return response
        else:
            context = {'request': request, 'message': 'there is no account in the database'}
            return templates.TemplateResponse('login.html', context)
    else:
        context = {'request': request, 'message': 'wrong data, try again'}
        return templates.TemplateResponse('login.html', context)


@app.get('/rate/{book_id}', response_class=HTMLResponse)
async def rating(request: Request, book_id: int):
    context = {'request': request, 'book_id': book_id}
    return templates.TemplateResponse('rating.html', context)


@app.post('/submit-comment/{id}')
async def add_comment(request: Request, id: int):
    form = await request.form()
    rating = form.get('rating')
    comment = form.get('comment')
    user_id = form.get('id')
    book_id = id
    print(rating, comment, user_id, book_id)
    return None


@app.get('/order/{book_id}', response_class=HTMLResponse)
async def order(request: Request, book_id: int):
    results = DataBase().select_book_info_order(book_id)
    print(book_id)
    context = {'request': request, 'results': results, 'book_id': book_id}
    return templates.TemplateResponse('rent.html', context)


@app.post('/ordered/{book_id}')
async def order_post(request: Request, book_id: int):
    form = await request.form()
    adress = form.get('adress')
    street = form.get('street')
    city = form.get('city')
    print(adress, street, city, book_id)
    

@app.get('/protected')
def protected(user_data=Depends(auth_checker.auth_wrapper)):
    return {
        'email': user_data
    }
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        reload_includes=["*.html", "*.css", "*.js"],
        reload_dirs=["../templates", "../templates/static", "../static"],
    )
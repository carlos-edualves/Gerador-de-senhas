from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.generator import generate_password
from src.strength import evaluate_password_strength, get_password_strength

app = FastAPI()

templates = Jinja2Templates(directory="web/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    length: int = Form(...),
    numbers: bool = Form(False),
    symbols: bool = Form(False),
    uppercase: bool = Form(False),
    lowercase: bool = Form(False),
):
    try:
        password = generate_password(length, numbers, symbols, uppercase, lowercase)

        score = evaluate_password_strength(password)
        strength = get_password_strength(score)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "password": password,
                "strength": strength
            },
        )
        
    except ValueError as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e)
            }
        )
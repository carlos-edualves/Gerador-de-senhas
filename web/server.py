from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.generator import generate_password
from src.strength import evaluate_password_strength, get_password_strength
from src.logging_config import setup_logging
import logging
import uuid

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI()

templates = Jinja2Templates(directory="web/templates")

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    return response




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
    logger.info(
        "Requsição recebida",
        extra={
            "extra_data": {
                "event": "request_received",
                "request_id": request.state.request_id,
                "message": "Requisição recebida com sucesso",
                "status": "success"
            }
        }
    )

    if not any([uppercase, lowercase, numbers, symbols]):
        logger.warning(
        "Erro de validação",
        extra={
            "extra_data": {
                "event": "weak_password",
                "request_id": request.state.request_id,
                "message": "Nenhuma opção de caractere selecionado",
                "status": "error",
                }
            }
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Selecione pelo menos um tipo"
            },
        )

    if length < 6:
        logger.warning(
            "Erro de validação",
            extra={
                "extra_data": {
                    "event": "weak_password",
                    "request_id": request.state.request_id,
                    "message": "Senha com menos de 6 Dígitos",
                    "status": "error",
                    "length": length
                }
            }
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "A senha deve ter pelo menos 6 caracteres"
            }
        )
    

    try:
        password = generate_password(length, numbers, symbols, uppercase, lowercase)

        score = evaluate_password_strength(password)
        strength = get_password_strength(score)
        logger.info(
        "Senha gerada com sucesso",
        extra={
            "extra_data": {
                "event": "password_generated",
                "request_id": request.state.request_id,
                "message": "Senha com menos de 6 Dígitos",
                "status": "success",
                "length": length,
                "strength": strength
            }
        }
    )
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
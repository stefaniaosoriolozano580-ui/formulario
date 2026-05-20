from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mensajes_db = []

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="formulario.html",
        context={"ano_actual": datetime.now().year},
    )

@app.post("/enviar")
async def enviar_mensaje(
    autor: str = Form(...),
    mensaje: str = Form(...)
):
    mensajes_db.append({
        "autor": autor,
        "mensaje": mensaje
    })

    return RedirectResponse(
        url="/muro",
        status_code=303
    )

@app.get("/muro", response_class=HTMLResponse)
async def muro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="muro.html",
        context={
            "mensajes": mensajes_db,
            "año_actual": datetime.now().year,
        }
    )
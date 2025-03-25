from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from stripe import checkout

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/create-checkout-session/{tier}")
async def create_checkout(tier: str):
    prices = {
        "basic": "price_basic_id",
        "professional": "price_pro_id",
        "enterprise": "price_enterprise_id"
    }
    session = checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': prices[tier],
            'quantity': 1,
        }],
        mode='subscription',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return {"id": session.id}

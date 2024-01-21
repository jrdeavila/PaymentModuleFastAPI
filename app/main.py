from typing import Annotated, Union

import uvicorn
from api.routes import (
    on_trasanction_change_event,
    payment,
    terms_and_conditions,
    user_payments,
)
from core.application.exceptions.message_exception import MessageException
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from api.auth import auth_routes

# --------------------------- Variables ---------------------------
is_dev = True
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token", scheme_name="Application Token"
)
# -----------------------------------------------------------------

# --------------------------- Main App ----------------------------
app = FastAPI()
# -----------------------------------------------------------------


# ------------------------- Middlewares ---------------------------
@app.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["IP-Address"] = request.client.host
    return response


# -----------------------------------------------------------------

# ------------------------- Include Routers -----------------------
app.include_router(
    payment.router,
    prefix="/api/v1/payment",
    tags=["Payment"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(
    terms_and_conditions.router,
    prefix="/api/v1/terms-and-conditions",
    tags=["Terms and Conditions"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(
    on_trasanction_change_event.router,
    prefix="/api/v1/on-transaction-change-event",
    tags=["On Transaction Change Event"],
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(
    user_payments.router,
    prefix="/api/v1",
    tags=["User Payments"],
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(
    auth_routes.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)


# -----------------------------------------------------------------

# ------------------------- Exception Handlers --------------------


@app.exception_handler(MessageException)
async def message_exception_handler(request, exc: MessageException):
    return JSONResponse(
        status_code=exc.code,
        content={"name": f"Opps! {exc.name}", "message": exc.message},
    )


# -----------------------------------------------------------------


# ------------------------- Run Server ----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=is_dev)
# -----------------------------------------------------------------

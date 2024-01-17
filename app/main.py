from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from api.controllers.payment_controller import PaymentCtrl
from core.application.exceptions.message_exception import MessageException

# --------------------------- Variables ---------------------------
is_dev = True
# -----------------------------------------------------------------

# --------------------------- Main App ----------------------------
app = FastAPI()
# -----------------------------------------------------------------

# ------------------------- Include Routers -----------------------
app.include_router(
    PaymentCtrl().router,
    prefix="/api/v1/payment",
    tags=["Payment"],
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# -----------------------------------------------------------------

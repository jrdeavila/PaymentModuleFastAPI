from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from api.controllers.on_trasanction_change_event_controller import (
    OnTransactionChangeEventCtrl,
)

from api.controllers.payment_controller import PaymentCtrl
from api.controllers.terms_and_conditions_controller import TermsAndConditionController
from api.controllers.user_payments_controller import UserPaymentsController
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

app.include_router(
    TermsAndConditionController().router,
    prefix="/api/v1/terms-and-conditions",
    tags=["Terms and Conditions"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    OnTransactionChangeEventCtrl().router,
    prefix="/api/v1/on-transaction-change-event",
    tags=["On Transaction Change Event"],
)

app.include_router(
    UserPaymentsController().router,
    prefix="/api/v1",
    tags=["User Payments"],
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

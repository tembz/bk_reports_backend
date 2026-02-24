from datetime import datetime

from fastapi import APIRouter, Request, Depends

from src.database.methods.credit import get_db_credits, update_credit_status, add_new_credit
from src.tools.bot import send_credit_message_to_chat
from src.tools.responses import *
from src.tools.schemas import NewCredit

credit_handler = APIRouter(prefix="/api/credit")

@credit_handler.get("/get")
async def get_credits(limit: int = 30, offset: int = 0):
    credit_result = await get_db_credits(offset, limit)
    credit_list = []

    for credit in credit_result:
        credit_dict = credit.__dict__.copy()
        credit_dict.pop("_sa_instance_state", None)
        credit_dict.update({
            "credit_type": "взяли" if credit.credit_type == "take" else "дали",
        })

        credit_list.append(credit_dict)

    return HTTPSuccess({"items": credit_list})

@credit_handler.get("/toggle")
async def toggle_credit_status(credit_id: int):
    await update_credit_status(credit_id)
    return HTTPSuccess()

@credit_handler.post("/create")
async def create_new_credit(credit: NewCredit = Depends()):

    data = credit.model_dump()
    data["date"] = datetime.today()

    await send_credit_message_to_chat(data)
    await add_new_credit(data)
    return HTTPSuccess()
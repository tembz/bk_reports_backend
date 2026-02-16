from datetime import datetime

from fastapi import APIRouter, Request

from database.methods.credit import get_db_credits, update_credit_status, add_new_credit
from tools.bot import send_credit_message_to_chat

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

    return {
        "status": "success",
        "data": {
            "items": credit_list,
            "ok": True
        }
    }

@credit_handler.get("/toggle")
async def toggle_credit_status(credit_id: int):
    await update_credit_status(credit_id)
    return {"status": "success", "data": {"ok": True}}


@credit_handler.post("/create")
async def create_new_credit(request: Request):
    source = await request.json()
    data = {
        "date": datetime.today(),
        "restaurant": int(source.get("restaurant", 0)),
        "what_take": source.get("what_take", ""),
        "measurement_unit": source.get("measurement_unit", ""),
        "repayment_date": source.get("repayment_date", datetime.today()),
        "is_transfer": bool(source.get("is_transfer", False)),
        "credit_type": source.get("credit_type", ""),
        "count": float(source.get("count", 0))
    }
    await send_credit_message_to_chat(data)
    await add_new_credit(data)
    return {"status": "success", "data": {"ok": True}}
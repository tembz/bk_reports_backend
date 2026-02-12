from fastapi import APIRouter

from database.methods.credit import get_db_credits

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
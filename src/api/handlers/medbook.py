import logging

from fastapi import APIRouter, Request

from api.database.methods.medbook import add_new_book
from api.tools.schemas import NewMedBook
from api.tools.responses import HTTPSuccess

medbook = APIRouter("/api/medbook")
logger = logging.getLogger(__name__)

@medbook.post("/create")
async def create_new_book(request: Request):
    admin_id = request.state.admin_id
    data = NewMedBook.model_validate(request.form())
    logger.info(
        "creating report | admin_id=%s name=%s",
        admin_id,
        data.full_name
    )
    await add_new_book(data.full_name, data.inspect_end, data.fluorography_end, data.reference)
    return HTTPSuccess()

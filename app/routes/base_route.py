from fastapi import APIRouter, Request


router = APIRouter(
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


@router.get("/", status_code=200)
def catch_all(__: Request):
    return {"message": "running..."}

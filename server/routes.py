from fastapi import APIRouter
from server.stream_logs import read_logs_from_files

router = APIRouter()


@router.get("/stream", response_description="Start streaming")
async def parse_logs(start_date: str = '', end_date: str = '', per_page: int = 50):
    return await read_logs_from_files(start_date, end_date, per_page)

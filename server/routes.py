from fastapi import APIRouter
router = APIRouter()


@router.get("/process-file", response_description="Start streaming")
async def parse_logs(file_path: str = '', log_type: int = 0):
    return await process_log_file(file_path, log_type)

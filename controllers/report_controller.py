from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from services import report_service
from database import get_db
import os

router = APIRouter(prefix="/report")

@router.get("/weekly", response_class=FileResponse)
def get_weekly_report(db: Session = Depends(get_db)):
    """
    Generate and download the weekly PDF report.

    Args:
        db (Session): Database session.

    Returns:
        FileResponse: PDF file as downloadable response.

    Raises:
        HTTPException: If the PDF report file is not found.
    """
    pdf_path = report_service.generate_weekly_report_pdf() 

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename='weekly_report.pdf',
        headers={"Content-Disposition": "attachment; filename=weekly_report.pdf"}
    )

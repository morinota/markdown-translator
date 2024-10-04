from fastapi import APIRouter, File, UploadFile

from pdf_to_md_converter.app.services.pdf_extraction import extract_text_from_pdf_by_pypdf

router = APIRouter()


@router.post("/upload_pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...)) -> dict:
    raw_text = extract_text_from_pdf_by_pypdf(await pdf_file.read())
    return {"raw_text": raw_text}

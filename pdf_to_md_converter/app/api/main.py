from fastapi import FastAPI

from pdf_to_md_converter.app.api.pdf_summary import router as pdf_summary_router

app = FastAPI()

app.include_router(pdf_summary_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

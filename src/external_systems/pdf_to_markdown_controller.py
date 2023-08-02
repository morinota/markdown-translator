from services.pdf_content_extracter import PDFContentExtractor
from services.pdf_to_markdown_converter import PDF2MarkdownConverter


class PDF2MarkdownController:
    PDF_EQUATION_FONTNAMES = [
        "YNTGTF+CMR10",
    ]

    def __init__(self) -> None:
        self.extractor = PDFContentExtractor()
        self.converter = PDF2MarkdownConverter()

    def run(self, pdf_bytes: bytes) -> str:
        pdf_contents = self.extractor.extract(pdf_bytes)
        md_contents = self.converter.convert(pdf_contents)
        return ""

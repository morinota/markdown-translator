from markdown_reader.markdown_content_base import MarkdownContentBase
from markdown_reader.pdf_content_base import PDFContentBase


class PDF2MarkdownConverter:
    def __init__(self) -> None:
        pass

    def convert(
        self,
        pdf_contents: list[PDFContentBase],
    ) -> list[MarkdownContentBase]:
        return [pdf_content.raw_text for pdf_content in pdf_contents]

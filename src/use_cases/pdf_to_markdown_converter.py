from entities.markdown_content_base import MarkdownContentBase, MarkdownTagName
from entities.pdf_content_base import PDFContentBase


class PDF2MarkdownConverter:
    TAG_BY_LOWEST_FONTSIZE = {
        15: MarkdownTagName.HEADER_1,
        12: MarkdownTagName.HEADER_2,
        11: MarkdownTagName.HEADER_3,
    }

    def __init__(self) -> None:
        pass

    def convert(
        self,
        pdf_contents: list[PDFContentBase],
    ) -> list[MarkdownContentBase]:
        return [pdf_content.raw_text for pdf_content in pdf_contents]

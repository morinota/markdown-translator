from entities.pdf_content_base import PDFContentBase
from use_cases.pdf_content_extracter import PDFContentExtractor
from use_cases.pdf_to_markdown_converter import PDF2MarkdownConverter, PDFFontsToTagConfig


class PDF2MarkdownController:
    def __init__(self) -> None:
        self.extractor = PDFContentExtractor()
        self.converter = PDF2MarkdownConverter()

    def run(self, pdf_bytes: bytes) -> str:
        pdf_contents = self.extractor.extract(pdf_bytes)
        self._debug(pdf_contents)
        md_contents = self.converter.convert(pdf_contents)
        return ""

    def _debug(self, pdf_contents: list[PDFContentBase]) -> None:
        for pdf_content in pdf_contents:
            if pdf_content.fontname_mode in PDFFontsToTagConfig.HEADERS_FONTS:
                continue
                print(
                    pdf_content.raw_text, pdf_content.content_type, pdf_content.fontname_mode, pdf_content.fontsize_mode
                )
            if pdf_content.fontname_mode in PDFFontsToTagConfig.EQUATION_FONTS:
                continue
            print(pdf_content.raw_text, pdf_content.content_type, pdf_content.fontname_mode, pdf_content.fontsize_mode)

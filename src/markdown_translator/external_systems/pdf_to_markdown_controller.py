from entities.pdf_content_base import PDFContentBase
from markdown_reader.md_input_output import MarkdownGenerator
from use_cases.pdf_2_md_tag_classfier import PDFFontsToTagConfig
from use_cases.pdf_content_extracter import PDFContentExtractor
from use_cases.pdf_to_markdown_converter import PDF2MarkdownConverter


class PDF2MarkdownController:
    def __init__(self) -> None:
        self.extractor = PDFContentExtractor()
        self.converter = PDF2MarkdownConverter()
        self.generator = MarkdownGenerator()

    def run(self, pdf_bytes: bytes) -> str:
        pdf_contents = self.extractor.extract(pdf_bytes)
        self._debug(pdf_contents)

        md_contents = self.converter.convert(pdf_contents)

        return self.generator.generage(md_contents)

    def _debug(self, pdf_contents: list[PDFContentBase]) -> None:
        for pdf_content in pdf_contents:
            if pdf_content.fontname_mode in PDFFontsToTagConfig.HEADERS_FONTS:
                # print(
                #     pdf_content.raw_text,
                #     pdf_content.content_type,
                #     pdf_content.fontname_mode,
                #     pdf_content.fontsize_mode,
                # )
                continue
            if pdf_content.fontname_mode in PDFFontsToTagConfig.EQUATION_FONTS:
                continue
            if pdf_content.raw_text == "\n":
                print(
                    pdf_content.raw_text,
                    pdf_content.content_type,
                    pdf_content.fontname_mode,
                    pdf_content.fontsize_mode,
                )

from entities.markdown_content_base import MarkdownContentBase, MarkdownTagName
from entities.pdf_content_base import PDFContentBase


class PDFFontsToTagConfig:
    EQUATION_FONTS = ["YNTGTF+CMR10"]
    HEADERS_FONTS = ["ZEAUGF+NimbusRomNo9L-Medi"]
    PLAIN_TEXT_FONTS = []


class PDF2MarkdownConverter:
    TAG_BY_LOWEST_FONTSIZE = {
        MarkdownTagName.HEADER_1: 15,
        MarkdownTagName.HEADER_2: 12,
        MarkdownTagName.HEADER_3: 11,
    }

    def __init__(self) -> None:
        pass

    def convert(
        self,
        pdf_contents: list[PDFContentBase],
    ) -> list[MarkdownContentBase]:
        md_contents = []
        previous_fontsize = None
        previous_fontname = None
        for pdf_content in pdf_contents:
            if self._is_headers_tag(pdf_content):
                md_contents.append(MarkdownContentBase(self._clasify_header_type(pdf_content), pdf_content.raw_text))

        return md_contents

    def _is_headers_tag(self, pdf_content: PDFContentBase) -> bool:
        """headers tagか否かを判定してboolを返す。"""
        if pdf_content.fontname_mode not in PDFFontsToTagConfig.HEADERS_FONTS:
            return False
        if pdf_content.fontsize_mode < self.TAG_BY_LOWEST_FONTSIZE[MarkdownTagName.HEADER_3]:
            return False
        return True

    def _clasify_header_type(self, pdf_content: PDFContentBase) -> MarkdownTagName:
        """どのheaderかを判定して返す"""
        fontsize = pdf_content.fontsize_mode
        fontname = pdf_content.fontname_mode
        if fontsize >= self.TAG_BY_LOWEST_FONTSIZE[MarkdownTagName.HEADER_1]:
            return MarkdownTagName.HEADER_1
        elif fontsize >= self.TAG_BY_LOWEST_FONTSIZE[MarkdownTagName.HEADER_2]:
            return MarkdownTagName.HEADER_2
        elif fontsize >= self.TAG_BY_LOWEST_FONTSIZE[MarkdownTagName.HEADER_3]:
            return MarkdownTagName.HEADER_3
        return MarkdownTagName.HEADER_4

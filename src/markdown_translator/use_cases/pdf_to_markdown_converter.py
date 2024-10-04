import re
from entities.markdown_content_base import MarkdownContentBase, MarkdownTagName
from entities.pdf_content_base import PDFContentBase
from use_cases.pdf_2_md_tag_classfier import PDF2MdTagClassifier


class PDF2MarkdownConverter:
    def __init__(self) -> None:
        self.md_tag_classifier = PDF2MdTagClassifier()

    def convert(
        self,
        pdf_contents: list[PDFContentBase],
    ) -> list[MarkdownContentBase]:
        md_contents: list[MarkdownContentBase] = []
        previous_md_type = None
        for pdf_content in pdf_contents:
            md_tag = self.md_tag_classifier.classify(pdf_content)
            raw_text = ""

            if md_tag == MarkdownTagName.PLAIN_TEXT and previous_md_type == MarkdownTagName.PLAIN_TEXT:
                previous_plain_text_md = md_contents.pop()
                raw_text += previous_plain_text_md.text_raw + " "

            raw_text += pdf_content.raw_text
            raw_text_processed = re.sub(r"\n", "", raw_text)  # pdfの全てのtextlineに含まれている改行文字を削除
            md_content = MarkdownContentBase(
                md_tag,
                raw_text_processed,
            )
            md_contents.append(md_content)
            previous_md_type = md_content.tag_name
        return md_contents

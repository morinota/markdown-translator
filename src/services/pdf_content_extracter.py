import abc
from io import BytesIO
from pathlib import Path
from statistics import mode
from typing import Optional

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTChar, LTContainer, LTItem, LTTextLine, LTTextLineHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

from markdown_reader.pdf_content_base import PDFContentBase


class PDFContentExtractorInterface(abc.ABC):
    @abc.abstractmethod
    def extract(self) -> list[PDFContentBase]:
        raise NotImplementedError


class PDFContentExtractor(PDFContentExtractorInterface):
    def __init__(self) -> None:
        pass

    def extract(self, pdf_bytes: Optional[bytes] = None) -> list[PDFContentBase]:
        if pdf_bytes is None:
            return list()
        parser = PDFParser(BytesIO(pdf_bytes))
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        laparams = LAParams(all_texts=True)
        resource_manager = PDFResourceManager()
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)

        results: list[PDFContentBase] = []
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            print("objs------------------")
            self._get_pdf_contents(layout, results)
        for pdf_content in results:
            if pdf_content.fontsize_mode >= 15:
                print(pdf_content.raw_text, pdf_content.fontname_mode)

        self._save_raw_data(results)

        return results

    def _get_pdf_contents(self, layout: LTContainer, results: list[PDFContentBase]) -> None:
        """再帰的にlayoutの中を探索し、LTTextLine型のオブジェクト(テキスト行)
        を見つけた場合にその情報をresultsに追加する。
        振る舞いとしては、図表内のTextLineは無視する。
        """
        # print(f"type of layout: {type(layout)}")
        if not isinstance(layout, LTContainer):
            return
        for obj in layout:
            if isinstance(obj, LTTextLine):
                char_fontsize = mode([char.size for char in obj if isinstance(char, LTChar)])
                char_fontname = mode([char.fontname for char in obj if isinstance(char, LTChar)])
                # print(char_fontsize)
                # print(char_fontname)
                results.append(
                    PDFContentBase(
                        bbox=obj.bbox,
                        raw_text=obj.get_text(),
                        content_type=type(obj),
                        fontsize_mode=char_fontsize,
                        fontname_mode=char_fontname,
                    )
                )
            self._get_pdf_contents(obj, results)

    def _save_raw_data(self, results: list[PDFContentBase]) -> None:
        log_path = Path("extracted_pdf_data_log.md")
        with log_path.open("w", encoding="utf-8") as file:
            file.write("\n".join(str(content) for content in results))

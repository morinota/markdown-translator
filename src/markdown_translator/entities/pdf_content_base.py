import dataclasses
from enum import Enum
from typing import Any

from pdfminer.layout import LTTextLine
from pdfminer.layout import (
    LAParams,
    LTChar,
    LTContainer,
    LTItem,
    LTTextLine,
    LTTextLineHorizontal,
    LTAnno,
    LTFigure,
    LTTextBoxHorizontal,
)


class PDFContentTypes:
    TEXT_LINE_HORIZONTAL = LTTextLineHorizontal
    ANNOTATION = LTAnno
    FIGURE = LTFigure
    TEXT_BOX_HORIZONTAL = LTTextBoxHorizontal


@dataclasses.dataclass
class PDFContentBase:
    # bbox: tuple
    raw_text: str
    content_type: type
    fontsize_mode: int
    fontname_mode: str

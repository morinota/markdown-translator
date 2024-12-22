import dataclasses
from enum import Enum
from typing import Any

from pdfminer.layout import (
    LAParams,
    LTAnno,
    LTChar,
    LTContainer,
    LTFigure,
    LTItem,
    LTTextBoxHorizontal,
    LTTextLine,
    LTTextLineHorizontal,
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

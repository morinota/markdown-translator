import dataclasses
from typing import Any

from pdfminer.layout import LTTextLine


@dataclasses.dataclass
class PDFContentBase:
    bbox: tuple
    raw_text: str
    content_type: type
    fontsize_mode: float
    fontname_mode: str

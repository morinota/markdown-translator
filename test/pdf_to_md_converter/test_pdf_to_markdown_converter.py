import pytest

from src.markdown_reader.pdf_content_base import PDFContentBase
from src.services.pdf_to_markdown_converter import PDF2MarkdownConverter


def test_pdf_content_is_converted_to_markdown_content() -> None:
    # Arrange
    pdf_contents = []
    sut = PDF2MarkdownConverter
    # Act

    # Assert

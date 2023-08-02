import pytest

from entities.markdown_content_base import MarkdownContentBase
from entities.pdf_content_base import PDFContentBase, PDFContentTypes
from use_cases.pdf_to_markdown_converter import PDF2MarkdownConverter
import pdfminer


def test_pdf_content_is_converted_to_markdown_content() -> None:
    # Arrange
    pdf_contents = [
        PDFContentBase(
            bbox=None,
            raw_text="Off-Policy Evaluation for Large Action Spaces via Embeddings\n",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=18.0,
            fontname_mode="ZEAUGF+NimbusRomNo9L-Medi",
        ),
    ]
    sut = PDF2MarkdownConverter()

    # Act
    md_contents = sut.convert(pdf_contents)

    # Assert
    md_contents_expected = [MarkdownContentBase()]
    assert md_contents == md_contents_expected

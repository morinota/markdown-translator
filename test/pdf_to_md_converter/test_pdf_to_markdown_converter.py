import pytest

from entities.markdown_content_base import MarkdownContentBase, MarkdownTagName
from entities.pdf_content_base import PDFContentBase, PDFContentTypes
from use_cases.pdf_to_markdown_converter import PDF2MarkdownConverter, PDFFontsToTagConfig
import pdfminer


def test_continuous_pdf_contents_without_headers_font_are_joined_and_converted_to_plaintext_md_content() -> None:
    # Arrange
    pdf_contents = [
        PDFContentBase(
            bbox=(),
            raw_text="Off-Policy Evaluation for Large Action Spaces via Embeddings\n",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=18,
            fontname_mode=PDFFontsToTagConfig.HEADERS_FONTS[0],
        ),
    ]
    sut = PDF2MarkdownConverter()

    # Act
    md_contents = sut.convert(pdf_contents)

    # Assert
    md_contents_expected = [
        MarkdownContentBase(
            MarkdownTagName.HEADER_1,
            "Off-Policy Evaluation for Large Action Spaces via Embeddings\n",
        )
    ]
    assert md_contents == md_contents_expected


def test_continuous_pdf_contents_without_headers_font_are_joined_and_converted_to_plaintext_md_content() -> None:
    # Arrange
    pdf_contents = [
        PDFContentBase(
            bbox=(),
            raw_text="Off-Policy Evaluation for Large Action Spaces via Embeddings\n",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=18,
            fontname_mode=PDFFontsToTagConfig.HEADERS_FONTS[0],
        ),
    ]
    sut = PDF2MarkdownConverter()

    # Act
    md_contents = sut.convert(pdf_contents)

    # Assert
    md_contents_expected = [
        MarkdownContentBase(
            MarkdownTagName.HEADER_1,
            "Off-Policy Evaluation for Large Action Spaces via Embeddings\n",
        )
    ]
    assert md_contents == md_contents_expected

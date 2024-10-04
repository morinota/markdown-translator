from markdown_translator.entities.markdown_content_base import (
    MarkdownContentBase,
    MarkdownTagName,
)
from markdown_translator.entities.pdf_content_base import (
    PDFContentBase,
    PDFContentTypes,
)
from markdown_translator.use_cases.pdf_2_md_tag_classfier import PDFFontsToTagConfig
from markdown_translator.use_cases.pdf_to_markdown_converter import (
    PDF2MarkdownConverter,
)


def test_pdf_content_with_large_fontsize_is_converted_to_h1_md_content() -> None:
    # Arrange
    pdf_contents = [
        PDFContentBase(
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
            "Off-Policy Evaluation for Large Action Spaces via Embeddings",
        )
    ]
    assert md_contents == md_contents_expected


def test_continuous_pdf_contents_without_headers_font_are_joined_and_converted_to_plaintext_md_content() -> (
    None
):
    # Arrange
    pdf_contents = [
        PDFContentBase(
            raw_text="A is regard as\n",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=12,
            fontname_mode=PDFFontsToTagConfig.PLAIN_TEXT_FONTS[0],
        ),
        PDFContentBase(
            raw_text="the B. C will be D.\n",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=12,
            fontname_mode=PDFFontsToTagConfig.PLAIN_TEXT_FONTS[0],
        ),
    ]
    sut = PDF2MarkdownConverter()

    # Act
    md_contents = sut.convert(pdf_contents)

    # Assert
    md_contents_expected = [
        MarkdownContentBase(
            MarkdownTagName.PLAIN_TEXT,
            "A is regard as the B. C will be D.",
        )
    ]
    assert md_contents == md_contents_expected


def test_pdf_content_with_equation_font_is_converted_to_equation_md_content() -> None:
    # Arrange
    pdf_contents = [
        PDFContentBase(
            raw_text="Bias(j) + CNF(m)",
            content_type=PDFContentTypes.TEXT_LINE_HORIZONTAL,
            fontsize_mode=12,
            fontname_mode=PDFFontsToTagConfig.EQUATION_FONTS[0],
        ),
    ]
    sut = PDF2MarkdownConverter()

    # Act
    md_contents = sut.convert(pdf_contents)

    # Assert
    md_contents_expected = [
        MarkdownContentBase(
            MarkdownTagName.EQUATION,
            "Bias(j) + CNF(m)",
        )
    ]
    assert md_contents == md_contents_expected

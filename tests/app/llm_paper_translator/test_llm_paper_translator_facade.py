import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from markdown_translator.app.llm_paper_translator.llm_paper_translator_facade import (
    LlmPaperTranslatorFacade,
    is_pdf_url,
    download_pdf,
)


class TestLlmPaperTranslatorFacade:
    def test_run_should_add_refs_line_to_output_markdown_for_pdf_input(self):
        """PDFファイルを入力とした場合、出力Markdownファイルの1行目にrefs行が追加されること"""
        facade = LlmPaperTranslatorFacade()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # テスト用のPDFファイルパスを設定（実際のファイルは存在しなくてもよい）
            input_pdf_path = "/path/to/test.pdf"
            output_md_path = Path(temp_dir) / "output.md"
            
            # PDFからMarkdownへの変換をモック
            with patch("pymupdf4llm.to_markdown", return_value="# Test Content\nThis is test content."), \
                 patch("pathlib.Path.exists", return_value=True), \
                 patch.object(facade, "_translator_chain") as mock_chain:
                
                mock_chain.invoke.return_value = "# テストコンテンツ\nこれはテストコンテンツです。"
                
                facade.run(input_pdf_path, output_md_path)
                
                # 出力ファイルの内容を確認
                output_content = output_md_path.read_text()
                lines = output_content.split('\n')
                
                # 1行目にrefs行が含まれていることを確認
                assert lines[0] == f"refs: {input_pdf_path}"
                # 2行目以降に翻訳されたコンテンツが含まれていることを確認
                assert "# テストコンテンツ" in output_content

    def test_run_should_add_refs_line_to_output_markdown_for_url_input(self):
        """WebページURLを入力とした場合、出力Markdownファイルの1行目にrefs行が追加されること"""
        facade = LlmPaperTranslatorFacade()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_url = "https://example.com/test-page"
            output_md_path = Path(temp_dir) / "output.md"
            
            # WebページからMarkdownへの変換をモック
            mock_document = Mock()
            mock_document.model_dump.return_value = {"page_content": "<html><body><h1>Test</h1></body></html>"}
            
            with patch("markdown_translator.app.llm_paper_translator.llm_paper_translator_facade.AsyncChromiumLoader") as mock_loader, \
                 patch("markdown_translator.app.llm_paper_translator.llm_paper_translator_facade.parse_html_to_markdown") as mock_parser, \
                 patch.object(facade, "_translator_chain") as mock_chain:
                
                mock_loader.return_value.load.return_value = [mock_document]
                mock_parser.return_value = "# Test Content\nThis is test content."
                mock_chain.invoke.return_value = "# テストコンテンツ\nこれはテストコンテンツです。"
                
                facade.run(input_url, output_md_path)
                
                # 出力ファイルの内容を確認
                output_content = output_md_path.read_text()
                lines = output_content.split('\n')
                
                # 1行目にrefs行が含まれていることを確認
                assert lines[0] == f"refs: {input_url}"
                # 2行目以降に翻訳されたコンテンツが含まれていることを確認
                assert "# テストコンテンツ" in output_content


class TestIsPdfUrl:
    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://arxiv.org/pdf/1809.06473", True),
            ("https://example.com/paper.pdf", True),
            ("https://example.com/paper.PDF", True),
            ("http://example.com/document.pdf", True),
            ("https://example.com/page.html", False),
            ("https://example.com/index", False),
            ("https://example.com", False),
        ],
    )
    def test_should_detect_pdf_url_correctly(self, url: str, expected: bool):
        """URLがPDFを指しているかを正しく判定できること"""
        assert is_pdf_url(url) == expected


class TestDownloadPdf:
    def test_should_download_pdf_from_url_to_local_path(self):
        """PDF URLからローカルにPDFをダウンロードできること"""
        with tempfile.TemporaryDirectory() as temp_dir:
            url = "https://example.com/test.pdf"
            output_path = Path(temp_dir) / "downloaded.pdf"
            mock_pdf_content = b"PDF content"

            with patch("requests.get") as mock_get:
                mock_response = Mock()
                mock_response.content = mock_pdf_content
                mock_get.return_value = mock_response

                download_pdf(url, output_path)

                # リクエストが正しく呼ばれたことを確認
                mock_get.assert_called_once_with(url)

                # ファイルが正しく保存されたことを確認
                assert output_path.exists()
                assert output_path.read_bytes() == mock_pdf_content
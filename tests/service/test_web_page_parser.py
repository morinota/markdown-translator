import pytest

from markdown_translator.service.web_page_parser import parse_html_to_markdown


def _normalize_md(text: str) -> str:
    """生成後のmarkdownの正誤を比較しやすいように、余分な空白や改行を削除"""
    return "\n".join(line.strip() for line in text.strip().splitlines())


class TestWebPageParser:
    def test_シンプルなHTMLはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                <h1>Welcome</h1>
                <p>This is a test paragraph.</p>
            </body>
        </html>
        """

        result = parse_html_to_markdown(html)

        expected_markdown = """
        # Welcome
        This is a test paragraph.
        """
        assert _normalize_md(result) == _normalize_md(expected_markdown)

    def test_ヘッダーと本文とコードブロックを含むHTMLはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                <h1>Introduction</h1>
                <p>This is the introduction text.</p>
                <h2>Details</h2>
                <p>Here are some details.</p>
                <pre><code>def hello():\n    return "Hello, world!"</code></pre>
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        expected_markdown = """
        # Introduction
        This is the introduction text.
        ## Details
        Here are some details.
        ```
        def hello():
            return "Hello, world!"
        ```
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

    def test_空のHTMLの場合は空の文字列に変換される(self):
        html = """
        <html>
            <body></body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        assert actual == ""

    def test_ネストされたHTMLはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                <h1>Outer Header</h1>
                <div>
                    <h2>Inner Header</h2>
                    <p>Nested paragraph text.</p>
                </div>
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        expected_markdown = """
        # Outer Header
        ## Inner Header
        Nested paragraph text.
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

    def test_タグに囲まれていないプレーンテキストはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                This is plain text before any tags.
                <h1>Header</h1>
                <p>Paragraph text.</p>
                More plain text after the paragraph.
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        expected_markdown = """
        This is plain text before any tags.
        # Header
        Paragraph text.
        More plain text after the paragraph.
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

    def test_連番なしの箇条書きを含むHTMLはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                <h1>Header</h1>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        expected_markdown = """
        # Header
        - Item 1
        - Item 2
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

    def test_連番ありの箇条書きを含むHTMLはmarkdown形式に変換される(self):
        html = """
        <html>
            <body>
                <h1>Header</h1>
                <ol>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ol>
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)

        expected_markdown = """
        # Header
        1. Item 1
        2. Item 2
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

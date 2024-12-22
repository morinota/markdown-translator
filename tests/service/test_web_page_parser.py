import pytest

from markdown_translator.service.web_page_parser import parse_html_to_markdown


@pytest.mark.parametrize(
    "test_name, html, expected_markdown",
    [
        (
            "シンプルなHTMLの例",
            """
            <html>
                <body>
                    <h1>Welcome</h1>
                    <p>This is a test paragraph.</p>
                </body>
            </html>
            """,
            """
            # Welcome
            This is a test paragraph.
            """,
        ),
        (
            "ヘッダー、本文、コードブロックの例",
            """
            <html>
                <body>
                    <h1>Introduction</h1>
                    <p>This is the introduction text.</p>
                    <h2>Details</h2>
                    <p>Here are some details.</p>
                    <pre><code>def hello():\n    return "Hello, world!"</code></pre>
                </body>
            </html>
            """,
            """
            # Introduction
            This is the introduction text.
            ## Details
            Here are some details.
            ```
            def hello():
                return "Hello, world!"
            ```
            """,
        ),
        (
            "空のHTMLの場合",
            """
            <html>
                <body></body>
            </html>
            """,
            "",
        ),
        (
            "ネストされたHTMLの場合",
            """
            <html>
                <body>
                    <h1>Outer Header</h1>
                    <div>
                        <h2>Inner Header</h2>
                        <p>Nested paragraph text.</p>
                    </div>
                </body>
            </html>
            """,
            """
            # Outer Header
            ## Inner Header
            Nested paragraph text.
            """,
        ),
        (
            "タグに囲まれていないプレーンテキスト",
            """
            <html>
                <body>
                    This is plain text before any tags.
                    <h1>Header</h1>
                    <p>Paragraph text.</p>
                    More plain text after the paragraph.
                </body>
            </html>
            """,
            """
            This is plain text before any tags.
            # Header
            Paragraph text.
            More plain text after the paragraph.
            """,
        ),
        (
            "連番なしの箇条書きを含むHTMLの場合",
            """
            <html>
                <body>
                    <h1>Header</h1>
                    <ul>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ul>
                </body>
            </html>
            """,
            """
            # Header
            - Item 1
            - Item 2
            """,
        ),
        (
            "連番ありの箇条書きを含むHTMLの場合",
            """
            <html>
                <body>
                    <h1>Header</h1>
                    <ol>
                        <li>Item 1</li>
                        <li>Item 2</li>
                    </ol>
                </body>
            </html>
            """,
            """
            # Header
            1. Item 1
            2. Item 2
            """,
        ),
    ],
)
def test_HTML形式の文字列をMarkdown形式の文字列にparseする(test_name: str, html: str, expected_markdown: str):
    result = parse_html_to_markdown(html)
    print("==========")
    print(result)
    print("==========")
    assert _normalize_md(result) == _normalize_md(expected_markdown), f"Failed test: {test_name}"


def _normalize_md(text: str) -> str:
    # 余分な空白や改行を削除
    return "\n".join(line.strip() for line in text.strip().splitlines())

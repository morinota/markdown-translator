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

    def test_spanタグやdivタグにもいい感じに対応する(self):
        html = """
        <html>
            <body>
                <div class="entry-content prose prose-doordash pb-20 max-w-none">
                    <a href="https://doordash.engineering/2018/07/20/how-artificial-intelligence-powers-logistics-at-doordash/"><span style="font-weight: 400;">DoorDash uses Machine Learning</span></a><span style="font-weight: 400;"> (ML) at various places like inputs to </span><a href="https://doordash.engineering/2020/02/28/next-generation-optimization-for-dasher-dispatch-at-doordash/"><span style="font-weight: 400;">Dasher Assignment Optimization</span></a><span style="font-weight: 400;">, balancing Supply &amp; Demand, Fraud prediction, Search Ranking, Menu classification, Recommendations etc. As the usage of ML models increased, there grew a need for a holistic ML Platform to increase the productivity of shipping ML-based solutions. This kick-started an effort to build an ML Platform for DoorDash.</span>

                <span style="font-weight: 400;">The ML Platform consists of two critical pieces: first the infrastructure needed for ML to work at scale, and second a productive environment for engineers and data scientists to build their models. Scalability and productivity are the key driving factors in the decision making process for us.</span>
                <h3><span style="font-weight: 400;">Scenarios and Requirements</span></h3>
                <span style="font-weight: 400;">As we dug into ML usage at DoorDash, the following key scenarios for ML emerged:</span>
    
            </body>
        </html>
        """

        actual = parse_html_to_markdown(html)
        print(actual)

        expected_markdown = """
        DoorDash uses Machine Learning (ML) at various places like inputs to Dasher Assignment Optimization, balancing Supply &amp; Demand, Fraud prediction, Search Ranking, Menu classification, Recommendations etc. As the usage of ML models increased, there grew a need for a holistic ML Platform to increase the productivity of shipping ML-based solutions. This kick-started an effort to build an ML Platform for DoorDash.

        ### Scenarios and Requirements
        As we dug into ML usage at DoorDash, the following key scenarios for ML emerged:
        """
        assert _normalize_md(actual) == _normalize_md(expected_markdown)

from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from loguru import logger
from playwright.sync_api import sync_playwright


def parse_html_to_markdown(html: str) -> str:
    """HTML形式の文字列をMarkdown形式の文字列に変換する
    - h1, h2, h3タグをMarkdownのヘッダーに変換
    - pタグをMarkdownの本文に変換
    - preタグをMarkdownのコードブロックに変換

    """
    soup = BeautifulSoup(html, "html.parser")
    markdown_parts = []

    # 順序を保ちながらHTMLツリーを走査
    elements = list(soup.body.descendants)
    for element in elements:
        # タグの場合
        if element.name:
            markdown_part = _parse_by_tag(element)
            if not markdown_part:
                continue
            markdown_parts.append(markdown_part)

        # 最も子供なテキストノードの場合
        elif isinstance(element, NavigableString):
            parent = element.parent
            # body直下のタグで囲まれていないプレーンテキストの場合のみ追加
            if parent.name == "body":
                text = element.strip()
                if text:  # 空白や改行だけのテキストは無視
                    markdown_parts.append(text)

    return "\n".join(markdown_parts)


def _parse_by_tag(element: NavigableString) -> str | None:
    print(type(element))
    if element.name in ["h1", "h2", "h3"]:
        level = int(element.name[1])
        return f"{'#' * level} {element.get_text(strip=True)}"

    elif element.name == "p":
        return element.get_text(strip=True)

    elif element.name == "pre":
        code_content = element.get_text(strip=True)
        return f"```\n{code_content}\n```"

    # 箇条書きの場合
    elif element.name == "ul":
        items = [f"- {li.get_text(strip=True)}" for li in element.find_all("li")]
        return "\n".join(items)
    # 連番つき箇条書きの場合
    elif element.name == "ol":
        items = [f"{i+1}. {li.get_text(strip=True)}" for i, li in enumerate(element.find_all("li"))]
        return "\n".join(items)
    return None


def save_webpage_as_pdf(url: str, output_path: Path) -> None:
    """指定したURLのWebページをPDF形式のファイルとして保存する"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # 指定したURLを開く
        page.goto(url)

        # PDFとして保存
        page.pdf(path=output_path, format="A4", print_background=True)

        browser.close()
    logger.info(f"Webpage saved as PDF at: {output_path}")

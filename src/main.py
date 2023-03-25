import sys
from pathlib import Path
from typing import List

import websockets
from selenium import webdriver

from markdown_reader.markdown_content_class import MarkdownContent
from markdown_reader.md_input_output import MarkdownCreator, MarkdownReader
from markdown_translator.md_translator import MarkdownTranslatorWrapper

WINDOWS_ENCODE = "utf-8"

"""
- chrome driverのversion更新:
    - https://chromedriver.chromium.org/downloads より 自身のchromeのversionと合致するchrome driverをインストールして置き換える.
    - chrome driverの置き場所は"C:\Program Files\chromedriver.exe"
"""


def print_md_contents(md_contents: List[MarkdownContent]) -> None:
    for md_content in md_contents:
        print(md_content.text_raw)


def main(input_md_path: Path) -> None:
    raw_str = input_md_path.read_text(encoding=WINDOWS_ENCODE)
    markdown_reader = MarkdownReader()
    md_contents = markdown_reader.read(raw_str)

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    md_translator = MarkdownTranslatorWrapper(
        driver=webdriver.Chrome(options=options),
    )
    md_contents_translated = md_translator.translate(md_contents, correspond=True)
    md_string = "\n\n".join(
        [md_content.to_str() for md_content in md_contents_translated],
    )

    output_path = Path(input_md_path.parent, f"{input_md_path.stem}_trans.md")

    print(MarkdownCreator.save_as_md(str(output_path), md_string))


if __name__ == "__main__":

    # NOTE: 動作確認の場合は、sample_markdown.mdを指定する.
    input_md_path_str = sys.argv[1]  # NOTE: idx=0はスクリプトファイル名になってしまう.

    print(f"Translate .md document : {input_md_path_str}")

    main(input_md_path=Path(input_md_path_str))

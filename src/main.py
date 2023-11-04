import sys
from pathlib import Path
from typing import List

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from entities.markdown_content_class import MarkdownContent
from markdown_reader.md_input_output import MarkdownExporter, MarkdownParser
from markdown_translator.md_translator import MarkdownTranslatorWrapper

WINDOWS_ENCODE = "utf-8"

"""
- chrome driverのversion更新:
    - https://chromedriver.chromium.org/downloads より 自身のchromeのversionと合致するchrome driverをインストールして置き換える.
    - chrome driverの置き場所は"C:\Program Files\chromedriver.exe"

- 以下のよくわからないエラーが起こる場合、多分chrome driverとSeleniumのversionが一致しないのかも?? でも動作には悪影響はない。
[21656:26652:1102/194354.534:ERROR:cert_issuer_source_aia.cc(36)] Error parsing cert retrieved from AIA (as DER):
ERROR: Couldn't read tbsCertificate as SEQUENCE
ERROR: Failed parsing Certificate

"""


def print_md_contents(md_contents: List[MarkdownContent]) -> None:
    for md_content in md_contents:
        print(md_content.text_raw)


def main(input_md_path: Path) -> None:
    raw_str = input_md_path.read_text(encoding=WINDOWS_ENCODE)

    markdown_parser = MarkdownParser()
    md_contents = markdown_parser.parse(raw_str)

    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(options, service)

    md_translator_wrapper = MarkdownTranslatorWrapper(chrome_driver)
    md_contents_translated = md_translator_wrapper.translate(md_contents, correspond=True)

    output_path = Path(input_md_path.parent, f"{input_md_path.stem}_trans.md")
    md_string = "\n\n".join([md_content.to_str() for md_content in md_contents_translated])
    print(MarkdownExporter.save_as_md(str(output_path), md_string))


if __name__ == "__main__":
    # NOTE: 動作確認の場合は、sample_markdown.mdを指定する.
    input_md_path = Path(sys.argv[1])  # NOTE: idx=0はスクリプトファイル名になってしまう。

    print(f"Translate .md document : {str(input_md_path)}")

    main(input_md_path)

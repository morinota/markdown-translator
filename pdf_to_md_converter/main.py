import sys
from pathlib import Path

from app.services.pdf_extraction import extract_text_from_pdf_by_pypdf

WINDOWS_ENCODE = "utf-8"


def main(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise ValueError(f"指定されたパス '{pdf_path}' は有効なファイルパスではありません。")
    if not pdf_path.is_file():
        raise ValueError(f"指定されたパス '{pdf_path}' は有効なファイルパスではありません。")

    with pdf_path.open("rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        markdown_text = extract_text_from_pdf_by_pypdf(pdf_bytes)

    # PDFファイルと同じ階層にMarkdownファイルを出力
    output_path = pdf_path.with_suffix(".md")
    with output_path.open("w", encoding="utf-8") as output_file:
        output_file.write(markdown_text)

    print(f"PDFファイル '{pdf_path.name}' をMarkdownファイル '{output_path.name}' に変換しました。")


if __name__ == "__main__":
    input_pdf_path = Path(sys.argv[1])  # NOTE: idx=0はスクリプトファイル名になってしまう.

    main(input_pdf_path)

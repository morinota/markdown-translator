import re
from pathlib import Path

import pymupdf4llm
import requests
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from omegaconf import OmegaConf

from markdown_translator.service.custom_callback_handlers import TokenUsageLoggingHandler
from markdown_translator.service.web_page_parser import parse_html_to_markdown


def is_pdf_url(url: str) -> bool:
    """URLがPDFファイルを指しているかを判定する"""
    url_lower = url.lower()
    return url_lower.endswith(".pdf") or "/pdf/" in url_lower


def download_pdf(url: str, output_path: Path) -> None:
    """URLからPDFをダウンロードしてローカルに保存する"""
    response = requests.get(url)
    output_path.write_bytes(response.content)
    logger.info(f"PDF downloaded from {url} to {output_path}")


class LlmPaperTranslatorFacade:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini",
            callbacks=[TokenUsageLoggingHandler()],
        )

        self._config = OmegaConf.load("config.yaml")

        self._translater_prompt = ChatPromptTemplate.from_messages(
            messages=[(message.role, message.content) for message in self._config.paper_translater_prompt.messages]
        )

        self._translator_chain = self._translater_prompt | self._llm | StrOutputParser()

    def run(self, input_path: str, output_md_path: Path) -> None:
        if input_path.startswith("https://") or input_path.startswith("http://"):
            if is_pdf_url(input_path):
                # PDF URLの場合は一時的にダウンロード
                temp_pdf_path = Path("/tmp/temp_downloaded.pdf")
                download_pdf(input_path, temp_pdf_path)
                md_text = pymupdf4llm.to_markdown(str(temp_pdf_path))
                # 正規表現でヘッダーっぽいものを検出して変換
                pattern = r"\*\*(\d+)\*\*\s+\*\*([^*]+)\*\*"
                md_text = re.sub(pattern, r"## \1 \2", md_text)
                md_text = fix_line_breaks(md_text)
            else:
                # 通常のWebページの場合
                loader = AsyncChromiumLoader(urls=[input_path])
                html_text = loader.load()[0].model_dump()["page_content"]
                Path("/tmp/temp_web_page.html").write_text(html_text)
                # HTMLをMarkdownに変換
                md_text = parse_html_to_markdown(html_text)
                Path("/tmp/temp_md_text.md").write_text(md_text)

        elif input_path.endswith(".pdf") and Path(input_path).exists():
            md_text = pymupdf4llm.to_markdown(input_path)
            # 正規表現でヘッダーっぽいものを検出して変換
            pattern = r"\*\*(\d+)\*\*\s+\*\*([^*]+)\*\*"
            md_text = re.sub(pattern, r"## \1 \2", md_text)
            md_text = fix_line_breaks(md_text)
        else:
            raise ValueError("Invalid input_pdf_path: ", input_path)

        logger.info("PDF to markdown conversion successful")

        # markdown構造に基づいてテキストを分割
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
                ("####", "Header 4"),
                ("#####", "Header 5"),
            ],
            strip_headers=False,
        )
        md_header_splits = md_splitter.split_text(md_text)

        translated_outputs = []
        for idx, doc in enumerate(md_header_splits):
            logger.info(f"Processing chunk {idx + 1} of {len(md_header_splits)}")
            translated_output = self._translator_chain.invoke({"input_paper_content": doc.page_content})

            # 先頭の```mdと末尾の```を削除する
            if translated_output.startswith("```md") and translated_output.endswith("```"):
                translated_output = translated_output[5:-3]

            translated_outputs.append(translated_output)

        translated_output = "\n\n".join(translated_outputs)

        # 出力ファイルの1行目にrefs行を追加
        final_output = f"refs: {input_path}\n\n{translated_output}"

        if not output_md_path.parent.exists():
            output_md_path.parent.mkdir(parents=True)
        output_md_path.write_text(final_output)
        logger.info(f"Markdown file saved at: {output_md_path}")


def fix_line_breaks(md_text: str) -> str:
    """
    以下の条件をすべて満たす行の改行だけをスペースに置き換える:
      1. 行頭が '## ' で始まらない (ヘッダー行でない)
      2. 行末が '.' で終わらない (文末ドットがない)
      3. 改行が 1つだけで、連続する改行が無い (二重改行は保持)
      4. 次の行が '## ' で始まらない
    """
    pattern = r"^(?!## )(?P<text>.*?)(?<!\.)\n(?!\n|## )"
    #  re.MULTILINE フラグを用いることで、
    # '^' および '$' が各行の先頭・末尾にマッチするようになる
    md_text = re.sub(pattern, r"\g<text> ", md_text, flags=re.MULTILINE)
    return md_text


if __name__ == "__main__":
    # input = Path("sample_paper.pdf")
    # input = "https://langchain-ai.github.io/langgraph/tutorials/introduction/"
    # runner = LlmPaperTranslatorFacade()
    # runner.run(input, Path("sample_paper_2.md"))
    pdf_path = Path("/tmp/temp_web_page.pdf")
    html_uri = "https://langchain-ai.github.io/langgraph/tutorials/introduction/"

    md_text = """## 1 Header
これはヘッダー行です

この行はドットがないし
行頭が##じゃなく、改行2つで段落が空いてます

ドットがない1行改行
ここはスペースに置き換えられます

ドットで終わる行.
これは改行してOK
## 2 Header
二重改行があるなら
そこは消さずにそのまま
"""
    print(fix_line_breaks(md_text))

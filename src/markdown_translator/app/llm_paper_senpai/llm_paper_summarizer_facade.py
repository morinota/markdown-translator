import re
from pathlib import Path
from typing import Any, TypeVar

import pymupdf4llm
import typer
from langchain.schema.runnable import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownHeaderTextSplitter
from loguru import logger
from omegaconf import OmegaConf

T = TypeVar("T")


def show_progress(inp: T) -> T:
    logger.info("Progress: hoge")
    return inp


class LlmPaperSummarizerFacade:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

        self._config = OmegaConf.load("config.yaml")

        self._writer_prompt = ChatPromptTemplate.from_messages(
            messages=[(message.role, message.content) for message in self._config.paper_summarizer_prompt.messages]
        )

        self._writer_chain = (
            {
                "input_paper_content": lambda x: x["input_paper_content"],
                "review": lambda x: x.get("review", "初回の作成のため、レビューはありません。"),
            }
            | self._writer_prompt
            | RunnableLambda(show_progress)
            | self._llm
            | RunnableLambda(show_progress)
            | StrOutputParser()
        )

        self._reviewer_prompt = ChatPromptTemplate.from_messages(
            messages=[(message.role, message.content) for message in self._config.reviewer_prompt.messages]
        )
        self._reviewer_chain = (
            self._reviewer_prompt
            | RunnableLambda(show_progress)
            | self._llm
            | RunnableLambda(show_progress)
            | StrOutputParser()
        )

    def run(self, input_pdf_path: Path, output_md_path: Path) -> None:
        md_text = pymupdf4llm.to_markdown(input_pdf_path)
        # 正規表現でヘッダーっぽいものを検出して変換
        pattern = r"\*\*(\d+)\*\*\s+\*\*([^*]+)\*\*"
        md_text = re.sub(pattern, r"## \1 \2", md_text)
        logger.info("PDF to markdown conversion successful")

        # markdown構造に基づいてテキストを分割
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ],
            strip_headers=False,
        )
        md_header_splits = md_splitter.split_text(md_text)

        # 各セクションごとに解説を作成する
        summary_outputs = [
            self._writer_chain.invoke({"input_paper_content": md_section.page_content})
            for md_section in md_header_splits
        ]
        summarization_output = "\n\n".join(summary_outputs)
        logger.info("Initial summarization successful")
        with open(output_md_path, "w") as f:
            f.write(summarization_output)

        # ユーザ自身がレビューを行い、そのレビューをもとにwriter_chainが再度、記事を執筆する
        review_by_human = input("フィードバックを入力してください。終了する場合は'finish'と入力してください。: ")

        while review_by_human != "finish":
            summarization_output = self._writer_chain.invoke(
                {"input_paper_content": md_text, "review": review_by_human}
            )
            with open(output_md_path, "w") as f:
                f.write(summarization_output)

            review_by_human = input("Please review the output and provide feedback: ")


if __name__ == "__main__":
    # input_pdf_path = Path("sample_paper.pdf")
    input_pdf_path = Path(
        "/Users/masato.morita/Downloads/NIPS-2010-parametric-bandits-the-generalized-linear-case-Paper.pdf"
    )
    runner = LlmPaperSummarizerFacade()
    runner.run(input_pdf_path, Path("sample_paper_summary.md"))

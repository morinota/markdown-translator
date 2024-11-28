import re
from pathlib import Path
from typing import TypeVar

import pymupdf4llm
from langchain.schema.runnable import RunnableLambda
from langchain.text_splitter import CharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from omegaconf import OmegaConf

from markdown_translator.service.custom_callback_handlers import TokenUsageLoggingHandler

T = TypeVar("T")


def show_progress(inp: T) -> T:
    # logger.info("Progress: hoge")
    return inp


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

        self._translator_chain = (
            self._translater_prompt
            | RunnableLambda(show_progress)
            | self._llm
            | RunnableLambda(show_progress)
            | StrOutputParser()
        )

    def run(self, input_path: str, output_md_path: Path) -> None:
        if input_path.startswith("https://"):
            loader = WebBaseLoader(web_path=input_path)
            md_text = loader.load()[0].model_dump()["page_content"]
        elif input_path.endswith(".pdf") and Path(input_path).exists():
            md_text = pymupdf4llm.to_markdown(input_path)
            # 正規表現でヘッダーっぽいものを検出して変換
            pattern = r"\*\*(\d+)\*\*\s+\*\*([^*]+)\*\*"
            md_text = re.sub(pattern, r"## \1 \2", md_text)

        else:
            raise ValueError("Invalid input_pdf_path: ", input_path)

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

        translated_outputs = []
        for idx, doc in enumerate(md_header_splits):
            logger.info(f"Processing chunk {idx + 1} of {len(md_header_splits)}")
            translated_outputs.append(self._translator_chain.invoke({"input_paper_content": doc.page_content}))

        translated_output = "\n\n".join(translated_outputs)
        if not output_md_path.parent.exists():
            output_md_path.parent.mkdir(parents=True)
        output_md_path.write_text(translated_output)
        logger.info(f"Markdown file saved at: {output_md_path}")


if __name__ == "__main__":
    # input = Path("sample_paper.pdf")
    input = "https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/"
    runner = LlmPaperTranslatorFacade()
    runner.run(input, Path("sample_paper_2.md"))

from pathlib import Path
from typing import Any, TypeVar

import pymupdf4llm
import typer
from langchain.schema.runnable import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger
from omegaconf import OmegaConf

from markdown_translator.app.schema import PaperTranslationOutput

app = typer.Typer(pretty_exceptions_short=True)

T = TypeVar("T")


def show_progress(inp: T) -> T:
    logger.info("Progress: hoge")
    return inp


class Runner:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

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

    def run(self, input_pdf_path: Path, output_md_path: Path) -> None:
        md_text = pymupdf4llm.to_markdown(input_pdf_path)
        logger.info("PDF to markdown conversion successful")

        translated_output = self._translator_chain.invoke({"input_paper_contents": md_text})
        logger.info("Translation successful")

        with open(output_md_path, "w") as f:
            f.write(translated_output)


@app.command()
def main(input_pdf_path: Path = typer.Argument(..., help="Input PDF file path")) -> None:
    runner = Runner()
    runner.run(input_pdf_path, input_pdf_path.with_suffix(".md"))


if __name__ == "__main__":
    # app()
    input_pdf_path = Path("sample_paper.pdf")
    runner = Runner()
    runner.run(input_pdf_path, Path("sample_paper.md"))

from pathlib import Path

import typer

from markdown_translator.app.llm_paper_translator.llm_paper_translator_facade import LlmPaperTranslatorFacade

app = typer.Typer(pretty_exceptions_enable=False)


@app.command()
def main(
    input: str = typer.Option(..., help="Input PDF file path"),
    output: Path = typer.Option(..., help="Output markdown file path"),
) -> None:
    runner = LlmPaperTranslatorFacade()
    runner.run(input, output)


if __name__ == "__main__":
    app()

from pathlib import Path

import typer

from markdown_translator.app.llm_paper_senpai.llm_paper_summarizer_facade import LlmPaperSummarizerFacade

app = typer.Typer(pretty_exceptions_enable=False)


@app.command()
def main(
    input: Path = typer.Option(..., help="Input PDF file path"),
    output: Path = typer.Option(..., help="Output markdown file path"),
) -> None:
    runner = LlmPaperSummarizerFacade()
    runner.run(input, output)


if __name__ == "__main__":
    app()

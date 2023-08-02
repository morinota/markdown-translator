import re
from typing import List

from entities.markdown_content_class import MarkdownContent


class MarkdownReader:
    LINE_BREAK_STR = "\n"
    EQUATION_STR = "$$"
    WINDOWS_ENCODE = "utf-8"

    def __init__(self) -> None:
        pass

    def read(self, raw_str: str) -> List[MarkdownContent]:
        str_lines = self._split_by_line_break(raw_str)
        str_lines = self._combine_equation_lines(str_lines)
        str_lines = self._combine_code_block_lines(str_lines)
        str_lines = self._remove_edge_spaces(str_lines)
        str_lines = self._remove_empty_line(str_lines)

        return [MarkdownContent.from_str(text) for text in str_lines]

    def _split_by_line_break(self, raw_string: str) -> List[str]:
        """raw_stringを各lineで分割する"""
        # TODO:この分割するタイミングで$\tilde$が$\\tilde$に変換されてしまう? => コンソールに出力しただけでの問題だったのでOK。
        return raw_string.split(sep=MarkdownReader.LINE_BREAK_STR)

    def _remove_edge_spaces(self, str_lines: List[str]) -> List[str]:
        """str.strip()：stringの両端の指定した文字を削除する.
        defaultは空白文字(改行\nや全角スペース\u3000やタブ\tなどが空白文字とみなされ削除)"""
        return [text.strip() for text in str_lines if text != ""]

    def _remove_empty_line(self, str_lines: List[str]) -> List[str]:
        return [text for text in str_lines if text != ""]

    def _combine_equation_lines(self, str_lines: List[str]) -> List[str]:
        """str_linesから、markdownの数式箇所(ex. $$hogehoge$$)を見つけて、一つの要素にcombineする
        str_linesをList[str]でコンソール出力すると、$\tilde$が$\\tilde$に変換されているように見えるが、
        各要素strのみ出力すると変換はされてなかったので問題なし。
        """
        str_lines_equation_combined = []
        cache_for_equation = []
        is_equation = False

        for text in str_lines:
            if text == MarkdownReader.EQUATION_STR:
                is_equation = not is_equation  # boolを反転
            if is_equation:
                cache_for_equation.append(text)
                continue
            if len(cache_for_equation) == 0:
                str_lines_equation_combined.append(text)
                continue

            cache_for_equation.append(text)
            equation_text_lines_str = "\n".join(cache_for_equation)
            str_lines_equation_combined.append(equation_text_lines_str)
            cache_for_equation = []

        return str_lines_equation_combined

    def _combine_code_block_lines(self, str_lines: List[str]) -> List[str]:
        """str_linesから、markdownの数式箇所(ex. $$hogehoge$$)を見つけて、一つの要素にcombineする
        str_linesをList[str]でコンソール出力すると、$\tilde$が$\\tilde$に変換されているように見えるが、
        各要素strのみ出力すると変換はされてなかったので問題なし。
        """
        str_lines_codeblock_combined = []
        cache_for_codeblock = []
        is_codeblock = False

        for text in str_lines:
            if re.match(MarkdownContent.CODE_BLOCK_PATTERN, text):
                is_codeblock = not is_codeblock  # ```を発見したらboolを反転
            if is_codeblock:
                cache_for_codeblock.append(text)
                continue
            if len(cache_for_codeblock) == 0:
                str_lines_codeblock_combined.append(text)
                continue

            cache_for_codeblock.append(text)
            equation_text_lines_str = "\n".join(cache_for_codeblock)
            str_lines_codeblock_combined.append(equation_text_lines_str)
            cache_for_codeblock = []

        return str_lines_codeblock_combined


class MarkdownCreator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def save_as_md(output_path: str, md_string: str) -> str:
        """stringを受け取って、output_pathに.mdとして保存する"""
        with open(
            file=output_path,
            mode="w",
            encoding=MarkdownReader.WINDOWS_ENCODE,
        ) as f:
            f.write(md_string)
        return output_path

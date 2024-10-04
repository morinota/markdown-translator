import abc
import re
from urllib import parse


class QueryParserInterface(abc.ABC):
    @abc.abstractmethod
    def parse(self, query: str) -> str:
        raise NotImplementedError


class QueryParser(QueryParserInterface):
    def parse(self, query: str) -> str:
        parsed_query = parse.quote(query, safe="")
        parsed_query = self._adjust_for_query_including_slash(parsed_query)
        parsed_query = self._adjust_pipe_parse(parsed_query)
        parsed_query = self._adjust_parse_double_quart_and_F(parsed_query)
        parsed_query = self._adjust_adding_newline_for_colon_whitespace(parsed_query)

        return parsed_query

    def _adjust_for_query_including_slash(self, parsed_query: str) -> str:
        """ "/"が"5C%2F"にparseされて欲しい.("5C"は"¥"のurl encode, "2F"は"/"のurl encode)"""
        return re.sub(
            pattern=r"2F",
            repl=r"5C%2F",
            string=parsed_query,
        )

    def _adjust_pipe_parse(self, parsed_query: str) -> str:
        """P(A|B)みたいなケースで翻訳が途切れるバグ対応.
        - どうやら半角round braket"("と")"がurl encodeされる("%28A%7CB%29")ケースで、翻訳の前半が途切れるみたい.
        - よってround braketのurl encodeをdecodeし、何故かpipeの前に%5C(\のurl encode)を追加する.
        """
        return re.sub(
            pattern=r"%28(.*)%7C(.*)%29",
            repl=r"(\1%5C%7C\2)",
            string=parsed_query,
        )

    def _adjust_parse_double_quart_and_F(self, parsed_query: str) -> str:
        """
            query内に["F]が含まれる場合に、[%22F]とparseされて欲しい。
        しかし、[%25C%2F]に変換されて翻訳が切れるケースが発生した為、本後処理を追加した。
        """
        return re.sub(
            pattern=r"%25C%2F",
            repl=r"%22F",
            string=parsed_query,
        )

    def _adjust_adding_newline_for_colon_whitespace(self, parsed_query: str) -> str:
        """
        文中の[: ]をシンプルに"%3A%20"にparseすると、翻訳が途切れるケースが発生した。
        よって"%3A%20%0"としてparseさせる(改行を追加する)ようにして対応する。
        """
        return re.sub(
            pattern=r"%3A%20",
            repl=r"%3A%20%0A",
            string=parsed_query,
        )

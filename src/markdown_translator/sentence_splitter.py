import abc
import re
from typing import List


class SentenceSplitterInterface(abc.ABC):
    @abc.abstractmethod
    def split(self, query: str) -> List[str]:
        raise NotImplementedError


class SentenceSplitter(SentenceSplitterInterface):
    PATTERN_REPL_MAP = {
        r"\. \(([0-9]*)\)": r".(\g<1>)",  # "Hoge et al. (2023)"の場合にsplitしないように変換する.
        r"(\.\s*)(\d+)": r".\2",  # "According to Fig. 8, A is B."の場合にsplitしないように変換する.
        r"et al\. ": r"et al.",  # "Gupta et al. [12] proposed hogehoge."の場合にsplitしないように変換する.
        r"(.\..\.)(\s*)(.)": r"\1\3",  # "See e.g. [13]."や "(i.e. I love A.)"の場合にsplitしないように変換する.
    }

    def split(self, query: str) -> List[str]:
        preprocessed_query = self.__preprocessed_query(query)
        splitted_sentences = preprocessed_query.split(". ")
        return self.__add_period_to_sentences(splitted_sentences)

    def __add_period_to_sentences(self, splitted_sentences: List[str]) -> List[str]:
        length = len(splitted_sentences)
        if length == 1:
            return splitted_sentences
        return [f"{query}." if idx < length - 1 else query for idx, query in enumerate(splitted_sentences)]

    def __preprocessed_query(self, query: str) -> str:
        """splitの正常動作を阻害しうる要素を除去/変換する"""
        preprocessed_query = query
        for pattern, replace in self.PATTERN_REPL_MAP.items():
            preprocessed_query = re.sub(pattern, replace, preprocessed_query)

        return preprocessed_query

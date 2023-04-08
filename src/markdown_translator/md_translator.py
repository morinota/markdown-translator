import logging
import re
import time
from email.mime import base
from typing import Generator, List, Optional, Tuple
from urllib import parse

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

from markdown_reader.markdown_content_class import MarkdownContent

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(hdlr=handler)


class MarkdownTranslatorWrapper:
    def __init__(
        self,
        driver: webdriver.Chrome,
        from_lang: str = "en",
        to_lang: str = "ja",
    ):
        self.deepl_translator = DeepLTranslator(driver, from_lang, to_lang)

    def translate(
        self,
        md_contents: List[MarkdownContent],
        correspond: bool,
    ) -> List[MarkdownContent]:
        """MarkdownContentのListを受け取り、翻訳した情報をtext_translatedに格納して返す
        Parameters
        ----------
        md_contents : List[MarkdownContent]

        Returns
        -------
        List[MarkdownContent]
        """
        md_contents_translated = []
        length_contents = len(md_contents)
        for idx, md_content in enumerate(md_contents):
            logger.info(f"[LOG] {idx+1}/{length_contents}========================")
            md_content_translated = self._tranlate_each_md_content(
                md_content,
                correspond=correspond,
            )
            md_contents_translated.append(md_content_translated)

        return md_contents_translated

    def _tranlate_each_md_content(
        self,
        md_content: MarkdownContent,
        correspond: bool,
    ) -> MarkdownContent:
        if md_content.tag_name in MarkdownContent.NON_TRANSLATE_TAGS:
            return md_content

        raw_text_list, translated_text_list = self.deepl_translator.translate(base_query=md_content.text_raw)

        return MarkdownContent(
            tag_name=md_content.tag_name,
            text_raw=md_content.text_raw,
            text_translated=" ".join(translated_text_list),
            text_raw_list=raw_text_list,
            text_translated_list=translated_text_list,
        )


class DeepLTranslator:
    URL_FORMAT = "https://www.deepl.com/en/translator#{from_lang}/{to_lang}/" + "{query}"
    TRIALS_NUM = 30  # 1 queryをdeepLに投げて翻訳結果の取得を試す回数.
    INTERVAL_SEC_WEBDRIVER = 1  # 1 trial当たりのinterval
    TARGET_TAG_NAME = "button"
    TARGET_TAG_CLASS = "lmt__translations_as_text__text_btn"

    def __init__(
        self,
        driver: webdriver.Chrome,
        from_lang: str = "en",
        to_lang: str = "ja",
    ) -> None:
        self.driver = driver
        self.to_lang = to_lang
        self.from_lang = from_lang

    def translate(
        self,
        base_query: str,
    ) -> Tuple[List[str], List[str]]:
        self.URL_FORMAT
        source_sentences = []
        target_sentences = []

        base_query_preprocessed = self._preprocess(base_query)
        splitted_querys = self._split_querys(base_query_preprocessed)
        for query in splitted_querys:
            parsed_query = self._parse_query(query)
            url = self.URL_FORMAT.format(
                from_lang=self.from_lang,
                to_lang=self.to_lang,
                query=parsed_query,  # 変換(query parameterに渡す.)
            )
            self.driver.refresh()
            self.driver.get(url)

            for _ in range(self.TRIALS_NUM):  # 翻訳が完了するまでTRIALS_NUM回 繰り返す
                time.sleep(self.INTERVAL_SEC_WEBDRIVER)
                soup_deepl = BeautifulSoup(markup=self.driver.page_source.encode("utf-8"), features="lxml")  # htmlを取得

                translated_query: str = self._find_translated_text(soup_deepl)
                if self._is_translated_properly(translated_query):
                    break
            else:
                logger.info(f"we cannot get translated_query of this in TRIALS_NUM.:{query}")
                translated_query = "[empty]"
            logger.debug(f"one_query: {query}")
            logger.debug(f"translated_query: {translated_query}")
            source_sentences.append(query)
            target_sentences.append(translated_query)
        return source_sentences, target_sentences

    def _find_translated_text(self, soup_obj: BeautifulSoup) -> str:
        """Find translated text from soup object"""
        target_tag_info = soup_obj.find(
            name=self.TARGET_TAG_NAME,
            class_=self.TARGET_TAG_CLASS,
        )
        # with open("my_file.html", "w", encoding="utf-8") as f:
        #     f.write(str(soup_obj))

        text_in_tag = target_tag_info.text if target_tag_info is not None else ""
        return text_in_tag

    @staticmethod
    def _is_translated_properly(translated_text: str) -> bool:
        """Check if the acquired translated_text is appropriate."""
        return len(translated_text) > 0

    @staticmethod
    def _split_querys(base_query: str) -> List[str]:
        """簡易的に、query を". "で分割している."""
        splitted_querys = base_query.split(". ")
        length = len(splitted_querys)
        if length == 1:
            return splitted_querys
        return [f"{query}." if idx < length - 1 else query for idx, query in enumerate(splitted_querys)]

    @staticmethod
    def _preprocess(base_query: str) -> str:
        """_splitの正常動作を阻害しうる要素を除去/変換する"""
        # # "Hoge et al. (2023)"の場合にsplitしないように変換する.
        pattern = r"\. \(([0-9]*)\)"
        base_query = re.sub(pattern, r".(\g<1>)", base_query)

        # "According to Fig. 8, A is B."の場合にsplitしないように変換する.
        pattern = r"(\.\s*)(\d+)"
        base_query = re.sub(pattern, r".\2", base_query)

        # "Gupta et al. [12] proposed hogehoge."の場合にsplitしないように変換する.
        pattern = r"et al\. "
        base_query = re.sub(pattern, r"et al.", base_query)

        # "See e.g. [13]."や "(i.e. I love A.)"の場合にsplitしないように変換する.
        pattern = r"(.\..\.)(\s*)(.)"
        base_query = re.sub(pattern, r"\1\3", base_query)
        return base_query

    @staticmethod
    def _parse_query(query: str) -> str:
        parsed_query = parse.quote(query, safe="")
        # "/"で翻訳文章が切れるケースへの対処を追加
        parsed_query = re.sub(
            pattern=r"2F",
            repl=r"5C%2F",
            string=parsed_query,
        )  # "/"が"5C%2F"にparseされて欲しい.("5C"は"¥"のurl encode, "2F"は"/"のurl encode)
        return parsed_query

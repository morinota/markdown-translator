import logging
import time
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


class MarkdownTranslator:
    URL_FORMAT = "https://www.deepl.com/en/translator#{from_lang}/{to_lang}/" + "{query}"
    TRIALS_NUM = 30  # 1 queryをdeepLに投げて翻訳結果の取得を試す回数.
    INTERVAL_SEC_WEBDRIVER = 1  # 1 trial当たりのinterval

    def __init__(
        self,
        driver: webdriver.Chrome,
        from_lang: str = "en",
        to_lang: str = "ja",
    ):
        self.driver = driver

        self.to_lang = to_lang
        self.from_lang = from_lang

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

        raw_text_list, translated_text_list = self._translate_wrapper(
            query=md_content.text_raw,
            driver=self.driver,
        )

        return MarkdownContent(
            tag_name=md_content.tag_name,
            text_raw=md_content.text_raw,
            text_translated=" ".join(translated_text_list),
            text_raw_list=raw_text_list,
            text_translated_list=translated_text_list,
        )

    def _translate_wrapper(
        self,
        query: str,
        driver: webdriver.Chrome,
    ) -> Tuple[List[str], List[str]]:

        self.URL_FORMAT
        source_sentences = []
        target_sentences = []

        splitted_querys = self._split_querys(query)
        for one_query in splitted_querys:
            url = self.URL_FORMAT.format(
                from_lang=self.from_lang,
                to_lang=self.to_lang,
                query=parse.quote(one_query),  # 変換(query parameterに渡す.)
            )
            driver.refresh()
            driver.get(url)

            for _ in range(self.TRIALS_NUM):  # 翻訳が完了するまでTRIALS_NUM回 繰り返す
                time.sleep(self.INTERVAL_SEC_WEBDRIVER)
                soup_deepl = BeautifulSoup(markup=driver.page_source.encode("utf-8"), features="lxml")  # htmlを取得

                translated_query: str = self._find_translated_text(soup_deepl)
                if self._is_translated_properly(translated_query):
                    break
            else:
                logger.info(f"we cannot get translated_query of this in TRIALS_NUM.:{one_query}")
                translated_query = "[empty]"
            logger.debug(f"one_query: {one_query}")
            logger.debug(f"translated_query: {translated_query}")
            source_sentences.append(one_query)
            target_sentences.append(translated_query)
        return source_sentences, target_sentences

    def _find_translated_text(self, soup_obj: BeautifulSoup) -> str:
        """Find translated text from soup object"""
        target_tag = "japanese"
        target_tag_info = soup_obj.find(
            name="button",
            class_="lmt__translations_as_text__text_btn"  # html内を検索するタグ名
            # attrs={},  # 検索する属性と属性値のセット
            # recursive=None,  # 再帰的に(=下の階層まで?)検索するならTrue
            # text=None,  # 検索対象のtext
        )
        with open("my_file.html", "w", encoding="utf-8") as f:
            f.write(str(soup_obj))

        text_in_tag = target_tag_info.text if target_tag_info is not None else ""
        return text_in_tag

    def _is_translated_properly(self, translated_text: str) -> bool:
        """Check if the acquired translated_text is appropriate."""
        return len(translated_text) > 0

    def _split_querys(self, query: str) -> List[str]:
        """簡易的に、query を". "で分割している."""
        return [splitted_query + "." for splitted_query in query.split(". ")]

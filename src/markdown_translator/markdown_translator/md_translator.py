import logging
import time


from bs4 import BeautifulSoup
from selenium import webdriver

from markdown_translator.entities.markdown_content_class import MarkdownContent
from markdown_translator.markdown_translator.query_parser import (
    QueryParser,
    QueryParserInterface,
)
from markdown_translator.markdown_translator.sentence_splitter import (
    SentenceSplitter,
    SentenceSplitterInterface,
)


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
        page_load_timeout: int = 600,  # seleniumのdefalut値(300sec) * 2
        implicit_wait_timeout: int = 100,
    ):
        """
        Parameters
        ----------
        - driver : webdriver.Chrome
        - from_lang : str
            - 翻訳元言語
        - to_lang : str
            - 翻訳先言語
        - page_load_timeout : int
            - ページが完全に読み込まれるまでの最大時間。このタイムアウトを超えると、TimeoutExceptionがthrowされる。
        - implicit_wait_timeout : int
            - 要素が見つかるまでの待機時間。このタイムアウトを超えると、NoSuchElementExceptionがthrowされる。
        """
        # set timeouts
        driver.set_page_load_timeout(page_load_timeout)
        driver.implicitly_wait(implicit_wait_timeout)

        query_parser = QueryParser()
        sentence_splitter = SentenceSplitter()
        self.deepl_translator = DeepLTranslator(
            driver,
            query_parser,
            sentence_splitter,
            from_lang,
            to_lang,
        )

    def translate(
        self,
        md_contents: list[MarkdownContent],
        correspond: bool,
    ) -> list[MarkdownContent]:
        """MarkdownContentのlistを受け取り、翻訳した情報をtext_translatedに格納して返す
        Parameters
        ----------
        md_contents : list[MarkdownContent]

        Returns
        -------
        list[MarkdownContent]
        """
        contents_translated = []
        length_contents = len(md_contents)
        for idx, md_content in enumerate(md_contents):
            logger.info(f"[LOG] {idx+1}/{length_contents}========================")
            md_content_translated = self._tranlate_each_md_content(
                md_content,
                correspond=correspond,
            )
            contents_translated.append(md_content_translated)

        return contents_translated

    def _tranlate_each_md_content(
        self,
        md_content: MarkdownContent,
        correspond: bool,
    ) -> MarkdownContent:
        if md_content.tag_name in MarkdownContent.NON_TRANSLATE_TAGS:
            return md_content

        raw_text_list, translated_text_list = self.deepl_translator.translate(
            base_query=md_content.text_raw
        )

        return MarkdownContent(
            tag_name=md_content.tag_name,
            text_raw=md_content.text_raw,
            text_translated=" ".join(translated_text_list),
            text_raw_list=raw_text_list,
            text_translated_list=translated_text_list,
        )


class DeepLTranslator:
    URL_FORMAT = (
        "https://www.deepl.com/en/translator#{from_lang}/{to_lang}/" + "{query}"
    )
    TRIALS_NUM = 30  # 1 queryをdeepLに投げて翻訳結果の取得を試す回数.
    INTERVAL_SEC_WEBDRIVER = 3  # 1 trial当たりのinterval
    TARGET_TAG_NAME = "button"
    TARGET_TAG_CLASS = "lmt__translations_as_text__text_btn"

    def __init__(
        self,
        driver: webdriver.Chrome,
        query_parser: QueryParserInterface,
        splitter: SentenceSplitterInterface,
        from_lang: str = "en",
        to_lang: str = "ja",
    ) -> None:
        self.driver = driver
        self.query_parser = query_parser
        self.splitter = splitter
        self.to_lang = to_lang
        self.from_lang = from_lang

    def translate(
        self,
        base_query: str,
    ) -> tuple[list[str], list[str]]:
        self.URL_FORMAT
        source_sentences = []
        target_sentences = []

        splitted_querys = self.splitter.split(base_query)
        for query in splitted_querys:
            parsed_query = self.query_parser.parse(query)
            url = self.URL_FORMAT.format(
                from_lang=self.from_lang,
                to_lang=self.to_lang,
                query=parsed_query,  # 変換(query parameterに渡す.)
            )
            self.driver.refresh()
            self.driver.get(url)

            for _ in range(self.TRIALS_NUM):  # 翻訳が完了するまでTRIALS_NUM回 繰り返す
                time.sleep(self.INTERVAL_SEC_WEBDRIVER)
                soup_deepl = BeautifulSoup(
                    markup=self.driver.page_source.encode("utf-8"), features="lxml"
                )  # htmlを取得
                translated_query = self._extract_translated_text_from_html(soup_deepl)
                if self._is_translated_properly(translated_query):
                    break
            else:
                logger.info(
                    f"we cannot get translated_query of this in TRIALS_NUM.:{query}"
                )
                translated_query = "[empty]"
            logger.debug(f"one_query: {query}")
            logger.debug(f"translated_query: {translated_query}")
            source_sentences.append(query)
            target_sentences.append(translated_query)
        return source_sentences, target_sentences

    def _extract_translated_text_from_html(self, soup_obj: BeautifulSoup) -> str:
        """Find translated text from soup object"""

        translated_tag = soup_obj.find(
            name="div",  # 要素の指定
            attrs={"aria-labelledby": "translation-target-heading"},  # 属性の指定
        )
        # with open("sample.html", "w", encoding="utf-8") as file:
        #     file.write(str(soup_obj))
        # raise Exception

        return translated_tag.text if translated_tag else ""

    def _is_translated_properly(self, translated_text: str) -> bool:
        """Check if the acquired translated_text is appropriate."""
        return len(translated_text) > 0

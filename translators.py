# coding: utf-8
"""These classes translate English(``from_lang``) into Japanese(``to_lang``) using an external 
translation service (website).

Currently, Translation-Gummy supports the following services:
    - `Google Translate <https://translate.google.co.jp/#en/ja/Translation%20Gummy>`_
    - `DeepL Translator <https://www.deepl.com/en/translator#en/ja/Translation%20Gummy>`_

You can easily get (import) ``Translator Class`` by the following ways.

.. code-block:: python

    >>> from gummy import translators
    >>> translator = translators.get("google")
    >>> translator
    <gummy.translators.GoogleTranslator at 0x129890160>
    >>> from gummy.translators import GoogleTranslator
    >>> google = GoogleTranslator()
    >>> google
    <gummy.translators.GoogleTranslator at 0x129890700>
    >>> translator = translators.get(google)
    >>> id(google) == id(translator)
    True
"""

import time
import urllib
import warnings
from abc import ABCMeta, abstractmethod, abstractproperty, abstractstaticmethod
from collections import defaultdict
from email.generator import Generator
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from typing_extensions import Self

from utils._data import lang_code2name, lang_name2code
from utils._exceptions import GummyImprementationError
from utils._warnings import GummyImprementationWarning
from utils.coloring_utils import toBLUE, toGREEN, toRED
from utils.driver_utils import get_driver
from utils.generic_utils import handleKeyError, handleTypeError, mk_class_get, splitted_query_generator
from utils.monitor_utils import ProgressMonitor
from utils.soup_utils import find_all_target_text, find_target_text

INTERVAL_WEBDRIVER = 5


class GummyAbstTranslator(metaclass=ABCMeta):
    def __init__(
        self,
        driver: Optional[webdriver.Chrome] = None,
        maxsize: int = 5000,
        interval: int = 1,
        trials: int = 30,
        verbose: bool = False,
        use_cache: bool = True,
        specialize: bool = True,
        from_lang: str = "en",
        to_lang: str = "ja",
    ):
        """If you want to create your own translator class, please inherit this class.

        Args:
            driver (WebDriver) : Selenium WebDriver.
            maxsize (int)      : Number of English characters that we can send a request at one time. (default= ``5000``)
            interval (int)     : Trial interval [s]. (default= ``1``)
            trials (int)       : How many times to try to find translated text. (default= ``30``)
            verbose (bool)     : Whether to print message or not. (default= ``False``)
            use_cache (bool)   : Whether to use cache or not. cashe is used in :meth:`is_translated <gummy.translators.GummyAbstTranslator.is_translated>` (default= ``True``)
            specialize (bool)  : Whether to support multiple languages or specialize. (default= ``True``) If you want to specialize in translating between specific languages, set ``from_lang`` and ``to_lang`` arguments.
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.

        Attributes:
            cache (str) : Translated text acquired one time ago. Prevent bugs where the same translated text is repeated. Used in :meth:`is_translated <gummy.translators.GummyAbstTranslator.is_translated>`.
        """
        self.driver = driver
        self.maxsize = maxsize
        self.interval = interval
        self.trials = trials
        self.verbose = verbose
        self.use_cache = use_cache
        self.cache = ""
        self.setup(specialize=specialize, from_lang=from_lang, to_lang=to_lang)

    @property
    def class_name(self):
        """Same as ``self.__class__.__name__``."""
        return self.__class__.__name__

    @property
    def name(self):
        """Translator service name."""
        return self.class_name.replace("Translator", "")

    @property
    def driver_info(self) -> Dict:
        """Return driver_info

        Examples:
            >>> from gummy.utils import get_driver
            >>> from gummy.translators import GoogleTranslator
            >>> with get_driver() as driver:
            ...     translator = GoogleTranslator(driver=driver)
            ...     print(translator.driver_info)
            {'session_id': '3e869e62f06c5f7d938831179ad3c50e', 'browserName': 'chrome'}
            >>> translator = GoogleTranslator(driver=None)
            >>> print(translator.driver_info)
            {}
        """
        info = {}
        driver = self.driver
        if driver is not None:
            info["session_id"] = driver.session_id
            info["browserName"] = driver.capabilities.get("browserName")
        return info

    def check_driver(self, driver: Optional[webdriver.Chrome] = None) -> webdriver.Chrome:
        """If the driver does not exist, use :meth:`get_driver <gummy.utils.driver_utils.get_driver>` to get the driver.

        Args:
            driver (WebDriver) : Selenium WebDriver.

        Returns:
            WebDriver : Selenium WebDriver.
        """
        driver = driver or self.driver
        if driver is None:
            driver = get_driver()
        self.driver = driver
        # if self.verbose: print(f"Driver info:\n{json.dumps(self.driver_info, indent=2)}")
        return driver

    def setup(self, specialize=True, from_lang="en", to_lang="ja"):
        """Setup an instance by defining a required translation methods.

        Args:
            specialize (bool)  : Whether to support multiple languages or specialize. (default= ``True``) If you want to specialize in translating between specific languages, set ``from_lang`` and ``to_lang`` arguments.
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.
        """
        self.url_fmt = ""
        self.lang2args = defaultdict(lambda: defaultdict(list))
        if specialize:
            self.register_method(from_lang=from_lang, to_lang=to_lang)
            (
                self.find_translated_bulk,
                self.find_translated_corr,
                self.is_translated_properly,
                self.url_fmt,
            ) = self.lang2args[from_lang][to_lang]
        else:
            for from_lang, to_lang, kwargs in self.generate_lang_pairs():
                self.register_method(from_lang=from_lang, to_lang=to_lang, **kwargs)
        self.specialize = specialize

    @abstractproperty
    def supported_langs(self):
        """Supported language codes."""
        return []

    @abstractmethod
    def specialize2langs(self, from_lang, to_lang, **kwargs) -> Tuple:
        """Create the functions and variables needed to translate from ``from_lang`` to ``to_lang``

        Args:
            specialize (bool)  : Whether to support multiple languages or specialize. (default= ``True``) If you want to specialize in translating between specific languages, set ``from_lang`` and ``to_lang`` arguments.

        Return:
            tuple (func, func, func, str): Tuple of elements required in :meth:`register_method <gummy.translators.GummyAbstTranslator.register_method>`

        +-----------------------------------------------------------------------------------------------+---------------------------------------------------------------------+
        |                                            Method                                             |                             Description                             |
        +===============================================================================================+=====================================================================+
        |     :meth:`find_translated_bulk <gummy.translators.GummyAbstTranslator.find_translated_bulk>` |                   A function to find translated text from ``soup``  |
        +-----------------------------------------------------------------------------------------------+---------------------------------------------------------------------+
        |     :meth:`find_translated_corr <gummy.translators.GummyAbstTranslator.find_translated_corr>` |  A function to find translated text from ``soup`` , and ``driver``  |
        +-----------------------------------------------------------------------------------------------+---------------------------------------------------------------------+
        | :meth:`is_translated_properly <gummy.translators.GummyAbstTranslator.is_translated_properly>` | A function to check if the acquired translated_text is appropriate. |
        +-----------------------------------------------------------------------------------------------+---------------------------------------------------------------------+
        |                               :meth:`url_fmt <gummy.translators.GummyAbstTranslator.url_fmt>` |                    An url format ( ``"{query}"`` must be included.) |
        +-----------------------------------------------------------------------------------------------+---------------------------------------------------------------------+
        """
        url_fmt = f"https://domain/{from_lang}2{to_lang}/?query=" + "{query}"
        return (
            self.find_translated_bulk,
            self.find_translated_corr,
            self.is_translated_properly,
            url_fmt,
        )

    def generate_lang_pairs(self):
        """Generator to generate all translation pairs."""
        for from_lang in self.supported_langs:
            for to_lang in self.supported_langs:
                yield (from_lang, to_lang, {})

    def register_method(self, from_lang, to_lang, **kwargs):
        """Register Methods which translate ``from_lang`` to ``to_lang``

        Args:
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.
            kwargs (dict)      : kwargs required for :meth:`specialize2langs <gummy.translators.GummyAbstTranslator.specialize2langs>`.
        """
        from_lang = lang_name2code.get(from_lang, "en")
        to_lang = lang_name2code.get(to_lang, "ja")
        (
            find_translated_bulk,
            find_translated_corr,
            is_translated_properly,
            url_fmt,
        ) = self.specialize2langs(from_lang, to_lang, **kwargs)
        self.lang2args[from_lang][to_lang] = [
            find_translated_bulk,
            find_translated_corr,
            is_translated_properly,
            url_fmt,
        ]
        method_name = f"{from_lang}2{to_lang}"
        method = lambda query, driver=None, barname=None, correspond=True: " ".join(
            self._translate(
                query=query,
                find_translated_bulk=find_translated_bulk,
                find_translated_corr=find_translated_corr,
                is_translated_properly=is_translated_properly,
                url_fmt=url_fmt,
                driver=driver,
                barname=barname,
                correspond=correspond,
            )[1]
        )
        setattr(self, method_name, method)

    def translate(
        self,
        query: str,
        driver: Optional[webdriver.Chrome] = None,
        barname: Optional[str] = None,
        from_lang: str = "en",
        to_lang: str = "ja",
        correspond: bool = False,
    ) -> str:
        """Translate Query string.

        Args:
            query (str)        : Query to be translated.
            driver (WebDriver) : Selenium WebDriver.
            barname (str)      : Bar name for :meth:`ProgressMonitor <gummy.utils.monitor_utils.ProgressMonitor>`.
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.
            correspond (bool)  : Whether to correspond the location of ``from_lang`` correspond to that of ``to_lang``.

        Returns:
            str : Translated string.

        Examples:
            >>> from gummy import translators
            >>> #=== Support multiple languages ===
            >>> translator = translators.get("deepl", specialize=False, verbose=True)
            >>> # Translate from english to Japanese (Success)
            >>> ja = translator.translate(query="This is a pen.", from_lang="en", to_lang="ja")
            DeepLTranslator (query1) 02/30[#-------------------]  6.67% - 2.173[s]   translated: これはペン
            >>> print(ja)
            これはペンです。
            >>> # Translate from english to French (Success)
            >>> fr = translator.translate(query="This is a pen.", from_lang="en", to_lang="fr")
            DeepLTranslator (query1) 01/30[--------------------]  3.33% - 1.086[s]   translated: C'est
            >>> print(fr)
            C'est un stylo.
            >>> #=== Specialize in specific languages ===
            >>> translator = translators.get("deepl", specialize=True, from_lang="en", to_lang="ja", verbose=True)
            >>> # Translate from english to Japanese (Success)
            >>> ja = translator.translate(query="This is a pen.")
            DeepLTranslator (query1) 02/30[#-------------------]  6.67% - 2.149[s]   translated: これはペン
            >>> print(ja)
            これはペンです。
            >>> # Translate from english to French (Fail)
            >>> fr = translator.translate(query="This is a pen.", from_lang="en", to_lang="fr")
            DeepLTranslator (query1) 03/30 [##------------------] 10.00% - 3.220[s]
            >>> print(fr)
            これはペンです。
        """
        return " ".join(
            self.translate_wrapper(
                query=query,
                driver=driver,
                barname=barname,
                from_lang=from_lang,
                to_lang=to_lang,
                correspond=correspond,
            )[1]
        )

    def translate_wrapper(
        self,
        query: str,
        driver: Optional[webdriver.Chrome] = None,
        correspond: bool = True,
    ) -> Tuple[List, List]:
        """Wrapper function for :meth:`translate <gummy.translators.GummyAbstTranslator.translate>`

        Args:
            query (str)        : Query to be translated.
            driver (WebDriver) : Selenium WebDriver.
            barname (str)      : Bar name for :meth:`ProgressMonitor <gummy.utils.monitor_utils.ProgressMonitor>`.
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.
            correspond (bool)  : Whether to correspond the location of ``from_lang`` correspond to that of ``to_lang``.

        Returns:
            tuple : SourceSentences ( ``list`` ) , TargetSentences ( ``list`` ) .

        Examples:
            >>> from gummy import translators
            >>> translator = translators.get("deepl", specialize=False, verbose=True)
            >>> en, ja = translator.translate_wrapper(query="This is a pen.", from_lang="en", to_lang="ja", correspond=True)
            >>> en
            ['This is a pen.']
            >>> ja
            ['これはペンです。']
        """
        url_fmt = self.url_fmt

        text_separated_ori, text_separated_trans = self._translate(
            query=query,
            url_fmt=url_fmt,
            correspond=correspond,
            driver=driver,
        )

        return text_separated_ori, text_separated_trans

    def _translate(
        self,
        query: str,
        url_fmt: str,
        correspond: bool = True,
        driver: Optional[webdriver.Chrome] = None,
    ) -> Tuple[List, List]:
        """A translating function running in :meth:`translate <gummy.translators.GummyAbstTranslator.translate>`

        Args:
            query (str)                   : Query to be translated.
            url_fmt (str)                 : An url format ( ``"{query}"`` must be included.)
            driver (WebDriver)            : Selenium WebDriver.
            barname (str)                 : Bar name for :meth:`ProgressMonitor <gummy.utils.monitor_utils.ProgressMonitor>`.

        Returns:
            tuple : SourceSentences ( ``list`` ) , TargetSentences ( ``list`` ) .
        """
        driver = self.check_driver(driver=driver)
        source_sentences = []
        target_sentences = []
        # クエリ(翻訳対象text)をmaxsizeに合わせて分割する
        splitted_querys: Generator = splitted_query_generator(query=query, maxsize=self.maxsize)

        for idx, target_query in enumerate(splitted_querys):
            # url_formatにクエリを入れて、urlを作る
            url = url_fmt.format(query=urllib.parse.quote(target_query))
            driver.refresh()  # ブラウザを更新する
            driver.get(url)  # ブラウザのアドレスバーにURLを入力し、エンターキーを押す

            for idx in range(self.trials):
                time.sleep(INTERVAL_WEBDRIVER)
                soup = BeautifulSoup(markup=driver.page_source.encode("utf-8"), features="lxml")  # htmlを取得
                translated_text: str = self.find_translated_bulk(soup)  # ここでdeepLのhtmlから翻訳された<japanese>を取得
                if self.is_translated_properly(translated_text):
                    break

            if correspond:
                source_sentences, target_sentences = self.find_translated_corr(soup, driver)
                source_sentences.extend(source_sentences)  # 追加する形式がlistなのでextend(やってる事はappendと同じ)
                target_sentences.extend(target_sentences)
            else:
                source_sentences.append(query)
                target_sentences.append(translated_text)
            if self.use_cache:
                self.cache = translated_text
            time.sleep(INTERVAL_WEBDRIVER)
        return (source_sentences, target_sentences)

    @abstractstaticmethod
    def find_translated_bulk(soup: BeautifulSoup) -> str:
        """Find translated Translated text from ``soup``

        Args:
            soup (bs4.BeautifulSoup) : A data structure representing a parsed HTML or XML document.

        Return:
            str: Translated text.
        """
        return find_target_text(soup=soup, target_tag="japanese")

    def find_translated_corr(soup: BeautifulSoup, driver: webdriver.Chrome) -> Tuple[List, List]:
        """Find translated Translated text from ``soup``

        Args:
            soup (bs4.BeautifulSoup) : A data structure representing a parsed HTML or XML document.
            driver (WebDriver)       : Selenium WebDriver.

        Return:
            tuple: source_sentences ( ``list`` ) , target_sentences ( ``list`` )
        """
        sourceSentences = driver.execute_script("return sourceSentences.map(({sourceText}) => sourceText);")
        targetSentences = driver.execute_script("return targetSentences.map(({targeText}) => targeText);")
        return sourceSentences, targetSentences

    def is_translated_properly(self, translated_text: str) -> bool:
        """Check if the acquired translated_text is appropriate.

        Args:
            translated_text (str) : Translated text.

        Examples:
            >>> from gummy import translators
            >>> translator = translators.get("google", specialize=True, from_lang="en", to_lang="ja")
            >>> translator.is_translated_properly("")
            False
            >>> translator.is_translated_properly("日本語")
            True
            >>> translator.cache = "日本語"
            >>> translator.is_translated_properly("日本語")
            False
        """
        return (len(translated_text) > 0) and (not self.cache.startswith(translated_text))


class DeepLTranslator(GummyAbstTranslator):
    """
    DeepL is a deep learning company that develops artificial intelligence systems
    for languages. See https://www.deepl.com/en/home for more info.
    """

    def __init__(
        self,
        driver: Optional[webdriver.Chrome] = None,
        maxsize: int = 5000,
        interval: int = 1,
        trials: int = 30,
        verbose: bool = False,
        use_cache: bool = True,
        specialize: bool = True,
        from_lang: str = "en",
        to_lang: str = "ja",
    ):
        super().__init__(
            driver=driver,
            maxsize=maxsize,
            interval=interval,
            trials=trials,
            verbose=verbose,
            use_cache=use_cache,
            specialize=specialize,
            from_lang=from_lang,
            to_lang=to_lang,
        )

    @property
    def supported_langs(self) -> List[str]:
        return ["de", "es", "en", "fr", "it", "ja", "nl", "pl", "pt", "ru", "zh"]

    @staticmethod
    def find_translated_bulk(soup: BeautifulSoup) -> str:
        return find_target_text(soup=soup, target_tag="button", class_="lmt__translations_as_text__text_btn")

    @staticmethod
    def find_translated_corr(soup: BeautifulSoup, driver: Optional[webdriver.Chrome]) -> Tuple[List, List]:
        """Find translated Translated text from ``soup``

        Args:
            soup (bs4.BeautifulSoup) : A data structure representing a parsed HTML or XML document.
            driver (WebDriver)       : Selenium WebDriver.

        Return:
            tuple: source_sentences ( ``list`` ) , target_sentences ( ``list`` )
        """
        source_sentences = driver.execute_script(
            "return LMT_WebTranslator_Instance.getActiveLangContext().sourceSentences.map(({_rawTrimmedText}) => _rawTrimmedText);"
        )
        target_sentences = driver.execute_script(
            "return LMT_WebTranslator_Instance.getActiveLangContext().targetSentences.map(({_lastFullTrimmedText}) => _lastFullTrimmedText);"
        )
        return source_sentences, target_sentences

    def specialize2langs(self, from_lang, to_lang, **kwargs):
        url_fmt = f"https://www.deepl.com/en/translator#{from_lang}/{to_lang}/" + "{query}"
        return (
            self.find_translated_bulk,
            self.find_translated_corr,
            self.is_translated_properly,
            url_fmt,
        )

    def is_translated_properly(self, translated_text):
        """Deepl represents the character being processed as ``[...]``, so make sure it has not completed.

        Examples:
            >>> from gummy import translators
            >>> translator = translators.get("deepl")
            >>> translator.is_translated_properly("日本語 [...]")
            False
            >>> translator.is_translated_properly("[...]日本語")
            True
            >>> translator.is_translated_properly("日本語[...]日本語")
            True
        """
        return super().is_translated_properly(translated_text) and (not translated_text.endswith("[...]"))


class GoogleTranslator(GummyAbstTranslator):
    """Google Translate is a free multilingual neural machine translation service
    developed by Google, to translate text and websites from one language into
    another. See https://translate.google.com/ for more info.
    """

    def __init__(
        self,
        driver: Optional[webdriver.Chrome] = None,
        maxsize: int = 5000,
        interval: int = 1,
        trials: int = 30,
        verbose: bool = False,
        use_cache: bool = True,
        specialize: bool = True,
        from_lang: str = "en",
        to_lang: str = "ja",
    ):
        super().__init__(
            driver=driver,
            maxsize=maxsize,
            interval=interval,
            trials=trials,
            verbose=verbose,
            use_cache=use_cache,
            specialize=specialize,
            from_lang=from_lang,
            to_lang=to_lang,
        )

    @property
    def supported_langs(self):
        return [
            "af",
            "am",
            "ar",
            "az",
            "be",
            "bg",
            "bn",
            "bs",
            "ca",
            "co",
            "cs",
            "cy",
            "da",
            "de",
            "el",
            "en",
            "eo",
            "es",
            "et",
            "eu",
            "fa",
            "fi",
            "fr",
            "fy",
            "ga",
            "gd",
            "gl",
            "gu",
            "ha",
            "hi",
            "hr",
            "ht",
            "hu",
            "hy",
            "id",
            "ig",
            "is",
            "it",
            "iw",
            "ja",
            "jw",
            "ka",
            "kk",
            "km",
            "kn",
            "ko",
            "ku",
            "ky",
            "la",
            "lb",
            "lo",
            "lt",
            "lv",
            "mg",
            "mi",
            "mk",
            "ml",
            "mn",
            "mr",
            "ms",
            "mt",
            "my",
            "ne",
            "nl",
            "no",
            "ny",
            "or",
            "pa",
            "pl",
            "ps",
            "pt",
            "ro",
            "ru",
            "rw",
            "sd",
            "si",
            "sk",
            "sl",
            "sm",
            "sn",
            "so",
            "sq",
            "sr",
            "st",
            "su",
            "sv",
            "sw",
            "ta",
            "te",
            "tg",
            "th",
            "tk",
            "tl",
            "tr",
            "tt",
            "ug",
            "uk",
            "ur",
            "uz",
            "vi",
            "xh",
            "yi",
            "yo",
            "zh",
            "zu",
        ]

    @staticmethod
    def find_translated_bulk(soup):
        return find_all_target_text(soup=soup, name="span", attrs={"jsname": "W297wb"}, joint="")

    @staticmethod
    def find_translated_corr(soup, driver):
        raise GummyImprementationError(toRED("Not Impremented."))

    def _translate(
        self,
        query: str,
        find_translated_bulk,
        find_translated_corr,
        is_translated_properly,
        url_fmt: str,
        correspond: bool = False,
        driver: Optional[webdriver.Chrome] = None,
        barname: Optional[str] = None,
    ):
        if correspond == True:
            warnings.warn(
                f"In {toGREEN('GoogleTranslator')}, the method {toBLUE('find_translated_corr')} is not implemented, so use {toBLUE('find_translated_bulk')} instead.",
                category=GummyImprementationWarning,
            )
            correspond = False
        return super()._translate(
            query=query,
            find_translated_bulk=find_translated_bulk,
            find_translated_corr=find_translated_corr,
            is_translated_properly=is_translated_properly,
            url_fmt=url_fmt,
            correspond=correspond,
            driver=driver,
            barname=barname,
        )

    def specialize2langs(self, from_lang: str, to_lang: str, **kwargs):
        url_fmt = f"https://translate.google.co.jp/#{from_lang}/{to_lang}/".replace("zh", "zh-CN") + "{query}"
        return (
            self.find_translated_bulk,
            self.find_translated_corr,
            self.is_translated_properly,
            url_fmt,
        )


all = TranslationGummyTranslators = {
    "google": GoogleTranslator,
    "deepl": DeepLTranslator,
}

get = mk_class_get(
    all_classes=TranslationGummyTranslators,
    gummy_abst_class=[GummyAbstTranslator],
    genre="translators",
)

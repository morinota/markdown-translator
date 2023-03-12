# coding: utf-8
"""This file defines a model that integrates all of :mod:`journals <gummy.journals>`, 
:mod:`translators <gummy.translators>`, :mod:`gateways <gummy.gateways>`, and 
it is possible to do all of the following at once.

1. Determine the ``journal_type`` of paper from the ``url`` or file extension.
2. If necessary, use a ``GummyGateway`` to access non-open content of the journal.
3. Parse the paper using ``GummyJournals`` and obtain the contents.
4. Translate the English obtained using ``GummyTranslators`` to Japanese.
5. Arrange Japanese and English according to the `templates <https://github.com/iwasakishuto/Translation-Gummy/tree/master/gummy/templates>`_ .
6. Convert the obtained HTML to PDF.

You can get (import) ``TranslationGummy`` by the following 2 ways.

.. code-block:: python

    >>> from gummy.models import TranslationGummy
    >>> from gummy import TranslationGummy
"""

import os
from typing import Dict, List, Optional, Tuple

from selenium import webdriver

import journals
import translators
from markdown_reader.markdown_content_class import MarkdownContent
from section_content_class import ContentInSection
from utils._path import GUMMY_DIR, TEMPLATES_DIR
from utils.coloring_utils import toACCENT, toBLUE, toGREEN
from utils.download_utils import match2path
from utils.driver_utils import get_driver
from utils.journal_utils import whichJournal
from utils.outfmt_utils import html2pdf, sanitize_filename, to_html
from utils.pdf_utils import addHighlightToPage, createHighlight


class TranslationGummy:
    """This class integrates all of the followings

    - :mod:`journals <gummy.journals>`
    - :mod:`translators <gummy.translators>`
    - :mod:`gateways <gummy.gateways>`

    Args:
        chrome_options (ChromeOptions)    : Instance of ChromeOptions. (default= :meth:`get_chrome_options() <gummy.utils.driver_utils.get_chrome_options>` )
        browser (bool)                    : Whether you want to run Chrome with GUI browser. (default= ``False`` )
        driver (WebDriver)                : Selenium WebDriver.
        gateway (str, GummyGateWay)       : identifier of the Gummy Gateway Class. See :mod:`gateways <gummy.gateways>`. (default= `"useless"`)
        translator (str, GummyTranslator) : identifier of the Gummy Translator Class. See :mod:`translators <gummy.translators>`. (default= `"deepl"`)
        maxsize (int)                     : Number of English characters that we can send a request at one time. (default= ``5000``)
        specialize (bool)                 : Whether to support multiple languages or specialize. (default= ``True``) If you want to specialize in translating between specific languages, set ``from_lang`` and ``to_lang`` arguments.
        from_lang (str)                   : Language before translation.
        to_lang (str)                     : Language after translation.
        verbose (bool)                    : Whether you want to print output or not. (default= ``True`` )
        translator_verbose (bool)         : Whether you want to print translator’s output or not. (default= ``False`` )
    """

    def __init__(
        self,
        chrome_options: Optional[webdriver.ChromeOptions] = None,
        browser: bool = False,
        driver: Optional[webdriver.Chrome] = None,
        gateway: str = "useless",
        translator: str = "deepl",
        maxsize: int = 5000,
        specialize: bool = True,
        from_lang: str = "en",
        to_lang: str = "ja",
        verbose: bool = True,
        translator_verbose: bool = True,
    ):
        self.driver: webdriver.Chrome = driver or get_driver(chrome_options=chrome_options, browser=browser)
        self.gateway = gateway
        self.translator: translators.DeepLTranslator = translators.get(
            translator,
            maxsize=maxsize,
            specialize=specialize,
            from_lang=from_lang,
            to_lang=to_lang,
            verbose=translator_verbose,
        )
        self.verbose = verbose
        self.to_lang = to_lang
        self.from_lang = from_lang

    def translate(
        self,
        query: str,
        barname: Optional[str] = None,
        from_lang: str = "en",
        to_lang: str = "ja",
        correspond: bool = False,
    ) -> str:
        """Translate English into Japanese. See :meth:`translate <gummy.translators.translate>`.

        Args:
            query (str)        : English to be translated.
            barname (str)      : Bar name for :meth:`ProgressMonitor <gummy.utils.monitor_utils.ProgressMonitor>`.
            from_lang (str)    : Language before translation.
            to_lang (str)      : Language after translation.
            correspond (bool)  : Whether to correspond the location of ``from_lang`` correspond to that of ``to_lang``.

        Examples:
            >>> from gummy import TranslationGummy
            >>> model = TranslationGummy()
            >>> ja = model.translate("This is a pen.")
            DeepLTranslator (query1) 03/30 [##------------------] 10.00% - 3.243[s]
            >>> print(ja)
            'これはペンです。'
        """
        return self.translator.translate(
            query=query,
            driver=self.driver,
            barname=barname,
            from_lang=from_lang,
            to_lang=to_lang,
            correspond=correspond,
        )

    def get_contents(
        self,
        url: str,
        journal_type: Optional[str] = None,
        crawl_type: Optional[str] = None,
        gateway: Optional[str] = None,
        **gatewaykwargs,
    ) -> Tuple[str, List[ContentInSection]]:
        """Get contents of the journal.

        Args:
            url (str)                   : URL of a paper or ``path/to/local.pdf``.
            journal_type (str)          : Journal type, if you not specify, judge by analyzing from ``url``.
            crawl_type (str)            : Crawling type, if you not specify, use recommended crawling type.
            gateway (str, GummyGateWay) : identifier of the Gummy Gateway Class. See :mod:`gateways <gummy.gateways>`. (default= ``None``)
            gatewaykwargs (dict)        : Gateway keywargs. See :meth:`passthrough <gummy.gateways.GummyAbstGateWay.passthrough>`.

        Returns:
            tuple (str, dict) : (title, content)

        Examples:
            >>> from gummy import TranslationGummy
            >>> model = TranslationGummy()
            >>> title, texts = model.get_contents("https://www.nature.com/articles/ncb0800_500")
            Estimated Journal Type : Nature
            Crawling Type: soup
                :
            >>> print(title)
            Formation of the male-specific muscle in female by ectopic expression
            >>> print(texts[:1])
            [{'head': 'Abstract', 'en': 'The  () gene product Fru has been ... for the sexually dimorphic actions of the gene.'}]
        """
        if journal_type is None:
            if os.path.exists(url):
                journal_type = "pdf"
            else:
                journal_type = whichJournal(url, driver=self.driver, verbose=self.verbose)
        gateway = gateway or self.gateway
        crawler: journals.NatureCrawler = journals.get(
            journal_type, gateway=gateway, sleep_for_loading=3, verbose=self.verbose
        )
        print(f"[LOG] crawler: {type(crawler)} is created")

        title, contents = crawler.get_contents(url=url, driver=self.driver, crawl_type=crawl_type, **gatewaykwargs)
        print(f"[DEBUG]type(texts):{type(contents)}")
        return title, contents

    def to_html(
        self,
        url: str,
        output_path: Optional[str] = None,
        out_dir: str = GUMMY_DIR,
        correspond: bool = True,
        journal_type: Optional[str] = None,
        crawl_type: Optional[str] = None,
        gateway: Optional[str] = None,
        searchpath: str = TEMPLATES_DIR,
        template: str = "paper.html",
        **gatewaykwargs,
    ) -> str:
        """Get contents from URL and create a HTML.

        Args:
            url (str)                   : URL of a paper or ``path/to/local.pdf``.
            path/out_dir (str)          : Where you save a created HTML. If path is None, save at ``<out_dir>/<title>.html`` (default= ``GUMMY_DIR``)
            from_lang (str)             : Language before translation.
            to_lang (str)               : Language after translation.
            correspond (bool)           : Whether to correspond the location of ``from_lang`` correspond to that of ``to_lang``.
            journal_type (str)          : Journal type, if you specify, use ``journal_type`` journal crawler. (default= `None`)
            crawl_type (str)            : Crawling type, if you not specify, use recommended crawling type. (default= `None`)
            gateway (str, GummyGateWay) : identifier of the Gummy Gateway Class. See :mod:`gateways <gummy.gateways>`. (default= `None`)
            searchpath/template (str)   : Use a ``<searchpath>/<template>`` tpl for creating HTML. (default= `TEMPLATES_DIR/paper.html`)
            gatewaykwargs (dict)        : Gateway keywargs. See :meth:`passthrough <gummy.gateways.GummyAbstGateWay.passthrough>`.
        return:
            filepath_output(str)
        """
        # BeautifulSoupでhtmlから情報を吸い上げて取得する
        title, contents = self.get_contents(
            url=url,
            journal_type=journal_type,
            crawl_type=crawl_type,
            gateway=gateway,
            **gatewaykwargs,
        )

        print(f"\nTranslation: {toACCENT(self.translator.name)}\n{'='*30}")

        len_contents = len(contents)
        # Combine split text for faster translation.
        if crawl_type == "pdf":
            # pdf独自の処理を含んだ翻訳処理(?)
            contents_translated = self._translate_pdf(
                contents,
                len_contents,
                correspond,
            )
        else:  # pdf以外は基本htmlのはず...?
            contents_translated = self._translate_html(
                contents,
                len_contents,
                correspond,
            )

        # 出力先のファイルパスを作る
        if output_path is None:
            output_path = os.path.join(out_dir, sanitize_filename(fp=title, dirname="."))

        # 翻訳前&翻訳後のテキストをHTML化
        htmlpath = to_html(
            output_path=output_path,
            title=title,
            contents=contents_translated,
            searchpath=searchpath,
            template=template,
            verbose=self.verbose,
        )
        return htmlpath

    def _translate_pdf(self, contents: List[Dict], len_contents: int, correspond: bool) -> List[Dict]:
        """翻訳対象がpdfの場合の場合の翻訳メソッド"""
        raw = ""  # クエリの初期値??

        contents_translated = []
        # htmlから取得した各タグのtextに対して、繰り返し処理
        for i, content in enumerate(contents):
            barname = f"[{i+1:>0{len(str(len_contents))}}/{len_contents}] " + toACCENT(content.get("head", "\t"))
            if "raw" in content:
                if content["raw"] == "":
                    content["raw"], content["translated"] = self.translator.translate_wrapper(
                        query=raw,
                        barname=barname,
                        from_lang=self.from_lang,
                        to_lang=self.to_lang,
                        correspond=correspond,
                    )
                    raw = ""  # クエリをリセット
                else:
                    # dict.pop(key): 指定されたkeyを削除し、削除されたvalueを返す
                    raw += " " + content.pop("raw")  # 削除されたvalueをクエリにつなぐ...?
            elif "img" in content and self.verbose:
                print(barname + "<img>")

            # クエリが初期値ではなくなっていたら...?
            if len(raw) > 0:
                content["raw"], content["translated"] = self.translator.translate_wrapper(
                    query=raw,
                    barname=barname,
                    from_lang=self.from_lang,
                    to_lang=self.to_lang,
                    correspond=correspond,
                )

            contents_translated.append(content)

        return contents_translated

    def _translate_html(self, contents: List[ContentInSection], correspond: bool) -> List[ContentInSection]:
        """翻訳対象がhtmlの場合の場合の翻訳メソッド"""
        contents_translated = []
        print(f"[debug] {type(self.translator)}")
        # htmlから取得した各タグのtextに対して、繰り返し処理?
        length_contents = len(contents)
        for idx, content in enumerate(contents):
            print(f"[LOG] {idx+1}/{length_contents}========================")
            # 返り値でcontentをreplaceしている
            content_translated = self._tranlate_each_content(
                content=content,
                correspond=correspond,
            )
            if (
                content_translated.tag_name != "img"
                and len(content_translated.tag_text_original) != 0
                and len(content_translated.tag_text_translated) == 0
            ):
                content_translated.print_properties()
                raise ValueError("something of bag is happend.")

            contents_translated.append(content_translated)

        return contents_translated

    def _tranlate_each_content(self, content: ContentInSection, correspond: bool = True) -> ContentInSection:
        """htmlから取得した各タグに対して、テキストを抽出し、翻訳前(raw)&翻訳後(raw)のテキストをDictに格納して返す"""
        if content.tag_name == "img":
            return content

        content.tag_text_original_separated, content.tag_text_translated_separated = self.translator.translate_wrapper(
            query=content.tag_text_original,
            driver=self.driver,
            correspond=correspond,
        )

        # TODO:何故かseparatedが二重にListの要素が入っているので、後で修正する。(暫定でスライス)
        actual_length = int(len(content.tag_text_original_separated) / 2)
        content.tag_text_original_separated = content.tag_text_original_separated[:actual_length]
        actual_length = int(len(content.tag_text_translated_separated) / 2)
        content.tag_text_translated_separated = content.tag_text_translated_separated[:actual_length]

        content.tag_text_translated = " ".join(content.tag_text_translated_separated)
        return content

    def translate_markdown(self, md_contents: List[MarkdownContent], correspond: bool) -> List[MarkdownContent]:
        """MarkdownContentのListを受け取り、翻訳した情報をtext_translatedに格納して返す
        Parameters
        ----------
        md_contents : List[MarkdownContent]

        Returns
        -------
        List[MarkdownContent]
        """
        md_contents_translated = []
        print(f"[debug] {type(self.translator)}")
        # htmlから取得した各タグのtextに対して、繰り返し処理?
        length_contents = len(md_contents)
        for idx, md_content in enumerate(md_contents):
            print(f"[LOG] {idx+1}/{length_contents}========================")
            md_content_translated = self._tranlate_each_md_content(
                md_content,
                correspond=correspond,
            )
            md_contents_translated.append(md_content_translated)

        return md_contents_translated

    def _tranlate_each_md_content(self, md_content: MarkdownContent, correspond: bool) -> MarkdownContent:
        if md_content.tag_name in MarkdownContent.NON_TRANSLATE_TAGS:
            md_content.text_translated = md_content.text_raw
            return md_content

        raw_text_list, translated_text_list = self.translator.translate_wrapper(
            query=md_content.text_raw,
            driver=self.driver,
            correspond=correspond,
        )
        # TODO:何故かseparatedが二重にListの要素が入っているので、後で修正する。(暫定でスライス)
        actual_length = int(len(raw_text_list) / 2)
        raw_text_list = raw_text_list[:actual_length]
        actual_length = int(len(translated_text_list) / 2)
        translated_text_list = translated_text_list[:actual_length]

        return MarkdownContent(
            tag_name=md_content.tag_name,
            text_raw=md_content.text_raw,
            text_translated=" ".join(translated_text_list),
            text_raw_list=raw_text_list,
            text_translated_list=translated_text_list,
        )

    def toPDF(
        self,
        url,
        path=None,
        out_dir=GUMMY_DIR,
        from_lang="en",
        to_lang="ja",
        correspond=True,
        journal_type=None,
        crawl_type=None,
        gateway=None,
        searchpath=TEMPLATES_DIR,
        template="paper.html",
        delete_html=True,
        options={},
        **gatewaykwargs,
    ):
        """Get contents from URL and create a PDF.

        Args:
            url (str)                   : URL of a paper or ``path/to/local.pdf``.
            path/out_dir (str)          : Where you save a created HTML. If path is None, save at ``<out_dir>/<title>.html`` (default= ``GUMMY_DIR``)
            from_lang (str)             : Language before translation.
            to_lang (str)               : Language after translation.
            correspond (bool)           : Whether to correspond the location of ``from_lang`` correspond to that of ``to_lang``.
            journal_type (str)          : Journal type, if you specify, use ``journal_type`` journal crawler. (default= `None`)
            crawl_type (str)            : Crawling type, if you not specify, use recommended crawling type. (default= `None`)
            gateway (str, GummyGateWay) : identifier of the Gummy Gateway Class. See :mod:`gateways <gummy.gateways>`. (default= `None`)
            searchpath/template (str)   : Use a ``<searchpath>/<template>`` tpl for creating HTML. (default= `TEMPLATES_DIR/paper.html`)
            delete_html (bool)          : Whether you want to delete an intermediate html file. (default= `True`)
            options (dict)              : Options for wkhtmltopdf. See https://wkhtmltopdf.org/usage/wkhtmltopdf.txt (default= `{}`)
            gatewaykwargs (dict)        : Gateway keywargs. See :meth:`passthrough <gummy.gateways.GummyAbstGateWay.passthrough>`.
        """
        htmlpath = self.to_html(
            url=url,
            output_path=path,
            out_dir=out_dir,
            from_lang=from_lang,
            to_lang=to_lang,
            correspond=correspond,
            journal_type=journal_type,
            crawl_type=crawl_type,
            gateway=gateway,
            searchpath=searchpath,
            template=template,
            **gatewaykwargs,
        )
        if self.verbose:
            print(f"\nConvert from HTML to PDF\n{'='*30}")
        pdfpath = html2pdf(
            path=htmlpath,
            delete_html=delete_html,
            verbose=self.verbose,
            options=options,
        )
        return pdfpath

    def highlight(
        self,
        url,
        path=None,
        out_dir=GUMMY_DIR,
        from_lang="en",
        to_lang="ja",
        journal_type=None,
        gateway=None,
        ignore_length=10,
        highlight_color=[1, 1, 0],
        **gatewaykwargs,
    ):
        """Get contents from URL and create a PDF.

        Args:
            url (str)                   : URL of a paper or ``path/to/local.pdf``.
            path/out_dir (str)          : Where you save a created HTML. If path is None, save at ``<out_dir>/<title>.html`` (default= ``GUMMY_DIR``)
            from_lang (str)             : Language before translation.
            to_lang (str)               : Language after translation.
            journal_type (str)          : Journal type, if you specify, use ``journal_type`` journal crawler. (default= `None`)
            gateway (str, GummyGateWay) : identifier of the Gummy Gateway Class. See :mod:`gateways <gummy.gateways>`. (default= `None`)
            ignore_length (int)         : If the number of English characters is smaller than ``ignore_length`` , do not highlight
            highlight_color (list)      : The highlight color.
            gatewaykwargs (dict)        : Gateway keywargs. See :meth:`passthrough <gummy.gateways.GummyAbstGateWay.passthrough>`.
        """
        from PyPDF2 import PdfFileReader, PdfFileWriter

        title, contents = self.get_contents(
            url=url,
            journal_type=journal_type,
            crawl_type="pdf",
            gateway=gateway,
            **gatewaykwargs,
        )
        path_ = match2path(url, dirname=out_dir)
        out_path = path or os.path.join(out_dir, "_higlighted".join(os.path.splitext(os.path.basename(path_))))
        with open(path_, "rb") as inPdf:
            pdfInput = PdfFileReader(inPdf)
            pdfOutput = PdfFileWriter()
            page_no = 0
            len_contents = len(contents)
            for i, content in enumerate(contents):
                if "head" in content:
                    if page_no > 0:
                        pdfOutput.addPage(page)
                    page = pdfInput.getPage(page_no)
                    page_no += 1
                raw = content.get("raw", "")
                if raw == "" or len(raw) < ignore_length:
                    continue
                barname = f"[page.{page_no} {i+1:>0{len(str(len_contents))}}/{len_contents}] "
                translated = self.translator.translate(
                    query=raw,
                    barname=barname,
                    from_lang=from_lang,
                    to_lang=to_lang,
                    correspond=False,
                )
                highlight = createHighlight(bbox=content["bbox"], color=highlight_color, contents=translated)
                addHighlightToPage(highlight, page, pdfOutput)
            pdfOutput.addPage(page)
            with open(out_path, "wb") as outPdf:
                pdfOutput.write(outPdf)
            print(f"{toBLUE(out_path)} is created.")
        return out_path

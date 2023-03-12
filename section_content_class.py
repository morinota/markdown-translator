from dataclasses import dataclass
from typing import Dict, List

import bs4


@dataclass
class ContentInSection:
    HEADER_TAG = "h2"
    SUBHEADER_TAG = "h3"
    IMAGE_TAG = "img"
    PARAGRAPH_TAG = "p"

    tag_obj: bs4.element.Tag
    tag_name: str
    tag_text_original: str = None  # raw text
    tag_text_translated: str = None
    tag_text_original_separated: List[str] = None
    tag_text_translated_separated: List[str] = None

    def print_properties(self) -> None:
        print(f"tag_obj: {self.tag_obj}")
        print(f"tag_name: {self.tag_name}")
        print(f"tag_text_original: {self.tag_text_original}")
        print(f"tag_text_translated: {self.tag_text_translated}")
        print("=" * 10)
        print(f"tag_text_original_separated: {self.tag_text_original_separated}")
        print(f"tag_text_translated_separated: {self.tag_text_translated_separated}")
        # print(f"tag_text_original_separated: {self.tag_text_original_separated}")
        # print(f"tag_text_translated_separated: {self.tag_text_translated_separated}")

    def convert_format_for_html(self) -> Dict:
        """keyは["raw", "head", "subhead", "img"]の内のどれか1つ & "translated"の合計２つ。
        各センテンス毎に色分けしたい為、raw及びtranslatedに格納するテキスト情報は
        tag_text_original_separated及びtag_text_translated_separatedを用いる。
        """
        dict_for_html = {}
        if self.tag_name == ContentInSection.IMAGE_TAG:
            dict_for_html["img"] = self.tag_text_original  # imgのみsepalatedを取得していない
            return dict_for_html
        elif self.tag_name == ContentInSection.HEADER_TAG:
            dict_for_html["head"] = self.tag_text_original
        elif self.tag_name == ContentInSection.SUBHEADER_TAG:
            dict_for_html["subhead"] = self.tag_text_original
        elif self.tag_name == ContentInSection.PARAGRAPH_TAG:
            dict_for_html["raw"] = self.tag_text_original_separated

        dict_for_html["translated"] = self.tag_text_translated_separated
        return dict_for_html

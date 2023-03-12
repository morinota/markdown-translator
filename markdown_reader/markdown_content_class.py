import re
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class MarkdownContent:
    """.mdファイルの各Contentの内容を格納するデータクラス"""

    NON_TRANSLATE_TAGS = ["equation", "img", "code_block"]
    HEADER_TAGS = ["h1", "h2", "h3", "h4"]
    LI_TAGS = ["li", "number_li"]

    H1_TAG_PATTERN = re.compile(r"# .*")
    H2_TAG_PATTERN = re.compile(r"## .*")
    H3_TAG_PATTERN = re.compile(r"### .*")
    H4_TAG_PATTERN = re.compile(r"#### .*")
    EQUATION_PATTERN = re.compile(r"\$\$.*")  # ex) $$ \tilde{x} $$
    LI_TAG_PATTERN = re.compile(r"- .*")  # ex) - hogehoge
    NUMBER_LI_TAG_PATTERN = re.compile(r"[0-9]+\. .*")  # ex) 1. hogehoge
    IMG_TAG_PATTERN_1 = re.compile(r"!\[.*\]\(.*\)")  # ex) ![](image_url)
    IMG_TAG_PATTERN_2 = re.compile(r"<img .*>")  # ex) ![](image_url)
    CODE_BLOCK_PATTERN = r"```.*"

    tag_name: str  # htmlにおけるtag name
    text_raw: str
    text_translated: str
    text_raw_list: Optional[List[str]] = None  # 各sentence毎に分割したver.
    text_translated_list: Optional[List[str]] = None

    @classmethod
    def from_str(cls, text_raw: str) -> "MarkdownContent":
        if MarkdownContent.H1_TAG_PATTERN.match(text_raw):
            tag_name = "h1"
        elif MarkdownContent.H2_TAG_PATTERN.match(text_raw):
            tag_name = "h2"
        elif MarkdownContent.H3_TAG_PATTERN.match(text_raw):
            tag_name = "h3"
        elif MarkdownContent.H4_TAG_PATTERN.match(text_raw):
            tag_name = "h4"
        elif MarkdownContent.EQUATION_PATTERN.match(text_raw):
            tag_name = "equation"
        elif MarkdownContent.LI_TAG_PATTERN.match(text_raw):
            tag_name = "li"
        elif MarkdownContent.NUMBER_LI_TAG_PATTERN.match(text_raw):
            tag_name = "number_li"
        elif MarkdownContent.IMG_TAG_PATTERN_1.match(text_raw) or MarkdownContent.IMG_TAG_PATTERN_2.match(text_raw):
            tag_name = "img"
        elif re.match(MarkdownContent.CODE_BLOCK_PATTERN, text_raw):
            tag_name = "code_block"
        else:
            tag_name = "p"
        return MarkdownContent(
            tag_name=tag_name,
            text_raw=text_raw,
            text_translated="",
        )

    def to_str(self) -> str:
        if self.tag_name in MarkdownContent.NON_TRANSLATE_TAGS:
            return self.text_raw
        if self.tag_name in MarkdownContent.HEADER_TAGS:
            text_translated_removed_tag_list = self.text_translated.split(" ")[1:]
            text_translated_removed_tag = " ".join(text_translated_removed_tag_list)
            return f"{self.text_raw} {text_translated_removed_tag}"

        if self.tag_name in MarkdownContent.LI_TAGS:
            # 先頭の"- "や"1. "を取り除く。
            text_translated_removed_li = " ".join(self.text_translated.split(" ")[1:])
            return f"{self.text_raw} {text_translated_removed_li}"

        sentence_pairs = [
            f"{raw}\n{translated}" for raw, translated in zip(self.text_raw_list, self.text_translated_list)
        ]
        return "\n".join(sentence_pairs)

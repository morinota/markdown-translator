import abc
import dataclasses
import re
from enum import Enum


class MarkdownTagPattern(Enum):
    HEADER_1 = re.compile(r"# .*")
    HEADER_2 = re.compile(r"## .*")
    HEADER_3 = re.compile(r"### .*")
    HEADER_4 = re.compile(r"#### .*")
    EQUATION = re.compile(r"\$\$.*")  # ex) $$ \tilde{x} $$
    LIST_ITEM = re.compile(r"- .*")
    NUMBER_LIST_ITEM = re.compile(r"[0-9]+\. .*")  # ex) 1. hogehoge
    IMAGE_1 = re.compile(r"!\[.*\]\(.*\)")  # ex) ![](image_url)
    IMAGE_2 = re.compile(r"<img .*>")  # ex) ![](image_url)
    CODE_BLOCK = re.compile(r"```.*")


class MarkdownTagName(Enum):
    HEADER_1 = "h1"
    HEADER_2 = "h2"
    HEADER_3 = "h3"
    HEADER_4 = "h4"
    EQUATION = "equation"
    LIST_ITEM = "li"
    NUMBER_LIST_ITEM = "number_li"
    IMAGE = "img"
    CODE_BLOCK = "code_block"
    PLAIN_TEXT = "plain_text"


@dataclasses.dataclass
class MarkdownContentBase(abc.ABC):
    tag_name: MarkdownTagName  # htmlにおけるtag name
    text_raw: str

"""仮想環境nlp_moritaで実行してください。
errorで実行できない時は、
=>現在のGoogle chromeとchorome driverのバージョンが一致してない事が多いです。
chromeのVersionを確認して(error messageでも教えてくれます)、chrome driverをインストールし直してください。
web driver:webブラウザから自動で処理をするために必要なツール。chromeの場合はchrome driver.
chrome driverはr"c\Program files\"にあります。
"""

from pathlib import Path

from models import TranslationGummy
from utils.outfmt_utils import to_html

IS_DEBUG_MODE = False


def main(input_path: Path, output_path: Path) -> None:

    gummy = TranslationGummy(gateway="useless", translator="deepl")

    title_str, contents = gummy.get_contents(
        url=str(input_path), journal_type="Nature", crawl_type="soup", gateway=None
    )
    # TODO: 各sectionを取り出すタイミングで、h2のsection_tagにh3のセクションタグが含まれてしまっている。また更にh3のセクションタグも取得してしまっている。
    if IS_DEBUG_MODE:
        contents = contents[0:35]

    contents_translated = gummy._translate_html(contents, correspond=True)

    for content in contents_translated:
        if content.tag_name == "img":
            continue
        content.print_properties()
        # print(content)
        print("\n")

    # htmlのtemplateに渡す為に、dictに変換
    contents_translated_reformat = [content.convert_format_for_html() for content in contents_translated]

    output_path = to_html(
        str(output_path),
        contents_translated_reformat,
        title_str,
    )


if __name__ == "__main__":
    input_path = Path(
        r"C:\Users\Masat\デスクトップ_Instead\webアプリ開発\2020-Morita\translator\target_html\ozgobek_et_al_2019.html"
    )
    output_path = input_path.parent.joinpath(f"{input_path.stem}_trans{input_path.suffix}")

    main(input_path, output_path)

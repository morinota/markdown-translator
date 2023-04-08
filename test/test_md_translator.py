from urllib import parse

from markdown_translator.md_translator import DeepLTranslator


def test_parse_query() -> None:
    from_lang, to_lang = "en", "ja"
    original_query = "We further consider user return pattern as a supplement to click / no click label in order to capture more user feedback information."
    # 手動でdeepLにコピペした際は、"/"が"5C%2F"にparseされる.("5C"は"¥"のurl encode, "2F"は"/"のurl encode)
    url_expected = r"https://www.deepl.com/translator#en/ja/We%20further%20consider%20user%20return%20pattern%20as%20a%20supplement%20to%20click%20%5C%2F%20no%20click%20label%20in%20order%20to%20capture%20more%20user%20feedback%20information."

    parsed_query_actual = DeepLTranslator._parse_query(original_query)
    assert f"https://www.deepl.com/translator#{from_lang}/{to_lang}/{parsed_query_actual}" == url_expected


def test_split_querys() -> None:
    base_query = "A is B. B is C. Hoge is based on Morita et al. (2023). Gupta et al.[12] proposed hogehoge."
    splited_querys_expected = [
        "A is B.",
        "B is C.",
        "Hoge is based on Morita et al.",
        "(2023).",
        "Gupta et al.[12] proposed hogehoge.",
    ]

    splited_querys_actual = DeepLTranslator._split_querys(base_query)
    assert splited_querys_actual == splited_querys_expected


def test_preprocess() -> None:
    base_query_1 = "Hoge is based on Morita et al. (2023)."
    preprocessed_query_expected_1 = "Hoge is based on Morita et al.(2023)."

    preprocessed_query_actual = DeepLTranslator._preprocess(base_query_1)

    assert preprocessed_query_actual == preprocessed_query_expected_1

    base_query_2 = "According to Fig. 8, the results have similar patterns."
    preprocessed_query_expected_2 = "According to Fig.8, the results have similar patterns."
    preprocessed_query_actual = DeepLTranslator._preprocess(base_query_2)

    assert preprocessed_query_actual == preprocessed_query_expected_2

    base_query_3 = "Gupta et al. [12] proposed hogehoge."
    preprocessed_query_expected_3 = "Gupta et al.[12] proposed hogehoge."
    preprocessed_query_actual = DeepLTranslator._preprocess(base_query_3)

    assert preprocessed_query_actual == preprocessed_query_expected_3

    base_query_4 = "Hoge is Hoge. Fuga is Fuga. Piyo is Piyo."
    preprocessed_query_expected_4 = "Hoge is Hoge. Fuga is Fuga. Piyo is Piyo."
    preprocessed_query_actual = DeepLTranslator._preprocess(base_query_4)

    assert preprocessed_query_actual == preprocessed_query_expected_4

    base_query_5 = "See e.g. [13]. I like A. (i.e. I love A.)"
    preprocessed_query_expected_5 = "See e.g.[13]. I like A. (i.e.I love A.)"
    preprocessed_query_actual = DeepLTranslator._preprocess(base_query_5)

    assert preprocessed_query_actual == preprocessed_query_expected_5

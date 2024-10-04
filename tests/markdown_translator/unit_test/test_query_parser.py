from markdown_translator.markdown_translator.query_parser import QueryParser


BASE_URL = "https://www.deepl.com/translator#en/ja"


def test_parser_works_correctly_to_a_query_including_forward_slash() -> None:
    # Arrange
    from_lang, to_lang = "en", "ja"
    original_query = "We further consider user return pattern as a supplement to click / no click label in order to capture more user feedback information."
    sut = QueryParser()

    # Act
    parsed_query = sut.parse(original_query)

    # Assert
    # 手動でdeepLにコピペした際は、"/"が"5C%2F"にparseされる.("5C"は"¥"のurl encode, "2F"は"/"のurl encode)
    parsed_query_expected = r"We%20further%20consider%20user%20return%20pattern%20as%20a%20supplement%20to%20click%20%5C%2F%20no%20click%20label%20in%20order%20to%20capture%20more%20user%20feedback%20information."
    assert f"{BASE_URL}/{parsed_query}" == f"{BASE_URL}/{parsed_query_expected}"


def test_parser_works_correctly_to_a_query_including_pipe() -> None:
    # Arrange
    from_lang, to_lang = "en", "ja"
    original_query = "Given a sample from P(O|P), we can think of the IPS estimator."
    sut = QueryParser()

    # Act
    parsed_query = sut.parse(original_query)

    # Assert
    parsed_query_expected = r"Given%20a%20sample%20from%20P(O%5C%7CP)%2C%20we%20can%20think%20of%20the%20IPS%20estimator."
    assert f"{BASE_URL}/{parsed_query}" == f"{BASE_URL}/{parsed_query_expected}"


def test_parse_function_adjust_when_query_include_double_quart_and_F() -> None:
    """query内に["F]が含まれる場合に、[%22F]とparseされて欲しい。
    しかし、[%25C%2F]に変換されて翻訳が切れるケースが発生した為、本テストケースを追加した。
    """
    # Arrange
    from_lang, to_lang = "en", "ja"
    original_query = 'A is "Featured" fuga.'
    sut = QueryParser()

    # Act
    parsed_query = sut.parse(original_query)

    # Assert
    parsed_query_expected = r"A%20is%20%22Featured%22%20fuga."
    assert f"{BASE_URL}/{parsed_query}" == f"{BASE_URL}/{parsed_query_expected}"


def test_parse_query_add_newline_when_colon_whitespace() -> None:
    """
    文中の[: ]をシンプルに"%3A%20"にparseすると、翻訳が途切れるケースが発生した。
    よって"%3A%20%0A"としてparseさせる(改行を追加する)ようにして対応する。
    """
    # Arrange
    from_lang, to_lang = "en", "ja"
    original_query = "A will discuss an example: where A is B."
    sut = QueryParser()

    # Act
    parsed_query = sut.parse(original_query)

    # Assert
    parsed_query_expected = (
        r"A%20will%20discuss%20an%20example%3A%20%0Awhere%20A%20is%20B."
    )
    assert f"{BASE_URL}/{parsed_query}" == f"{BASE_URL}/{parsed_query_expected}"

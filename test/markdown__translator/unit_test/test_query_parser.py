from markdown_translator.query_parser import QueryParser


class TestParseQuery:
    def test_parser_works_correctly_to_a_query_including_forward_slash(self) -> None:
        # Arrange
        from_lang, to_lang = "en", "ja"
        original_query = "We further consider user return pattern as a supplement to click / no click label in order to capture more user feedback information."
        sut = QueryParser()

        # Act
        parsed_query = sut.parse(original_query)

        # Assert
        # 手動でdeepLにコピペした際は、"/"が"5C%2F"にparseされる.("5C"は"¥"のurl encode, "2F"は"/"のurl encode)
        url_expected = r"https://www.deepl.com/translator#en/ja/We%20further%20consider%20user%20return%20pattern%20as%20a%20supplement%20to%20click%20%5C%2F%20no%20click%20label%20in%20order%20to%20capture%20more%20user%20feedback%20information."
        assert f"https://www.deepl.com/translator#{from_lang}/{to_lang}/{parsed_query}" == url_expected

    def test_parser_works_correctly_to_a_query_including_pipe(self) -> None:
        # Arrange
        from_lang, to_lang = "en", "ja"
        original_query = "Given a sample from P(O|P), we can think of the IPS estimator."
        sut = QueryParser()

        # Act
        parsed_query = sut.parse(original_query)

        # Assert
        url_expected = r"https://www.deepl.com/translator#en/ja/Given%20a%20sample%20from%20P(O%5C%7CP)%2C%20we%20can%20think%20of%20the%20IPS%20estimator."
        assert f"https://www.deepl.com/translator#{from_lang}/{to_lang}/{parsed_query}" == url_expected

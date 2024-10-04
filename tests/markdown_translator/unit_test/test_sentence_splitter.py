from markdown_translator.markdown_translator.sentence_splitter import SentenceSplitter


class TestSentenceSplitter:
    def test_sentences_writtern_in_one_line_is_splitted(self) -> None:
        # Arrange
        one_line_sentence = "According to Fig. 8, A is B. Hoge is based on Morita et al. (2023). Gupta et al. [12] proposed hogehoge. See e.g. [13]."
        sut = SentenceSplitter()

        # Act
        splitted_sentences = sut.split(one_line_sentence)

        # Assert
        splited_sentences_expected = [
            "According to Fig.8, A is B.",
            "Hoge is based on Morita et al.(2023).",
            "Gupta et al.[12] proposed hogehoge.",
            "See e.g.[13].",
        ]
        assert splitted_sentences == splited_sentences_expected

    def test_one_sentence_is_not_splitted_and_just_convert_to_list_of_str(self) -> None:
        # Arrange
        one_line_sentence = "According to Fig. 8, A is B."
        sut = SentenceSplitter()

        # Act
        splitted_sentences = sut.split(one_line_sentence)

        # Assert
        splited_sentences_expected = [
            "According to Fig.8, A is B.",
        ]
        assert splitted_sentences == splited_sentences_expected

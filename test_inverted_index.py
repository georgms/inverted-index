from Sorstr import Sorstr

sorstr = Sorstr()
sorstr.index('test_resources/*.txt')


def assert_result(query, expected):
    actual = sorstr.search(query)
    assert expected == actual


def test_multiple_words_with_multiple_results_are_found():
    assert_result('is text', ['1.txt', '2.txt', '3.txt'])


def test_multiple_words_with_single_result_is_found():
    assert_result('is another', ['2.txt'])


def test_search_is_case_insensitive():
    result = sorstr.search('Is Another')
    lc_result = sorstr.search('is another')
    assert result == lc_result


def test_single_word_with_multiple_results_is_found():
    assert_result('text', ['1.txt', '2.txt', '3.txt'])


def test_non_existing_word_does_not_fail():
    assert_result('blubbergurken', [])


def test_existing_and_non_existing_word_returns_empty_result():
    assert_result('text blubbergurken', [])

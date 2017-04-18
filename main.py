from Sorstr import Sorstr


def ask_for_query():
    """
    Prompt the user for a search query.

    :return: The user input.
    """
    print('Enter query, empty to quit:')
    query = input('? ')
    return query


def main():
    sorstr = Sorstr()

    pattern = 'resources/*.txt'
    sorstr.index(pattern)
    while True:
        query = ask_for_query()

        if query == '':
            break

        results = sorstr.search(query)
        print(results)


main()

from Sorstr import Sorstr


def ask_for_query():
    """
    Prompt the user for a search query.

    :return: The user input.
    """
    print('Enter query, empty to quit:')
    try:
        query = input('? ')
    except EOFError:
        # User has cancelled
        return False

    return query


def main():
    sorstr = Sorstr()

    pattern = 'resources/*.txt'
    sorstr.index(pattern)
    while True:
        query = ask_for_query()

        if not query or query == '':
            break

        results = sorstr.search(query)
        print(results)

if __name__ == '__main__':
    main()

import os
import re
from glob import glob


class Sorstr:
    def __init__(self):
        self.inverted_index = {}

    def index(self, pattern: str) -> None:
        """
        Index files indicated by the pattern.

        :param pattern: The pattern to use to look for files
        """

        files = glob(pattern)
        for filename in files:
            self.index_file(filename)

    def index_file(self, filename: str) -> None:
        """
        Process a file and add the contents to the index.

        :param filename: The name of the file to process.
        """

        with open(filename, 'r') as f:
            contents = f.read()
            terms = Sorstr.tokenize(contents)
            for term in terms:
                self.add_term(os.path.basename(filename), term)

    def add_term(self, filename: str, term: str) -> None:
        """
        Add a filename-term tuple to the index.

        :param filename: The filename.
        :param term: The term.
        """

        if term not in self.inverted_index:
            self.inverted_index[term] = [filename]
        else:
            self.inverted_index[term].append(filename)

    def search(self, query: str) -> list:
        """
        Search the index for the query.

        :param query: The query to search.
        :return: The list of files matching the query.
        """
        matching_files = []
        query_terms = Sorstr.tokenize(query)

        for query_term in query_terms:
            postings = self.inverted_index.get(query_term)

            # No results found for this query term. Since we're using AND search we can abort right away.
            if not postings:
                matching_files = []
                break

            if not matching_files:
                matching_files = postings
            else:
                matching_files = Sorstr.intersect_results(matching_files, postings)

        # Sort results for stable result order
        matching_files.sort()

        return matching_files

    @staticmethod
    def tokenize(text: str) -> list:
        """
        Tokenize the incoming text.

        Currently just splits on whitespace and non-word characters, so it will return sequences of alphanumeric
        characters.

        Tokens will be lower-cased.

        :param text: The text to tokenize
        :return: The tokens
        """
        text = text.lower()
        tokens = re.split('[\s\W]+', text)
        # Filter out empty terms
        tokens  = list(filter(None, tokens))
        return tokens

    @staticmethod
    def intersect_results(matching_files: list, postings: list) -> list:
        """
        Intersect the results so far with the results for the current query term.

        :param matching_files: The results so far.
        :param postings: The results for the current query term.
        :return: The intersection of the two lists.
        """
        for matching_file in matching_files:
            if matching_file not in postings:
                matching_files.remove(matching_file)

        return matching_files

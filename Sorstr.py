from glob import glob

import re


class Sorstr:
    inverted_index = {}

    def index(self, pattern: str) -> None:
        """
        Index files indicated by the pattern.

        :param pattern: The pattern to use to look for files 
        """
        self.inverted_index = {}

        files = glob(pattern)
        files.sort()
        for file in files:
            with open(file, 'r') as f:
                contents = f.read().lower()
                terms = re.split('[\s\W]+', contents)
                terms = list(filter(None, terms))
                for term in terms:
                    if term not in self.inverted_index:
                        self.inverted_index[term] = [file]
                    else:
                        self.inverted_index[term].append(file)

    def search(self, query: str) -> list:
        """
        Search the index for the query.
        
        :param query: The query to search. 
        :return: The list of files matching the query. 
        """
        matching_files = []
        query_terms = re.split('[\s\W]+', query.lower())

        for query_term in query_terms:
            postings = self.inverted_index.get(query_term)

            # No results found for this query term. Since we're using AND search we can abort right away.
            if not postings:
                matching_files = []
                break

            if not matching_files:
                matching_files = postings
            else:
                for matching_file in matching_files:
                    if matching_file not in postings:
                        matching_files.remove(matching_file)

        return matching_files

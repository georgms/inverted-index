import os
from collections import Counter, OrderedDict
from glob import glob

import re


class Term:
    def __init__(self):
        self.postings = {}


class Posting:
    def __init__(self, num_occurrences):
        self.num_occurrences = num_occurrences


class FileStats:
    def __init__(self, filename, num_terms, num_unique_terms):
        self.filename = filename
        self.num_terms = num_terms
        self.num_unique_terms = num_unique_terms


class Result:
    def __init__(self, filename, file_stats):
        self.filename = filename
        self.file_stats = file_stats
        self.score = 0
        self.matches = {}

    def add_match(self, match, posting):
        self.matches[match] = posting.num_occurrences
        #self.score += posting.num_occurrences / self.file_stats.num_terms
        self.score += posting.num_occurrences

    def __str__(self):
        #output = '{}: score {:.2} with {} terms and {} unique terms'.format(self.filename, self.score,
        #                                                                    self.file_stats.num_terms,
        #                                                                    self.file_stats.num_unique_terms) + "\n"
        output = '{}: score {}'.format(self.filename, self.score) + "\n"
        for query_term, num_occurrences in self.matches.items():
            output += "\t" + '{}: {}'.format(query_term, num_occurrences) + "\n"

        return output


class Sorstr:
    inverted_index = {}
    file_stats = {}

    def index(self, pattern: str) -> None:
        """
        Index files indicated by the pattern.

        :param pattern: The pattern to use to look for files 
        """
        self.inverted_index = {}

        files = glob(pattern)
        files.sort()
        for file in files:
            filename = os.path.basename(file)

            with open(file, 'r') as f:
                contents = f.read().lower()
                # Split file contents on whitespace and non-word characters
                terms = re.split('[\s\W]+', contents)
                # Filter out empty terms that may result from the splitting
                terms = list(filter(None, terms))
                term_occurrences = Counter(terms)

                num_terms = len(terms)
                num_unique_terms = len(term_occurrences.keys())
                self.file_stats[filename] = FileStats(filename, num_terms, num_unique_terms)

                for term, num_occurrences in term_occurrences.items():
                    if term not in self.inverted_index:
                        self.inverted_index[term] = Term()

                    posting = Posting(num_occurrences)
                    self.inverted_index[term].postings[filename] = posting

        for term, term_info in self.inverted_index.items():
            term_info.idf = len(files) / len(term_info.postings)

    def search(self, query: str):
        """
        Search the index for the query.
        
        :param query: The query to search. 
        :return: The list of files matching the query. 
        """
        matching_files = {}
        query_terms = re.split('\s+', query)

        for query_term in query_terms:
            if not self.inverted_index.get(query_term):
                break

            postings = self.inverted_index.get(query_term).postings

            if not matching_files:

                for filename, num_occurrences in postings.items():
                    if filename not in matching_files:
                        matching_files[filename] = Result(filename, self.file_stats[filename])
                    matching_files[filename].add_match(query_term, num_occurrences)

            else:
                # Copy the list of matching files so far, so we can iterate and remove elements.
                new_matching_files = matching_files.copy()
                for matching_file in matching_files:
                    if matching_file not in postings:
                        del new_matching_files[matching_file]
                    else:
                        new_matching_files[matching_file].add_match(query_term, postings[matching_file])

                # Keep working with the new list
                matching_files = new_matching_files

        matching_files = OrderedDict(sorted(matching_files.items(), key=lambda x: x[1].score, reverse=True))

        num_results = len(matching_files)
        if num_results == 0:
            print('No results found')
        else:
            max_results = 5
            showing = 'all' if num_results <= max_results else 'top ' + str(max_results)
            print('Found {} results, showing {}'.format(len(matching_files), showing) + "\n")

            count = 0
            for result in matching_files.values():
                print(str(result))

                count += 1
                if count >= max_results:
                    break

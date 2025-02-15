__author__ = 'Nick Hirakawa'

from invdx import build_data_structures
from rank import score_BM25
import operator


class QueryProcessor:
    def __init__(self, queries, corpus, dev_candidates=None):
        self.queries = queries
        self.index, self.dlt = build_data_structures(corpus)
        self.dev_candidates = dev_candidates

    def run(self, isCustomFormat=True):
        results = []
        if isCustomFormat:
            for query_id, query in self.queries:
                print query
                results.append(self.run_query(query, query_id), query_id)
        else:
            for query in self.queries:
                print query
                results.append(self.run_query(query, query_id))
        return results

    def run_query(self, query, query_id=None):
        query_result = dict()
        print query_id
        for term in query:
            if term in self.index:
                print 'Term:', term
                doc_dict = self.index[term]  # retrieve index entry
                i = 0
                for docid, freq in doc_dict.items():  # for each document and its word frequency
                    # print 'docid', docid
                    # if we are using fiqa dataset, we need to choose only documents that are a candidate for this query
                    if query_id is not None:
                        shouldConsider = False
                        for question_candidate, isRelevant in self.dev_candidates[query_id]:
                            # print docid, question_candidate
                            if docid == question_candidate:
                                shouldConsider = True
                                break
                    # else we need not care and just consider the word
                    else:
                        shouldConsider = True
                    if shouldConsider:
                        print 'shouldConsider', shouldConsider
                    if shouldConsider:
                        if i % 100 == 0:
                            print 'Doc Id: ', docid
                        i += 1
                        score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
                                           dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length())  # calculate score
                        if docid in query_result:  # this document has already been scored once
                            query_result[docid] += score
                        else:
                            query_result[docid] = score
                print('=======\n')
        return query_result

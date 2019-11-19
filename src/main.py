__author__ = 'Nick Hirakawa'


from parse import *
from query import QueryProcessor
import operator
import pickle

def main():
	pickle_in = open('../pickles/question_candidates.pkl', 'rb')
	question_candidates = pickle.load(pickle_in)

	# qp = QueryParser(filename='../text/queries.txt')
	# cp = CorpusParser(filename='../text/corpus.txt')
	qp = QueryParser(filename='../text/queries-fiqa.txt')
	cp = CorpusParser(filename='../text/corpus-fiqa.txt')
	qp.parse(isCustomFormat=True)
	queries = qp.get_queries()
	cp.parse()
	corpus = cp.get_corpus()
	proc = QueryProcessor(queries, corpus, dev_candidates=question_candidates)
	results = proc.run(isCustomFormat=True)
	# qid = 0

	result_dict = dict()
	for result, qid in results:
		sorted_x = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
		# sorted_x.reverse()
		index = 0
		result_dict[qid] = []
		for i in sorted_x[:100]:
			tmp = (qid, i[0], index, i[1])
			print('{:>1}\tQ0\t{:>6}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
			index += 1
			result_dict[qid].append(i[0])
		# qid += 1


if __name__ == '__main__':
	main()

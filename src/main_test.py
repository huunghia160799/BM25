__author__ = 'Nick Hirakawa'


from parse import *
from query import QueryProcessor
import operator
import pickle


def main():
	# qp = QueryParser(filename='../text/queries.txt')
	# cp = CorpusParser(filename='../text/corpus.txt')
	folder_path = '../text-test/'
	query_path = folder_path + 'queries-fiqa-full.txt'
	corpus_path = folder_path + 'corpus-fiqa.txt'
	qp = QueryParser(filename=query_path)
	cp = CorpusParser(filename=corpus_path)
	qp.parse()
	queries = qp.get_queries()
	cp.parse()
	corpus = cp.get_corpus()
	proc = QueryProcessor(queries, corpus)
	results = proc.run()

	pickle_in = open('../pickles/valid_sample.pkl', 'rb')
	valid_sample = pickle.load(pickle_in)

	candidate_after_bm25 = {}
	total = 0
	contain_positive = 0
	for result, q_id in results:
		sorted_x = sorted(result.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		index = 0
		hasPositive = False
		candidate_after_bm25[q_id] = []
		for i in sorted_x[:100]:
			if (int(q_id), int(i[0])) in valid_sample:
				positive = 1
				hasPositive = True
			else:
				positive = 0
			candidate_after_bm25[q_id].append((i[0], positive))
			tmp = (q_id, i[0], index, i[1], positive)
			print('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25\t{}'.format(*tmp))
			index += 1
		# qid += 1
		if hasPositive:
			contain_positive += 1
		total += 1
	print('Total:', total)
	print('Contains positive:', contain_positive)
	print('Acc', contain_positive / total * 100)

	pickle_out = open('test_candidates_after_bm25.pkl', 'wb')
	pickle.dump(candidate_after_bm25, pickle_out)


if __name__ == '__main__':
	main()

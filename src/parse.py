__author__ = 'Nick Hirakawa'

import re


class CorpusParser:

	def __init__(self, filename):
		self.filename = filename
		self.regex = re.compile('^#\s*\d+')
		self.corpus = dict()

	def parse(self):
		with open(self.filename) as f:
			s = ''.join(f.readlines())
		blobs = s.split('#')[1:]
		for x in blobs:
			text = x.split()
			docid = text.pop(0)
			self.corpus[docid] = text

	def get_corpus(self):
		return self.corpus


class QueryParser:

	def __init__(self, filename):
		self.filename = filename
		self.queries = []

	def parse(self, isCustomFormat=False):
		with open(self.filename) as f:
			lines = ''.join(f.readlines())
		if isCustomFormat:
			self.queries = []
			for x in lines.split('\n')[:-1]:
				line = x.rstrip().split()
				query_id = int(line[0])
				self.queries.append((query_id, line[1:]))
		else:
			self.queries = [x.rstrip().split() for x in lines.split('\n')[:-1]]

	def get_queries(self):
		return self.queries


if __name__ == '__main__':
	qp = QueryParser('text/queries.txt')
	print qp.get_queries()
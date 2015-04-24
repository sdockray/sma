# adapted from http://nbviewer.ipython.org/github/brandomr/document_cluster/blob/master/cluster_analysis.ipynb
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3

class Clusterer(object):
	def __init__(self):
		from nltk.stem.snowball import SnowballStemmer
		self.stemmer = SnowballStemmer("english")

	def tokenize_and_stem(self, text):
	    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
	    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
	    filtered_tokens = []
	    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	    for token in tokens:
	        if re.search('[a-zA-Z]', token):
	            filtered_tokens.append(token)
	    stems = [self.stemmer.stem(t) for t in filtered_tokens]
	    return stems


	def tokenize_only(self, text):
	    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
	    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
	    filtered_tokens = []
	    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	    for token in tokens:
	        if re.search('[a-zA-Z]', token):
	            filtered_tokens.append(token)
	    return filtered_tokens

	def cluster_links(self, links_list):
		titles = []
		links = []
		synopses = []
		# load data
		for k in links_list:
			titles.append(links_list[k].url if hasattr(links_list[k], 'url') else "")
			links.append(links_list[k].url if hasattr(links_list[k], 'url') else "")
			synopses.append(links_list[k].raw_text(include_content=True))

		print(str(len(titles)) + ' titles')
		print(str(len(links)) + ' links')
		print(str(len(synopses)) + ' synopses')

		ranks = []
		for i in range(0,len(titles)):
			ranks.append(i)
		# load nltk's English stopwords as variable called 'stopwords'
		stopwords = nltk.corpus.stopwords.words('english')
		# load nltk's SnowballStemmer as variabled 'stemmer'
		

		totalvocab_stemmed = []
		totalvocab_tokenized = []
		for i in synopses:
			allwords_stemmed = self.tokenize_and_stem(i)
			totalvocab_stemmed.extend(allwords_stemmed)
			allwords_tokenized = self.tokenize_only(i)
			totalvocab_tokenized.extend(allwords_tokenized)

		vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
		
		from sklearn.feature_extraction.text import TfidfVectorizer

		tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
			min_df=0.10, stop_words='english',
			use_idf=True, tokenizer=self.tokenize_and_stem, ngram_range=(1,3))
		tfidf_matrix = tfidf_vectorizer.fit_transform(synopses)
		
		terms = tfidf_vectorizer.get_feature_names()
		print terms

		from sklearn.metrics.pairwise import cosine_similarity
		dist = 1 - cosine_similarity(tfidf_matrix)

		from sklearn.cluster import KMeans

		num_clusters = int(len(titles)/10)
		km = KMeans(n_clusters=num_clusters)
		km.fit(tfidf_matrix)
		clusters = km.labels_.tolist()
		

		films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters }
		frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster'])
		
		ret_links = {}
		for i in range(num_clusters):
			try:
				ret_links[i] = [links_list[l] for l in frame.ix[i]['title'].values.tolist()]
			except:
				pass
		return ret_links

if __name__ == '__main__':
	a = GroupArchive(None, '1463661227181475', filename='archive.pkl')
	titles = []
	links = []
	synopses = []
	# load data
	"""
	for k in a.links:
		titles.append(a.links[k].title if hasattr(a.links[k], 'title') else "")
		links.append(a.links[k].url if hasattr(a.links[k], 'url') else "")
		synopses.append(a.links[k].raw_text(include_content=True))
	"""
	for k in a.posts:
		titles.append(a.posts[k].message[0:80])
		links.append(k)
		synopses.append(a.posts[k].raw_text())

	print(str(len(titles)) + ' titles')
	print(str(len(links)) + ' links')
	print(str(len(synopses)) + ' synopses')

	ranks = []
	for i in range(0,len(titles)):
		ranks.append(i)
	# load nltk's English stopwords as variable called 'stopwords'
	stopwords = nltk.corpus.stopwords.words('english')
	# load nltk's SnowballStemmer as variabled 'stemmer'
	from nltk.stem.snowball import SnowballStemmer
	stemmer = SnowballStemmer("english")

	totalvocab_stemmed = []
	totalvocab_tokenized = []
	for i in synopses:
		allwords_stemmed = tokenize_and_stem(i)
		totalvocab_stemmed.extend(allwords_stemmed)
		allwords_tokenized = tokenize_only(i)
		totalvocab_tokenized.extend(allwords_tokenized)

	vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
	
	from sklearn.feature_extraction.text import TfidfVectorizer

	tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
		min_df=0.10, stop_words='english',
		use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))
	tfidf_matrix = tfidf_vectorizer.fit_transform(synopses)
	
	terms = tfidf_vectorizer.get_feature_names()
	print terms

	from sklearn.metrics.pairwise import cosine_similarity
	dist = 1 - cosine_similarity(tfidf_matrix)

	from sklearn.cluster import KMeans

	num_clusters = int(len(titles)/10)
	km = KMeans(n_clusters=num_clusters)
	km.fit(tfidf_matrix)
	clusters = km.labels_.tolist()
	from pprint import pprint
	
	import pandas as pd
	films = { 'title': titles, 'rank': ranks, 'synopsis': synopses, 'cluster': clusters }
	frame = pd.DataFrame(films, index = [clusters] , columns = ['rank', 'title', 'cluster'])
	
	for i in range(num_clusters):
		print "############ "
		print "Cluster #",i
		for title in frame.ix[i]['title'].values.tolist():
			print title
	#print frame['cluster'].value_counts()
	#print frame['cluster']
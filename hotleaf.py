#!/usr/bin/env python3
import os
import markdown
import sandwich
import datetime
import json

from operator import itemgetter

class Leaf(dict):
	def __format__(self, formatstring):
		return formatstring.format(**self)
	def __missing__(self, key):
		return ''

class Stem(str):
	def __getitem__(self, index):
		return self.split('/')[index]

class InfuseList(list):
	'''a list that can infuse each of its members'''
	def __format__(self, formatstring):
		returnstring = ''
		for i in self:
			try:
				returnstring += formatstring.format(**i)
			except SyntaxError:
				returnstring += formatstring.format(i)
		return returnstring
	def __getitem__(self, search):
		return [i for i in self if search in i]

class Indexer(InfuseList):
	'''a list which gets items by search string, rather than by index'''
	def __getitem__(self, search):
		if search[0] == '#': # tag
			return InfuseList([leaf for leaf in self if search[1:] in leaf['tags']])
		elif search[0] == '/': # path
			return InfuseList([leaf for leaf in self if search[1:] in str(leaf['stem'])])

class Navigator():
	def __init__(self, leaf, direction, pot):
		self.leaf = leaf
		self.direction = direction
		self.pot = Indexer(pot)
	def __getitem__(self, search):
		searched = list(self.pot[search])
		index = searched.index(self.leaf)
		if self.direction == 'prev':
			return searched[index+1]
		elif self.direction == 'next':
			return searched[index-1]



def pick(filename, pot=[]):
	'''pick a leaf up from a file ready for brewing'''
	with open(filename, encoding='utf-8') as f:
		leaf = Leaf(sandwich.load(f.read()))
	
	#Set some sensible defaults
	leaf['stem'] = Stem(os.path.splitext(filename)[0])
	leaf['tip'] = '.html'
	leaf['summary'] = leaf['text'].strip().split('\n')[0]
	leaf['template'] = None

	if not leaf['title']:
		leaf['title'] = leaf['roots'][-1]
	if not leaf['timestamp']:
		leaf['timestamp'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
	
	leaf['text'] = markdown.markdown(leaf['text'])
	leaf['tags'] = InfuseList(leaf['tags'])
	
	if os.path.exists(str(stem) + '.jpg'):
		leaf['image'] = str(stem) + '.jpg'
	elif os.path.exists(str(stem) + '.png'):
		leaf['image'] = str(stem) + '.png'
	else:
		leaf['image'] = "favicon.png"
	
	#Replace those defaults with page-specific text
	with open(leaf['stem']+'.json') as f:
		leaf.update(json.load(f))

	#Add some helpers:
	leaf['prev'] = Navigator(leaf,'prev', pot)
	leaf['next'] = Navigator(leaf,'next', pot)
	leaf['index'] = Indexer(pot)

	return leaf


def scoop(tip='.txt'):
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == tip:
				path = directory[0] + '/' + filename
				path = path.split('./',1)[1]
				print('picking: ' + path)
				pot.append(pick(path))
			
	pot.sort(key=itemgetter('date'), reverse=True)
	return pot
	
def infuse(leaf, plate):
	'''produce output from a given leaf. can optionally use another leaf as a template.'''

	print('infusing: ' + leaf['stem'])
	if leaf['template']:
		plate = pick(leaf['template'])
	
	fused = plate.copy()
	fused.update(leaf)
	fused['text'] = str(fused['text']).format(**fused)
	fused['text'] = str(plate['text']).format(**fused)
	return fused

def pour(leaf):
	'''put an (infused) leaf in the right spot'''
	with open(leaf['stem'] + leaf['tip'], 'w', encoding='utf-8',) as html:
		html.write(leaf['text'])
		

def brew(plate):
	'''brew up a whole pot of tasty hot leaf juice'''
	pot = scoop('.txt')
	for leaf in pot:
		pour(infuse(leaf, plate))



if __name__ == "__main__":
	plate = pick('.template')	#TODO: Have this set from command line parameters.
	brew(plate)

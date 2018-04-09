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
	def navsetup(self, pot):
		'''Adds navigational helper classes'''
		self['prev'] = Navigator(self,'prev', pot)
		self['next'] = Navigator(self,'next', pot)
		self['index'] = Indexer(pot)
		self['if'] = Conditional(self)

class Stem(str):
	def __getitem__(self, index):
		return self.split('/')[index] #Returns list

class InfuseList(list):
	'''a list that can infuse each of its members'''
	def __format__(self, formatstring):
		print(self)
		returnstring = ''
		for i in self:
			returnstring += formatstring.format(i)
		return returnstring #Returns string
#	def __getitem__(self,index):
#		return InfuseList(list.__getitem__(list(self),index))

class Indexer(list):
	'''a list which gets items by search string, rather than by index'''
	def __getitem__(self, search):
		if type(search) is int:
			return list(self)[search] #Returns leaf
		elif search[0] == '#': # tag; returns Indexer
			return Indexer([leaf for leaf in self if search[1:] in leaf['tags']])
		elif search[0] == '/': # path; returns Indexer
			return Indexer([leaf for leaf in self if search[1:] in leaf['stem']])
	def __format__(self, formatstring):
		returnstring = ''
		for i in self:
			returnstring += formatstring.format(**i)
		return returnstring #Returns string

class Navigator():
	def __init__(self, leaf, direction, pot):
		self.leaf = leaf
		self.direction = direction
		self.pot = Indexer(pot)
	def __getitem__(self, search):
		searched = list(self.pot[search])
		poslist = [i['stem'] for i in searched]
		index = poslist.index(self.leaf['stem'])

		if self.direction == 'prev':
			return searched[index+1] #Returns leaf
		elif self.direction == 'next':
			return searched[index-1] #Returns leaf

class Conditional():
	def __init__(self, leaf, state=False):
		self.leaf = leaf
		self.state = state
	def __getitem__(self, search):
		if search[0] == '#': # tag
			if search[1:] in self.leaf['tags']:
				return  Conditional(self.leaf, True)
			else:
				return self
		elif search[0] == '/': # path
			if search[1:] in self.leaf['stem']:
				return  Conditional(self.leaf, True)
			else:
				return self
	def __format__(self, formatstring):
		if self.state:
			return formatstring
		else:
			return ''

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
		leaf['title'] = leaf['stem'][-1]
	if not leaf['timestamp']:
		leaf['timestamp'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
	
	leaf['text'] = markdown.markdown(leaf['text'])
	leaf['tags'] = InfuseList(leaf['tags'])
	
	if os.path.exists(str(leaf['stem']) + '.jpg'):
		leaf['image'] = str(leaf['stem']) + '.jpg'
	elif os.path.exists(str(leaf['stem']) + '.png'):
		leaf['image'] = str(leaf['stem']) + '.png'
	else:
		leaf['image'] = "favicon.png"
	
	#Replace those defaults with page-specific text
	try:
		with open(leaf['stem']+'.json') as f:
			leaf.update(json.load(f))
	except FileNotFoundError:
		pass

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
				pot.append(pick(path,pot))

	pot.sort(key=itemgetter('timestamp'), reverse=True)

	for leaf in pot:
		leaf.navsetup(pot)

	return pot
	
def infuse(leaf, plate):
	'''produce output from a given leaf. can optionally use another leaf as a template.'''

	print('infusing: ' + leaf['stem'])
	if leaf['template']:
		with open(leaf['template'],encoding='utf-8',) as f:
			plate = f.read()
#		plate = pick(leaf['template'])
	
#	fused = plate.copy()
#	fused.update(leaf)
	leaf['text'] = leaf['text'].format(**leaf)
	leaf['text'] = plate.format(**leaf)
	return leaf

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
	with open('.template',encoding='utf-8',) as f: #TODO: Have this set from command line parameters.
		plate = f.read()
	brew(plate)

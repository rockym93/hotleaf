#!/usr/bin/env python3
import os
import markdown

import yaml
from operator import itemgetter

class Chest():
	'''a box to store bulky bits of leaves until they're needed'''
	def __init__(self, filename):
		self.filename = filename
	def __repr__(self):
		return 'Chest("'+self.filename+'")'
	def __str__(self):
		with open(self.filename, encoding='utf-8') as f:
			return markdown.markdown(grade(f.read())[0])
#	def __format__(self):
#		with open(self.filename, encoding='utf-8') as f:
#			return markdown.markdown(grade(f.read())[0])
		
class InfuseList(list):
	'''a list that can format each of its members'''
	def __format__(self, formatstring):
		returnstring = ''
		for i in self:
			returnstring += formatstring.format(str(i))
		return returnstring
		

def grade(raw):
	'''separate raw materials into metadata and text content'''
	broken = raw.split('---', maxsplit=2)
	if broken[0] == '':
		meta = yaml.load(broken[1])
		raw = broken[2]	
	else:
		meta = {}
	return raw, meta

def pick(filename):
	'''pick a leaf up from a file ready for brewing'''
	leaf = {}
	with open(filename, encoding='utf-8') as f:
		raw = f.read()
	
	raw, meta = grade(raw)
		
	#Set some sensible defaults
	leaf['stem'] = os.path.splitext(filename)[0]
	leaf['tip'] = '.html'
	leaf['roots'] = leaf['stem'].split('/')
	leaf['title'] = leaf['roots'][-1]
	leaf['content'] = Chest(filename)
	leaf['summary'] = raw.strip().split('\n')[0]
	leaf['template'] = '.template'
	
	#Replace those defaults with page-specific content
	leaf.update(meta)
	
	for i in leaf:
		if type(leaf[i]) is list:
			leaf[i] = InfuseList(leaf[i])
			
	return leaf


def scoop(tip):
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == tip:
				path = directory[0] + '/' + filename
				path = path.split('./',1)[1]
				print('picking: ' + path)
				pot.append(pick(path))
			
	return pot
	
def strain(pot, keep, reverse=False):
	'''filter and sort the leaves in the pot'''
	strained = []
	for leaf in pot:
		if keep in leaf:
			strained.append(leaf)

	strained.sort(key=itemgetter(keep), reverse=reverse)
	for i in range(len(strained)):
		strained[i]['pos_'+keep] = str(i)
		if i+1 < len(strained):
			strained[i]['next_'+keep] = strained[i+1]['stem']
		if i+1 > 1:
			strained[i]['prev_'+keep] = strained[i-1]['stem']
	return strained
	
def infuse(leaf, plate=None):
	'''produce output from a given leaf. can optionally use another leaf as a template.'''
	print('infusing: ' + leaf['stem'])
	if not plate:
		plate = pick(leaf['template'])
	
	fused = plate.copy()
	fused.update(leaf)
	
	fused['content'] = str(plate['content']).format(**fused)
	return fused

def pour(leaf):
	'''put an (infused) leaf in the right spot'''
	with open(leaf['stem'] + leaf['tip'], 'w', encoding='utf-8',) as html:
		html.write(leaf['content'])
		
	
def steep(menu, pot, plate=None):
	'''prepares special menu items. can optionally use another leaf as a template.'''
	print('steeping: ' + menu['stem'])
	if not plate:
		plate = pick(menu['template'])

	parameters = {
	'show':'title', 
	'length': None, 
	'reverse': False, 
	'header':str() }
	
	parameters.update(**menu['menu'])
	fused = plate.copy()
	fused.update(menu)
	
	content = ''
	for leaf in strain(pot, parameters['show'], parameters['reverse'])[:parameters['length']]:
		currentheader = parameters['header'].format(**leaf)
		try:
			if currentheader != oldheader:
				content += currentheader
		except UnboundLocalError:
			content += currentheader
		oldheader = currentheader
		content += infuse(leaf,fused)['content']
	fused['content'] = content
	
	fused['content'] = str(plate['content']).format(**fused)
	
	return fused

def brew(plate=None):
	'''brew up a whole pot of tasty hot leaf juice'''
	pot = scoop('.txt')
	for menu in scoop('.menu'):
		pour(steep(menu, pot, plate))
	for leaf in pot:
		pour(infuse(leaf, plate))



if __name__ == "__main__":
	brew()

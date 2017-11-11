#!/usr/bin/env python3
import os
import markdown
md = markdown.Markdown()
import yaml
from operator import itemgetter

def pick(filename):
	'''pick a leaf up from a file ready for brewing'''
	leaf = {}
	with open(filename, encoding='utf-8') as f:
		raw = f.read()
	
	#Separate metadata from markdown
	broken = raw.split('---', maxsplit=2)
	if broken[0] == '':
		meta = yaml.load(broken[1])
		raw = broken[2]	
	else:
		meta = {}
	
	#Set some sensible defaults
	leaf['stem'] = os.path.splitext(filename)[0]
	leaf['tip'] = '.html'
	leaf['roots'] = leaf['stem'].split('/')
	leaf['title'] = leaf['roots'][-1]
	leaf['content'] = md.convert(raw)
	leaf['summary'] = next(s for s in md.lines if s)
	leaf['template'] = '.template'
	
	#Replace those defaults with page-specific content
	leaf.update(meta)
	return leaf


def scoop(tip):
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == tip:
				path = directory[0] + '/' + filename
				print(path)
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
	if not plate:
		plate = pick(leaf['template'])
	
	fused = plate.copy()
	fused.update(leaf)
	
	fused['content'] = plate['content'].format(**fused)
	
	return fused

def pour(leaf):
	'''put an (infused) leaf in the right spot'''
	with open(leaf['stem'] + leaf['tip'], 'w', encoding='utf-8',) as html:
		html.write(leaf['content'])
		
	
def steep(menu, pot, plate=None):
	'''prepares special menu items. can optionally use another leaf as a template.'''
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
	fused['content'] = str()
	
	for leaf in strain(pot, parameters['show'], parameters['reverse'])[:parameters['length']]:
		currentheader = parameters['header'].format(**leaf)
		try:
			if currentheader != oldheader:
				fused['content'] += currentheader
		except UnboundLocalError:
			fused['content'] += currentheader
		oldheader = currentheader
		fused['content'] += infuse(leaf,menu)['content']
	
	fused['content'] = plate['content'].format(**fused)
	
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

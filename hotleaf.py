#!/usr/bin/env python3
import os
import markdown
md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
import yaml
from operator import itemgetter

def pick(filename):
	'''pick a leaf up from a file ready for brewing'''
	leaf = {}
	with open(filename, encoding='utf-8') as f:
		raw = f.read()
	
	leaf['stem'] = os.path.splitext(filename)[0]
	leaf['roots'] = leaf['stem'].split('/')
	leaf['title'] = leaf['roots'][-1]
	leaf['content'] = md.convert(raw)
	leaf['summary'] = next(s for s in md.lines if s)
	
	try:
		metadata = next(yaml.load_all(raw))
		if type(metadata) == dict:
			leaf.update(metadata)
	except yaml.scanner.ScannerError:
		pass
	
	return leaf


def scoop(tip):
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == tip:
				path = directory[0] + '/' + filename
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
		if i+1 < len(strained):
			strained[i]['next_'+keep] = strained[i+1]['stem']
		if i+1 > 1:
			strained[i]['prev_'+keep] = strained[i-1]['stem']
	return strained
	
def infuse(leaf, plate):
	'''produce output from a given leaf'''
	fused = plate.copy()
	fused.update(leaf)
	
	fused['content'] = plate['content'].format(**fused)
	
	return fused

def pour(leaf):
	'''put an (infused) leaf in the right spot'''
	with open(leaf['stem'] + '.html', 'w', encoding='utf-8',) as html:
		html.write(leaf['content'])
		
	
def steep(menu, plate, pot):
	'''prepares special menu items'''
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

def brew(plate):
	'''brew up a whole pot of tasty hot leaf juice'''
	pot = scoop('.txt')
	for leaf in pot:
		print(leaf['stem'])
		pour(infuse(leaf, plate))
	for menu in scoop('.menu'):
		print(menu['stem'])
		pour(steep(menu, plate, pot))


if __name__ == "__main__":
	brew(pick('.template'))

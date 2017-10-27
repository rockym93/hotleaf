#!/usr/bin/env python3
import os
import markdown
md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
import yaml
from operator import itemgetter

def pick(filename):
'''pick a leaf up from a file ready for brewing'''
	stem = directory[0] + '/' + os.path.splitext(filename)[0]
	leaf = {}
	with open(stem + '.txt', encoding='utf-8') as f:
		raw = f.read()
	
				
	leaf['stem'] = stem
	leaf['modified'] = os.stat(stem + '.txt').st_mtime
	leaf['roots'] = stem.split('/')
	leaf['title'] = os.path.splitext(filename)[0]
	leaf['content'] = md.convert(raw)
	leaf['summary'] = next(s for s in md.lines if s)
	
	try:
		metadata = next(yaml.load_all(raw))
		if type(metadata) == dict:
			leaf.update(metadata)
	except yaml.scanner.ScannerError:
		pass
	
	return leaf


def scoop():
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == '.txt':
				pot.append(pick(filename))
			
	return pot
	
def strain(pot, keep, reverse=False):
	'''filter and sort the leaves in the pot'''
	strained = []
	for leaf in pot:
		if keep in leaf:
			strained.append(leaf)

	strained.sort(key=itemgetter(keep), reverse=reverse)
	for i in range(len(strained)):
		strained[i]['next_'+keep] = strained[i+1][1]
		strained[i]['prev_'+keep] = strained[i-1][1]
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
	
	search = str(menu['menu'][1])
	if header in menu:
		header = menu['header']
	else:
		header = str()
	reverse = 'r' in menu['menu']

	
	#This lets us use non-int parameters to list the whole lot
	#(Slicing by None gives you the whole list.)
	if type(length) is not int:
		length = None
	else:
		length = int(menu['menu'][0])
		
	
	fused = plate.copy()
	fused.update(menu)
	fused['content'] = str()
	
	for leaf in strain(pot, search, reverse)[:length]:
		currentheader = header.format(leaf)
		if currentheader != oldheader:
			fused['content'] += currentheader
		oldheader = currentheader
		fused['content'] += infuse(leaf,menu)
	
	fused['content'] = plate['content'].format(**fused)
	
	return fused

def brew(plate):
	'''brew up a whole pot of tasty hot leaf juice'''
	pot = scoop()
	for leaf in pot:
		pour(infuse(leaf, plate))
	for menu in strain(pot, 'menu'):
		pour(steep(menu, plate, pot))


	

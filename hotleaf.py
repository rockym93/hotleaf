#!/usr/bin/env python3
import os
import markdown
md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
import yaml

def scoop():
	'''populate the pot with leaves'''
	pot = {}

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == '.txt':
				
				stem = directory[0] + '/' + os.path.splitext(filename)[0]
				leaf = {}
				
				leaf['stem'] = stem
				leaf['modified'] = os.stat(stem + '.txt').st_mtime
				leaf['roots'] = stem.split('/')
				leaf['title'] = os.path.splitext(filename)[0]
				
				with open(stem + '.txt', encoding='utf-8') as f:

					print(stem)
					try:
						metadata = next(yaml.load_all(f))
						if type(metadata) == dict:
							leaf.update(metadata)
					except yaml.scanner.ScannerError:
						pass
						
					f.seek(0)
					leaf['content'] = md.convert(f.read())
					leaf['summary'] = next(s for s in md.lines if s)


					
				pot[stem] = leaf
			
	return pot
	
def strain(pot, keep, reverse=False):
	'''filter and sort the leaves in the pot'''
	strained = []
	for stem in pot:
		if keep in pot[stem]:
			strained.append((pot[stem][keep], stem))

	strained.sort(reverse=reverse)
	for i in range(len(strained)):
		leaf = pot[strained[i][1]]
		leaf['next_'+keep] = strained[i+1][1]
		leaf['prev_'+keep] = strained[i-1][1]
	return strained
	
def infuse(leaf, tleaf):
	'''produce output from a given leaf'''
	fused = tleaf.copy()
	fused.update(leaf)
	
	fused['content'] = tleaf['content'].format(**fused)
	
	return fused['content']

def pour(pot):
	'''infuse all leaves in the pot and distribute the output'''
	
def steep(leaf, tleaf, pot):
	'''prepares special leaves'''
	
	length = int(leaf['index'][0])
	search = str(leaf['index'][1])
	header = leaf['header']
	
	#This lets us use non-int parameters to list the whole lot
	#(Slicing by None gives you the whole list.)
	if type(length) is not int:
		length = None
	
	fused = tleaf.copy()
	fused.update(leaf)
	fused['content'] = str()
	
	for stem in strain(pot, search)[:length]:
		currentheader = header.format(**pot[stem[1]]
		if currentheader != oldheader:
			fused['content'] += currentheader
		oldheader = currentheader
		fused['content'] += infuse(pot[stem[1]],leaf)
	
	fused['content'] = tleaf['content'].format(**fused)
	
	return fused['content']
	
	
	
def brew():
	'''brew up a whole pot of tasty hot leaf juice'''


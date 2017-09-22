#!/usr/bin/env python3
import os
import markdown
md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
import dateutil.parser as date


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
					leaf['content'] = md.convert(f.read())
					leaf['summary'] = next(s for s in md.lines if s)
					leaf.update(md.Meta)
					leaf['date'] = date.parse(leaf['date'])

					
				pot[stem] = leaf
			
	return pot
	
def strain(pot, keep):
	'''filter and sort the leaves in the pot'''
	strained = []
	for stem in pot:
		if keep in pot[stem]:
			strained.append((pot[stem][keep], stem))

	strained.sort()
	return strained
	
def infuse(leaf, tleaf):
	'''produce output from a given leaf'''
	fused = tleaf.copy()
	fused.update(leaf)
	
	fused['content'] = tleaf['content'].format(leaf)
	
	return fused
	
	
			

def pour(pot):
	'''infuse all leaves in the pot and distribute the output'''
	
def steep():
	'''prepares, infuses and distributes special leaves'''
	
def brew():
	'''brew up a whole pot of tasty hot leaf juice'''


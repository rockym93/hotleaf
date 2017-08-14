#!/usr/bin/env python3
import os
import yaml



def scoop():
	'''populate the pot with leaves'''
	pot = {}
	links = next(os.walk('.'))[1]
	links.sort()

	for l in list(links):
		if l[0] == '.':
			links.remove(l)

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == '.txt':
				
				stem = directory[0] + '/' + os.path.splitext(filename)[0]
				leaf = {}
				
				leaf['modified'] = os.stat(stem + '.txt').st_mtime
				leaf['links'] = links
				leaf['parent'] = stem.split('/')[0]
				leaf['title'] = filename
				
				with open(stem + '.txt', encoding='utf-8') as f:
					print(stem)
					try:
						metadata = next(yaml.load_all(f))
						if type(metadata) == dict:
							leaf.update(metadata)
					except yaml.scanner.ScannerError:
						pass

				pot[stem] = leaf
			
	return pot
	
def strain():
	'''sort the leaves in the pot'''
	
def infuse(leaf):
	'''produce output from a given leaf'''

def pour():
	'''infuse all leaves in the pot and distribute the output'''
	
def steep():
	'''prepares, infuses and distributes special leaves'''
	
def brew():
	'''brew up a whole pot of tasty hot leaf juice'''
	


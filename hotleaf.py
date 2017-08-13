#!/usr/bin/env python3
import os
import yaml

pot = {}

def scoop():
	'''populate the pot with leaves'''
	
	links = next(os.walk('.'))[1]
	links.sort()

	for l in list(links):
		if l[0] == '.':
			links.remove(l)

	for directory in os.walk('.'):
		for filename in directory[2]:
			if filename.split('.')[-1] == 'txt':
				
				stem = directory[0] + '/' + filename.rstrip('.txt')
				leaf = {}
				
				leaf['modified'] = os.stat(filename).st_mtime
				leaf['links'] = links
				leaf['parent'] = stem.split('/')[0]
				leaf['title'] = filename
				
				with open(filename, encoding='utf-8') as f:
					
					try:
						leaf.update(next(yaml.load_all(f)))
					except ScannerError:
						pass

				pot[stem] = leaf
	
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
	


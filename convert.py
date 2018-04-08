#!/usr/bin/env python3

import os
import yaml
import sandwich

def grade(raw):
	'''separate raw materials into metadata and text content'''
	broken = raw.split('---', maxsplit=2)
	if broken[0] == '':
		meta = yaml.load(broken[1])
		raw = broken[2]	
	else:
		meta = {}
	return raw, meta

def scoop():
	'''populate the pot with leaves'''
	pot = []

	for directory in os.walk('.'):
		for filename in directory[2]:
			if os.path.splitext(filename)[1] == '.txt':
				path = directory[0] + '/' + filename
				path = path.split('./',1)[1]
				print('picking: ' + path)
				with open(path, encoding='utf-8') as f:
					raw, meta = grade(f.read())
				leaf = {}
				leaf["stem"] = path
				leaf["text"] = raw.strip()
				if 'image' not in meta.keys():
					leaf['image'] = None
				try:
					leaf["title"] = meta["title"]
				except KeyError:
					leaf["title"] = ''
				try:
					leaf["summary"] = meta["summary"]
				except KeyError:
					leaf["summary"] = ''
				try:
					leaf["image"] = meta["image"]
				except KeyError:
					leaf["image"] = None
				try:
					leaf["timestamp"] = meta["blog"] #whatever the newest timestamp is - it could be under any key... >_<
				except KeyError:
					leaf["timestamp"] = None
				try:
					leaf["tags"] = [meta["tag"]] #and then we gotta add more >_<
				except KeyError:
					leaf["tags"] = []
				pot.append(leaf)
	return pot

def pour(leaf):
	'''put a reformatted leaf in the right spot'''
	with open(leaf['stem'], 'w', encoding='utf-8',) as txt:
		txt.write(sandwich.dump(leaf))

if __name__ == "__main__":
	pot = scoop()
	for leaf in pot:
		pour(leaf)




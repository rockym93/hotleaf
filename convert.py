#!/usr/bin/env python3

import os
import yaml
import sandwich
import json

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
#				print('picking: ' + path)
				with open(path, encoding='utf-8') as f:
					raw, meta = grade(f.read())
				leaf = {} #this stuff goes in the text file
				leaf["sidecar"] = {} #this stuff goes in the sidecar file
				leaf["stem"] = path.rsplit('.', maxsplit=1)[0]
				raw = raw.strip()
				if path.split('/')[0] == 'blog':
					if path.split('/')[1] < '2013':
						if '\n  \n' in raw:
							raw = raw.replace('\n  \n','\n\n')
						raw = raw.replace('\n\n','<BR>').replace('\n',' ').replace('<BR>','\n\n')

				leaf["text"] = raw 
				if 'image' not in meta.keys():
					leaf['image'] = None
				try:
					leaf["title"] = meta["title"]
				except KeyError:
					leaf["title"] = ''
				try:
					leaf["sidecar"]["summary"] = meta["summary"]
				except KeyError:
					pass
				try:
					if meta['image'].rsplit('.', maxsplit=1)[0] != leaf['stem']: #if it's not the same as the text file name
						leaf["sidecar"]["image"] = meta["image"]
					if leaf["sidecar"]["image"] == "favicon.png":
						del leaf["sidecar"]["image"] 
				except KeyError:
					pass
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
	with open(leaf['stem'] + '.new', 'w', encoding='utf-8',) as txt:
		txt.write(sandwich.dump(leaf))
	if leaf["sidecar"]:
		with open(leaf['stem'] + '.json', 'w', encoding='utf-8',) as txt:
			txt.write(json.dumps(leaf["sidecar"]))

	

if __name__ == "__main__":
	pot = scoop()
	for leaf in pot:
		pour(leaf)




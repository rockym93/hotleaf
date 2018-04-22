#!/usr/bin/env python3
import json
import dateutil.parser
import datetime



def load(text):
	'''processes a text file into a sandwich object with metadata'''
	sandwich = {}
	lines = text.strip().splitlines()
	headline = lines[0].strip()
	del lines[0]

	if lines[-1].strip()[0] in '#<': #if tags or timestamp present on last line
		tagline = lines[-1] #set the tagline
		del lines[-1] #remove it from the text
	text = '\n'.join(lines)

	if tagline[0] is '<': #if a date is present
		timestamp = tagline.split('>')[0].strip(' <>')
		try:
			sandwich['timestamp'] = dateutil.parser.parse(timestamp)
		except ValueError:
			print("Invalid date")
			sandwich['timestamp'] = None
	else:
		sandwich['timestamp'] = None
	sandwich['title'] = headline.strip("# ")
	sandwich['tags'] = [tag.strip() for tag in tagline.split("#")[1:]] #everything from the first tag on
	sandwich['text'] = text


	

#	# These could be used as defaults - if we knew what the filename was, which we don't.
#	sandwich['_title'] = os.path.basename(filename)
#	sandwich['_timestamp'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))

	return sandwich

def dump(sandwich):
	'''processes a sandwich object into a text file'''
	text = ''
	try: 
		tagline = ['<'+sandwich['timestamp'].isoformat()+'>'] + sandwich['tags']
	except AttributeError:
		tagline = [''] + sandwich['tags']
	

	if sandwich['title']:
		text += '# ' + sandwich['title']
	text += '\n' + sandwich['text']
	text += '\n\n' + ' #'.join(tagline)

	return text

def markstrip(text):
	image = None
	if '](' in text:
		while '](' in text:
			p = text.split('](', maxsplit=1)
			q = p[1].split(')', maxsplit=1)
			if '![' in p[0]:
				image = q[0]
			p.append(q[1])
			del p[1]
			text = ''.join(p)
		text = text.replace('![','')
		text = text.replace('[','')
	return text,image
			

# if __name__ == "__main__":
# 	import argparse
# 	parser = argparse.ArgumentParser(description="Process sandwich files")
# 	parser.add_argument('-j','--to-json' dest='mode' help='convert json input to sandwich output')
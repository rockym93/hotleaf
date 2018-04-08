#!/usr/bin/env python3
import json
import dateutil.parser
import datetime



def load(text):
	'''processes a text file into a sandwich object with metadata'''
	sandwich = {}
	headline = text.splitlines()[0]
	tagline = text.splitlines()[-1]
	text = '\n'.join(text.splitlines()[1:-1])

	try: 
		sandwich['timestamp'] = dateutil.parser.parse(tagline.split("#")[0])
	except ValueError:
		sandwich['timestamp'] = None
	sandwich['title'] = headline.strip("# ")
	sandwich['tags'] = [tag.strip() for tag in tagline.split("#")[1:]]
	sandwich['text'] = text

	try:
		finaltag = tagline.split('!')[1]
		try:
			sandwich['tags'].append(sandwich['tags'].pop().split(' !')[0].strip()) #remove the meta from final tag
		except IndexError:
			pass
		sandwich['summary'] = finaltag.split('](')[0].strip('[')
		if not sandwich['summary']:
			sandwich['summary'] = text.splitlines()[0]
		sandwich['image'] = finaltag.split('](')[1].strip(')')
		if not sandwich['image']:
			sandwich['image'] = None
	except IndexError:
		sandwich['summary'] = text.splitlines()[0] #first line of text
		sandwich['image'] = None
	

#	# These could be used as defaults - if we knew what the filename was, which we don't.
#	sandwich['_title'] = os.path.basename(filename)
#	sandwich['_timestamp'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))

	return sandwich

def dump(sandwich):
	'''processes a sandwich object into a text file'''
	text = ''
	try: 
		tagline = [sandwich['timestamp'].isoformat()] + sandwich['tags']
	except AttributeError:
		tagline = [''] + sandwich['tags']
	

	if sandwich['title']:
		text += '# ' + sandwich['title']
	text += '\n' + sandwich['text']
	text += '\n' + ' #'.join(tagline)

	try:
		if sandwich['summary'] == sandwich['text'].splitlines()[0]:
			sandwich['summary'] = ''
	except KeyError:
		sandwich['summary'] = ''
	
	try:
		if not sandwich['image']:
			sandwich['image'] = ''
	except KeyError:
		sandwich['image'] = ''

	if sandwich['image'] or sandwich['summary']:
		text += ' ![{summary}]({image})'.format(**sandwich)
	
	return text


# if __name__ == "__main__":
# 	import argparse
# 	parser = argparse.ArgumentParser(description="Process sandwich files")
# 	parser.add_argument('-j','--to-json' dest='mode' help='convert json input to sandwich output')
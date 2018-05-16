---
title: Hot Leaf Juice
summary: A really basic static site generator.
image: /code/hotleaf.png
---
<https://github.com/rockym93/hotleaf>


What is Hot Leaf Juice?
-----------------------

Hot Leaf Juice is a script that turns [markdown][1] formatted text files into html. There are [literally hundreds][2] of other bits of software that do this, but Hot Leaf Juice is different in a couple of ways.

First, it's really basic. Basic enough for me to hack on to work *exactly* how I want it to. It's written to maintain my own site at <http://rockym93.net>. There may be parts of the code that are hard-coded specifically for my site, but that's fine - hopefully, the code is basic enough that you can change those.

Second, and somewhat uniquely, Hot Leaf Juice does in-place formatting of files. I like being able to change the file extension to see the source of a page. Hot Leaf Juice doesn't insist on using its own file hierarchy, it just scans down through whatever directory it's in, looking for text files, and plunks down html files with the same name next to them. 

Third, Hot Leaf Juice is an experiment in coding whimsy. Working with the code, and with the script, is themed around making a pot of tea. This is mostly so that I can make jokes about my site being 'powered by tea' in my footer, but partly also as a way of forcing myself to plan my code ahead a little more. If you don't like it, feel free to move right along.

Setup
-----
1. Drop hotleaf.py into the root directory of your site.
2. Set up your template in a file called .template, also in the root directory (see Formatting, below).
3. Run hotleaf.py whenever something in your text files changes.


Usage
-----
  python ./hotleaf.py

Formatting
----------

*(File formatting has changed since past versions! There's a convert script in here, but you'll need to modify it a bit.)*

Hot Leaf Juice turns text files into html files with the same name. Those text files contain your content, formatted as [Markdown](https://daringfireball.net/projects/markdown/syntax).

Text files are written as a hashtag sandwich. 

The first line is your title, which starts with a # symbol as if it were a Markdown title.

The last line is a series of actual hashtags, which are your file tags. It can also include a date, wrapped in <angle brackets>. So your tagline might look like this:

  <2018-01-21> #blog #news #tea #sandwiches

A title is compulsory, but the tagline is optional.

Templates
---------
Templates are the files that your content gets pasted into. Like pages, they start with a metadata section. This lets you set some default values.

In the main part of your template, you can reference any metadata you've set in the document, any metadata set in the template, and any metadata that Hot Leaf Juice sets automatically. Data from the document overwrites automatic data, and both overwrite data from the template.

Metadata goes between curly braces. 

  {{title}}

If you need to use an actual curly brace character, you can double them up, like so:

  {{{{actual curly brackets}}}}

<!-- If you're reading this as a text file, you'll notice that these are already doubled: that's so that this very file can be processed by Hot Leaf Juice. -->

There is some more complex stuff you can do with these, like formatting date data in particular ways, or getting a specific item in a list. I'm actually using the standard Python string formatting library to do this, and there's some excellent documentation [here](https://pyformat.info/).

You can include tags like this in both your content and your template.



### Automatic tags ###

Hot Leaf Juice fills some tags automatically. 

{{stem}} contains the source file's path, without the extension. You can reference individual folders with square brackets, like this:
  {{stem[0]}} 
{{title}} is automatically set to the file name, with no extension.
{{text}} is filled with your formatted html. Use this to actually include your content in your template.
{{summary}} is set to the first line of your text.
{{image}} is set to the image file with the same name as your text file.
{{timestamp}} is set to the file modified date, unless you've set one in the tagline.

If you need extra stuff, Hot Leaf Juice also reads a .json file with the same title as your text file, and those keys/values are accessible through {{brackets}} as well.

### Magic tags ###

Hot Leaf Juice can also do some more complex stuff with tags.

{{tags:(some formatting)}} will list your tags, and fill out the formatting string for each one. {{{{}}}} will be replaced with the tag. For example:
  {{tags:tagged with {{{{}}}} }}

{{index[#tag]:(some formatting)}} will list everything under a particular tag, and fill out the formatting string for each one. The tags in the formatting string are the same as the tags in your text, but with two brackets instead of one.
  {{index[#blog]:<a href="{{{{stem}}}}.html">{{{{title}}}}</a>}}

{{prev[#tag]}} and {{next[tag]}} return the previous and next posts, chronologically, in a particular tag.

{{if[#tag]:(some text)}} will show some text only if a post is tagged with a particular tag. Useful for turning page elements on and off in your template.

These give you just enough indexing to do a simple blog, with previous and next links, tags, and an archive/feed/front page. They can interact with each other in some weird ways, so I'd recommend against trying to nest them.


Hacking
-------

Hot Leaf Juice should be pretty easy to repurpose. You can import it into your own python script with:

  import hotleaf

It's broken up into functions, and they're all pretty self explanatory - if slightly whimsically named. 

The stuff for interpreting the file format is under sandwich.py - it implements a standard load() and dump() interface, to help you get your data in and out of Hot Leaf Juice safely.

If you have any questions, or if you end up using Hot Leaf Juice for your own site, feel free to shoot me an email at hotleaf@rockym93.net.

License
-------

<https://opensource.org/licenses/MIT>

Copyright 2017 Rockwell McGellin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[1]: https://daringfireball.net/projects/markdown/
[2]: https://www.staticgen.com/

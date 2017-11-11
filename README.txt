Hot Leaf Juice
==============
A really basic static site generator.

<https://www.rockym93.net/code/hotleaf/> | <rockwell@mcgell.in>


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
Hot Leaf Juice turns text files into html files with the same name. Those text files contain your content, formatted as [Markdown](https://daringfireball.net/projects/markdown/syntax).

At the start of each file, you can put some YAML. This will let you set different bits of metadata for that page. These might be tags, or dates, or navigational elements, which need to be different on every page, and that you don't want to hand-write in.

Start this section with three dashes (---), on the very first line of your file. YAML can be a bit complex, but the gist of it is that you have names and values, separated by a colon:

  ---
  title: Example Page
  date: 2017-10-31
  ---
  
Once you're done setting your data, end the YAML document with three dashes (---). Then start your actual document.

In the main part of your document, you can reference any metadata you've set in the document, any metadata set in the template, and any metadata that Hot Leaf Juice sets automatically. Data from the document overwrites automatic data, and both overwrite data from the template.

Metadata goes between curly braces. If you had a variable called 'tag', you could reference it like this:

  {{tag}}

If you need to use an actual curly brace character, you can double them up, like so:

  {{{{actual curly brackets}}}}

<!-- If you're reading this as a text file, you'll notice that these are already doubled: that's so that this very file can be processed by Hot Leaf Juice. -->

There is some more complex stuff you can do with these, like formatting date data in particular ways, or getting a specific item in a list. I'm actually using the standard Python string formatting library to do this, and there's some excellent documentation [here](https://pyformat.info/).

You can include tags like this in both your content and your template.

### Automatic tags ###

Hot Leaf Juice fills some tags automatically. 

{{stem}} contains the source file's path, without the extension.
{{roots}} contains the source file's path, split up into subfolders. You can reference individual components with square brackets, like this:
  {{roots[0]}} 
{{title}} is automatically set to the file name, with no extension (or {{roots[-1]}})
{{content}} is filled with your formatted html. Use this to actually include your content in your template.
{{summary}} is set to the first line of your text.

You can override these in the file's metadata section. Note that changing 'stem' will cause your html file to end up at the new location rather than right next to your text files.

### Menus ###

There's one more special metadata structure, the menu. This is only active in files that end in .menu, which get processed differently.

Menus can be used to make a site map, or a tag list, or an archive, or a blog front page. They work by using their text content as the template for several pages which have a particular bit of metadata set, and then using that as the content for the page. Essentially, they let you stack a set of pages together.

You can tell it which pages, how many, and in what order using metadata tags:
  menu:
    show: blog
    length: 5
    header: {date:%Y}
    reverse: True

show: tells Hot Leaf Juice which bit of metadata it's looking for.
length: controls how many of those we show.
header: is a bit of text that's inserted every time it changes - it can include metadata tags.
reverse: reverses the order of the pages. Pages are sorted before being shown.

The indent is important! Your menu won't work without it.

You'll also need to set what you want shown for each page. That gets set in the content area of the menu file.

There are some examples of menus in tests/index.

Hacking
-------

Hot Leaf Juice should be pretty easy to repurpose. You can import it into your own python script with:

  import hotleaf

It's broken up into functions, and they're all pretty self explanatory - if slightly whimsically named. 

If you have any questions, feel free to shoot me an email at hotleaf@rockym93.net.

License
-------

<https://opensource.org/licenses/MIT>

Copyright 2017 Rockwell McGellin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

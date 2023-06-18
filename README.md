A utility to convert AO3 HTML-downloaded works into docx format, for export to
Google Docs.

This was originally developed for use on my personal account, so it definitely
has bugs and mess, and has not been verified on all cases. I'm putting this up
in case it comes in handy to anyone else, especially since one of the things it
features is a class for parsing AO3 works, particularly for metadata.

I'm (probably) not actively working on this -- pull requests are welcome, but
you're better off forking.

# Installation

This requires python3.

Clone the repo, and then install requirements with `pip -r requirements.txt`

# Usage

python3 docx_converter.py [input directory] [output directory]

Output directory must already exist.

# Known Issues

* Docx exporter doesn't correctly handle chaptered works.
* `Work.get_short_fandom_name()` will not work with all fandom names (names
  containing parentheses as part of the fandom name, and probably crossovers too.)
* Embedded images and workskins almost certainly won't work in the conversion.

 

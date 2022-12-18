SRC ?= ./
TITLE ?= Reveal JS Wrapper

all: head body tail 

head:
	cat $(SRC)/dist/head.html > header.html
	echo "<TITLE>$(TITLE)</TITLE><style>" >> header.html
	cat $(SRC)/dist/reset.css >> header.html
	cat $(SRC)/dist/reveal.css >> header.html
	cat $(SRC)/dist/theme/black.css >> header.html
	cat $(SRC)/plugin/highlight/monokai.css >> header.html
	echo "</style>" >> header.html
	echo '</head><body><div class="reveal">\n<div class="slides">\n' >> header.html
body:
	echo "<section>slide1</section>" > slide.html
	echo "<section>slide3</section>" >> slide.html

tail:
	echo "</div></div><script>" > footer.html
	cat $(SRC)/dist/reveal.js >> footer.html
	cat $(SRC)/plugin/notes/notes.js >> footer.html
	cat $(SRC)/plugin/markdown/markdown.js >> footer.html
	cat $(SRC)/plugin/highlight/highlight.js >> footer.html
	echo "</script><script> Reveal.initialize({ hash: true, plugins:" >> footer.html
	echo "[ RevealMarkdown, RevealHighlight, RevealNotes ]});</script>" >> footer.html
	echo "</body></html>" >> footer.html

html: 
	cat header.html > slides.html
	cat slide.html >> slides.html
	cat footer.html >> slides.html


.PHONY: clean

clean:
	rm -f slides.html header.html footer.html slide.html

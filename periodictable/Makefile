all: periodictable-a4.pdf periodictable-letter.pdf

periodictable-a4.tex: periodictable.py
	./periodictable.py --a4 periodictable-a4.tex

periodictable-letter.tex: periodictable.py
	./periodictable.py --letter periodictable-letter.tex

periodictable-a4.pdf: periodictable-a4.tex
	pdflatex periodictable-a4.tex

periodictable-letter.pdf: periodictable-letter.tex
	pdflatex periodictable-letter.tex

clean:
	rm -f periodictable-a4.out
	rm -f periodictable-a4.log
	rm -f periodictable-a4.aux
	rm -f periodictable-letter.out
	rm -f periodictable-letter.log
	rm -f periodictable-letter.aux

distclean: clean
	rm -f periodictable-a4.tex
	rm -f periodictable-a4.pdf
	rm -f periodictable-letter.tex
	rm -f periodictable-letter.pdf

.PHONY: all clean distclean

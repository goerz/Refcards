all: ascii_a4.pdf ascii_letter.pdf

ascii_a4.pdf: ascii.tex
	#xelatex -output-driver="xdvipdfmx -q -E -p a4 -l" $<
	pdflatex $<
	mv ascii.pdf $@

ascii_letter.pdf: ascii_letter.tex
	#xelatex -papersize=letter $<
	pdflatex $<

ascii_letter.tex: ascii.tex ascii_letter.patch
	cp $< $@
	patch $@ ascii_letter.patch

clean:
	rm -f *.out
	rm -f *.log
	rm -f *.aux

distclean: clean
	rm -f ascii_letter.tex
	rm -f *.pdf

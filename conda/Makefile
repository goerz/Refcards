all: conda-a4.pdf conda-letter.pdf

conda-a4.pdf: conda-a4.tex conda-cheatsheet.pdf
	pdflatex conda-a4.tex

conda-letter.pdf: conda-letter.tex conda-cheatsheet.pdf
	pdflatex conda-letter.tex

conda-cheatsheet.pdf:
	wget https://conda.io/docs/_downloads/conda-cheatsheet.pdf

clean:
	rm -f conda-a4.out
	rm -f conda-a4.log
	rm -f conda-a4.aux
	rm -f conda-letter.out
	rm -f conda-letter.log
	rm -f conda-letter.aux
	rm -f conda-cheatsheet.pdf

distclean: clean
	rm -f conda-a4.pdf
	rm -f conda-letter.pdf

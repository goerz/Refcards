ALL = \
./latex/ascii.pdf \
./latex/fortran_refcard.pdf \
./latex/powers_of_ten.pdf \
./latex/sympy_refcard.pdf \
./latex/conda-a4.pdf \
./latex/conda-letter.pdf \
./plaintex/linuxqrc.pdf \
./plaintex/my_vim_mappings.pdf \
./plaintex/vimlatexqrc.pdf \
./plaintex/vimqrc.pdf \

all: $(ALL)

./latex/ascii.pdf: ./latex/ascii.tex
	(cd latex && pdflatex ascii.tex)

./latex/fortran_refcard.pdf: ./latex/fortran_refcard.tex
	(cd latex && pdflatex fortran_refcard.tex)

#./latex/fortran_refcard_a4.pdf

#./latex/fortran_refcard_letter.pdf

./latex/powers_of_ten.pdf: ./latex/powers_of_ten.tex
	(cd latex && pdflatex powers_of_ten.tex)

./latex/sympy_refcard.pdf: ./latex/sympy_refcard.tex
	(cd latex && pdflatex sympy_refcard.tex)

./plaintex/linuxqrc.pdf: ./plaintex/linuxqrc.tex
	(cd plaintex && pdftex linuxqrc.tex)

./plaintex/my_vim_mappings.pdf: ./plaintex/my_vim_mappings.tex
	(cd plaintex && pdftex my_vim_mappings.tex)

./plaintex/vimlatexqrc.pdf: ./plaintex/vimlatexqrc.tex
	(cd plaintex && pdftex vimlatexqrc.tex)

./plaintex/vimqrc.pdf: ./plaintex/vimqrc.tex
	(cd plaintex && pdftex vimqrc.tex)

./latex/conda.pdf:
	wget -O ./latex/conda.pdf http://conda.pydata.org/docs/_downloads/conda-cheatsheet.pdf

./latex/conda-a4.pdf: ./latex/conda.pdf ./latex/conda-a4.tex
	(cd latex && pdflatex conda-a4.tex)

./latex/conda-letter.pdf: ./latex/conda.pdf ./latex/conda-a4.tex
	@sed <./latex/conda-a4.tex -e s/a4paper/letterpaper/g -e s/194mm/200mm/g > ./latex/conda-letter.tex
	(cd latex && pdflatex conda-letter.tex)
	@rm -f ./latex/conda-letter.tex

clean:
	@rm -f ./plaintex/*.aux
	@rm -f ./plaintex/*.glo
	@rm -f ./plaintex/*.idx
	@rm -f ./plaintex/*.log
	@rm -f ./plaintex/*.toc
	@rm -f ./plaintex/*.ist
	@rm -f ./plaintex/*.acn
	@rm -f ./plaintex/*.acr
	@rm -f ./plaintex/*.alg
	@rm -f ./plaintex/*.bbl
	@rm -f ./plaintex/*.blg
	@rm -f ./plaintex/*.dvi
	@rm -f ./plaintex/*.glg
	@rm -f ./plaintex/*.gls
	@rm -f ./plaintex/*.ilg
	@rm -f ./plaintex/*.ind
	@rm -f ./plaintex/*.lof
	@rm -f ./plaintex/*.lot
	@rm -f ./plaintex/*.maf
	@rm -f ./plaintex/*.mtc
	@rm -f ./plaintex/*.mtc1
	@rm -f ./plaintex/*.out
	@rm -f ./plaintex/*.synctex.gz
	@rm -f ./latex/*.aux
	@rm -f ./latex/*.glo
	@rm -f ./latex/*.idx
	@rm -f ./latex/*.log
	@rm -f ./latex/*.toc
	@rm -f ./latex/*.ist
	@rm -f ./latex/*.acn
	@rm -f ./latex/*.acr
	@rm -f ./latex/*.alg
	@rm -f ./latex/*.bbl
	@rm -f ./latex/*.blg
	@rm -f ./latex/*.dvi
	@rm -f ./latex/*.glg
	@rm -f ./latex/*.gls
	@rm -f ./latex/*.ilg
	@rm -f ./latex/*.ind
	@rm -f ./latex/*.lof
	@rm -f ./latex/*.lot
	@rm -f ./latex/*.maf
	@rm -f ./latex/*.mtc
	@rm -f ./latex/*.mtc1
	@rm -f ./latex/*.out
	@rm -f ./latex/*.synctex.gz

distclean: clean
	@rm -f $(ALL)
	@rm -f ./latex/conda.pdf


.PHONY: all clean distclean

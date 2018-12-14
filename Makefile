ALL = asciitable conda fortran my_vim_mappings powers_of_ten vim vimlatex periodictable

all:
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder; done

clean:
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder clean; done

distclean: clean
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder distclean; done
	rm -rf collect

collect: all
	mkdir -p collect
	cp asciitable/ascii_a4.pdf $@/
	cp asciitable/ascii_letter.pdf $@/
	cp fortran/fortran_refcard_a4.pdf $@/
	cp fortran/fortran_refcard_letter.pdf $@/
	cp my_vim_mappings/my_vim_mappings.pdf $@/
	cp periodictable/periodictable-a4.pdf $@/
	cp periodictable/periodictable-letter.pdf $@/
	cp perl/perl_refcard.odt $@/
	cp perl/perl_refcard.pdf $@/
	cp python24/python_refcard.odt $@/
	cp python24/python_refcard.pdf $@/
	cp vim/vimqrc.pdf $@/
	cp vimlatex/vimlatexqrc.pdf $@/
	cp powers_of_ten//powers_of_ten.pdf $@/
	rm -f $@/*.png
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten ascii_a4.pdf[0] ascii.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten ascii_a4.pdf[0] ascii_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten fortran_refcard_a4.pdf[0] fortran_refcard_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten fortran_refcard_a4.pdf[1] fortran_refcard_1.png)
	(cd $@ && montage fortran_refcard_*.png -tile 1x2 -geometry +0+0 fortran_refcard.png && rm fortran_refcard_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten fortran_refcard_a4.pdf[0] fortran_refcard_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten my_vim_mappings.pdf[0] my_vim_mappings_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten my_vim_mappings.pdf[1] my_vim_mappings_1.png)
	(cd $@ && montage my_vim_mappings_*.png -tile 1x2 -geometry +0+0 my_vim_mappings.png && rm my_vim_mappings_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten my_vim_mappings.pdf[0] my_vim_mappings_thumbnail.png)
	(cd $@ && convert -density 200 -background white -flatten periodictable-a4.pdf[0] periodictable.png)
	(cd $@ && convert -density 20 -background white -flatten periodictable-a4.pdf[0] periodictable_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten perl_refcard.pdf[0] perl_refcard_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten perl_refcard.pdf[1] perl_refcard_1.png)
	(cd $@ && montage perl_refcard_*.png -tile 1x2 -geometry +0+0 perl_refcard.png && rm perl_refcard_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten perl_refcard.pdf[0] perl_refcard_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten python_refcard.pdf[0] python_refcard_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten python_refcard.pdf[1] python_refcard_1.png)
	(cd $@ && montage python_refcard_*.png -tile 1x2 -geometry +0+0 python_refcard.png && rm python_refcard_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten python_refcard.pdf[0] python_refcard_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten vimqrc.pdf[0] vimqrc_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten vimqrc.pdf[1] vimqrc_1.png)
	(cd $@ && montage vimqrc_*.png -tile 1x2 -geometry +0+0 vimqrc.png && rm vimqrc_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten vimqrc.pdf[0] vimqrc_thumbnail.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten vimlatexqrc.pdf[0] vimlatexqrc_0.png)
	(cd $@ && convert -density 150 -background white -colorspace Gray -flatten vimlatexqrc.pdf[1] vimlatexqrc_1.png)
	(cd $@ && montage vimlatexqrc_*.png -tile 1x2 -geometry +0+0 vimlatexqrc.png && rm vimlatexqrc_*.png)
	(cd $@ && convert -density 20 -background white -colorspace Gray -flatten vimlatexqrc.pdf[0] vimlatexqrc_thumbnail.png)

.PHONY: all clean distclean

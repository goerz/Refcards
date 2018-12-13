ALL = asciitable conda fortran my_vim_mappings powers_of_ten vim vimlatex periodictable

all:
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder; done

clean:
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder clean; done

distclean: clean
	@for folder in $(ALL); do echo "\n\n-" $$folder; make -C $$folder distclean; done


.PHONY: all clean distclean

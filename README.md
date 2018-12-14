# Refcards

This repository contains the sources for various of my Reference Cards / Cheat
Sheets, available at https://michaelgoerz.net/refcards/.

Mostly, these are in LaTeX or Plain TeX (possibly generated through a Python
script), although some of the older refcards were written in Open Office (before
I wised up to the fact that text processors are not suitable for tightly
typeset documents that you still want to be able to reproduce ten years later).

## Prerequisites

* Full LaTeX installation ([texlive 2018](https://www.tug.org/texlive/) should do)
* [Python >= 3.5](https://www.anaconda.com/download/)
* [Open Office](https://www.libreoffice.org) for *.odt files
* gnu make (macOS: `xcode-select --install`)
* [ImageMagick](http://www.imagemagick.org/script/index.php) (macOS: `brew install imagemagick`)


## Generate the refcards

To generate *all* refcards, run

    make

To return the repository to a clean state, removing all generated refcards, run

    make distclean

You can also remove build-artifacts (such as tex-aux files) with

    make clean

To collect the files for https://michaelgoerz.net/refcards/, I use

    make collect


If you only want to generate a particular refcard, you can also run
`make`/`make clean`/`make distclean` from within the folder for that refcard.

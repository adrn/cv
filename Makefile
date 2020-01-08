LATEX       = xelatex
RM          = rm -rf

TMP_SUFFS   = aux bbl blg log dvi ps eps out synctex.gz fdb_latexmk fls
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})

ALL_FILES = cv.pdf

all: pubstex ${ALL_FILES}

%.pdf: %.tex
	${LATEX} $<

getpubs:
	python get_pubs.py

pubstex:
	python pubs2tex.py

clean:
	${RM_TMP} ${ALL_FILES}
	rm *~

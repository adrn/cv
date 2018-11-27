LATEX       = xelatex
RM          = rm -rf

TMP_SUFFS   = aux bbl blg log dvi ps eps out synctex.gz
RM_TMP      = ${RM} $(foreach suff, ${TMP_SUFFS}, *.${suff})

ALL_FILES = cv.pdf

all: ${ALL_FILES}

%.pdf: %.tex
	${LATEX} $<

clean:
	${RM_TMP} ${ALL_FILES}
	rm *~

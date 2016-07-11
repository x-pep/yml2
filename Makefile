YML_PATH=
YML2C=yml2c

all: homepage

homepage: index.html features.html yslt.html toolchain.html programming.html hello.html

update: homepage format.css gpl-2.0.txt
	rsync -avC *.html *.yml2 format.css *.yhtml2 gpl-2.0.txt samples dragon:fdik.org/yml2/

update-all: update yml2c yml2.py pyPEG.py backend.py yml2proc
	if test -z $(VERSION) ; then echo VERSION not set ; exit 1 ; fi
	rsync -avC *.py yml2c Makefile yml2proc xml2yml.ysl2 standardlib.ysl2 samples dragon:fdik.org/yml2/
	ssh dragon bash -c "cd ; cd fdik.org/; tar cvjf yml-$(VERSION).tar.bz2 yml2/{*.py,*.yml2,*.yhtml2,format.css,gpl-2.0.txt,yml2c,Makefile,yml2proc,xml2yml.ysl2,standardlib.ysl2,samples} ; rm yml2.tar.bz2 ; ln -s yml-$(VERSION).tar.bz2 yml2.tar.bz2"

%.html: %.en.yhtml2 heading.en.yhtml2 homepage.en.yhtml2
	$(YML2C) $< -o $@

clean:
	rm -f *.html *.pyc *.pyo

.PHONY: all search snowball watchdog screen bib figures readme paper check clean

all: screen bib figures readme paper check

search:
	python3 scripts/search.py

snowball:
	python3 scripts/snowball.py

watchdog:
	python3 scripts/watchdog.py

screen:
	python3 scripts/screen.py

bib:
	python3 scripts/bib_gen.py

figures:
	python3 scripts/figures.py

readme:
	python3 scripts/readme_gen.py

paper:
	cd paper && tectonic -X compile main.tex

check:
	python3 scripts/check.py

clean:
	rm -rf paper/*.aux paper/*.log paper/*.out paper/*.bbl paper/*.blg paper/.tectonic

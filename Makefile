all: test build watch


build:
	@echo "[ === Build === ]"
	@python3 main.py > main.tex
	@xelatex -halt-on-error -file-line-error main.tex 2>&1 > /dev/null
	@xelatex -halt-on-error -file-line-error main.tex | (! grep -i ".*:[0-9]*:.*\|warning")


test:
	@echo "[ === Test === ]"
	@mypy --pretty --no-error-summary main.py


watch:
	@echo "[ === Watch === ]"
	@sh -c "while inotifywait --quiet --event modify main.py; do make --silent test build; done"

build:
	@echo "[ === Build === ]"
	@j2 main.j2 > main.tex
	@xelatex -halt-on-error -file-line-error main.tex | (! grep -i ".*:[0-9]*:.*\|warning")

watch:
	@echo "[ === Watch === ]"
	@sh -c "while inotifywait --quiet --event modify main.j2; do make --silent build; done"

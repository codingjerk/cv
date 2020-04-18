build:
	@echo "[ === Build === ]"
	@j2 main.j2 > main.tex
	@xelatex -halt-on-error main.tex > /dev/null

watch:
	@echo "[ === Watch === ]"
	@sh -c "while inotifywait --quiet --event modify main.j2; do make --silent build; done"

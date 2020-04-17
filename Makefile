build:
	@echo "[ === Build === ]"
	@xelatex -halt-on-error main.tex > /dev/null

watch:
	@echo "[ === Watch === ]"
	sh -c "while inotifywait --event modify main.tex; do make --silent build; done"

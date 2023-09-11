SHELL:=/bin/bash

all:
	@echo "choose explicit target = type 'make ' and press TAB"

S=scripts


# ===== MAIN STUFF

char-based:
	cat source | python3 $S/wordbased2charbased.py > source_chars


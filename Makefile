all:
	rm -rf *_formatted
	mkdir recombined_formatted depth10_formatted depth20_formatted
	time ./formatter.py recombined recombined_formatted
	time ./formatter.py depth10 depth10_formatted
	time ./formatter.py depth20 depth20_formatted

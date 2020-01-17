execute:
	python3 -m app

quiet:
	python3 app 2> /dev/null

check:
	python3 -m unittest test

fun:
	python3 -m test

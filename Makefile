.PHONY: clean test

# Run all tests.
test: ../test/*.txt
	../test.sh test.py solution.py

# Clean outputs.
clean:
	rm -rf *.pyc __pycache__

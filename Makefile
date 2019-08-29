.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./specs/generateSpecification.py
clean:
	rm ./tmp/*.json

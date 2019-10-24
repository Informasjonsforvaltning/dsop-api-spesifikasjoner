.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./script/generateSpecification.py -i ./banker.csv
clean:
	rm ./tmp/*.json

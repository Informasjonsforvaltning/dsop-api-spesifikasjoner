.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./specs/generateSpecification.py -i ./banker_05.csv
clean:
	rm ./tmp/*.json

.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./src/dsop_api_spesifikasjoner/generateSpecification.py -i ./banker.csv
clean:
	rm ./tmp/*.json

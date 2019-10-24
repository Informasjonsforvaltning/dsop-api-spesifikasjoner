.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./script/generateSpecification.py -i ./banker_02.csv
clean:
	rm ./tmp/*.json

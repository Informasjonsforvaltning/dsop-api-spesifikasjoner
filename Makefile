.PHONY: test
all: extract transform load

extract:
	echo "Extracting...."
	python3 ./01_extract_organizations/extractOrganizations.py

transform:
	echo "Transforming...."
	python3 ./02_transform/transform.py

load:
	echo "Loading...."
	python3 ./03_load_publishers/loadPublishers.py

clean:
	rm ./tmp/*.json

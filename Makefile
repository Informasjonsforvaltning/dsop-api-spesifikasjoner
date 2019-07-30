.PHONY: test
all: extract transform load

extract:
	python3 ./01_extract_organizations/extractOrganizations.py

transform:
	python3 ./02_transform/transform.py

load:
	echo "TODO: Load"

clean:
	rm ./tmp/*.json

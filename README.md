# dsop-api-spesifikasjoner

A collection of openAPI specifications for the DSOP-banks.

The specifications are generated based on

- the master specification "Accounts API openapi v1.0.0.yaml",
- and the information in the file banker.csv

A simple script is made to do the generation based on the banker.csv file and the following rules:

- The title is a concatenation of the template title and the name of the organization,
- The server url for production is equal to the value in the "EndepunktProduksjon" column,
- The server url for test is equal to the value in the "EndepunktTest" column, and
- The file name of the specification is a concatenation of
  - the organization number,
  - the name of the organization, and
  - the name of the master specification file.
- The id for each data service is equal to the "Id" column and the "TestId" column for the test-catalog. If no id is provided one is generated as a hash of the full path for the specification file.

## Development

### Requirements

- python3
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

### Install

```shell
% git clone https://github.com/Informasjonsforvaltning/dsop-api-spesifikasjoner.git
% cd dsop-api-spesifikasjoner
% pyenv install 3.9.6
% pyenv install 3.7.9
% pyenv local 3.9.6 3.7.9
% poetry install
```

### Run all sessions

```shell
% nox
```

### Run all tests with coverage reporting

```shell
% nox -rs tests

```

## Run cli script

```shell
% poetry shell
% dsop_api_spesifikasjoner --help

```shell
Alternatively you can use `poetry run`:

```shell
% poetry run dsop_api_spesifikasjoner --help
```

Example:

```shell
% dsop_api_spesifikasjoner -d specs template/Accounts\ API\ openapi\ v1.0.0.yaml banker.csv
```

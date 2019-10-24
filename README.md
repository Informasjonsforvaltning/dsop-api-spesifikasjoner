# dsop-api-spesifikasjoner

A collection of openAPI specifications for the DSOP-banks.

The specifications are generated based on

- the master specification "Accounts API openapi v1.0.0-RC2.yaml",
- and the information in the file banker.csv

A simple script is made to do the generation based on the banker.csv file and the following rules:

- The title is a concatenation of the template title and the name of the organization,
- The server url for production is equal to the value in the "EndepunktProduksjon" column,
- The server url for test is equal to the value in the "EndepunktTest" column, and
- The file name of the specification is a concatenation of

  - the organization number,
  - the name of the organization, and
  - the name of the master specification file.

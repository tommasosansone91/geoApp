# postgres inspect commands

List all the schemas

    SELECT schema_name
    FROM information_schema.schemata;

List all the tables of all the schemas

    \dt *.*

List all the tables of a chosen schema

    \dt public.*

    \dt data.*
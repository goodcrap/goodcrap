# `goodcrap`

`goodcrap` is a python package that generates random data stuff: creates and fills data structures (tables, databases and `csv` files) with random data, generates [`Mage`](https://github.com/mage-ai/mage-ai) pipelines that the user can use to orchestrate filling the data structures, and generate random SQL queries.

## Motivation

This software enables data engineers to replicate the database schemas at their organisations, and then generate fake data that resemble a random sample of the actual data in their organisation. It also enables them to generate any number of random SQL queries that they can use for testing their analytics pipelines, as well as benchmark their data platforms.

While public datasets, such as those hosted at Google or Kaggle, is a common starting point for people interested in learning data analytics and machine learning, many of these datasets require extensive data cleaning so that they can be usable in analytics pipelines. This makes the use of these datasets difficult for AI learners and practitioners.

Public datasets are also utilized by data engineers who are interested in testing their ETL/ELT pipelines. Those folks are particularly interested in data quantity, more than quality. Most public datasets are limited in quantity, which make them not so useful for testing pipelines or for benchmarking query execution times.

Nowadays, generating random data is increasingly a requirement for data teams. [It is a better alternative to using public datasets that require cleaning](https://motherduck.com/blog/python-faker-duckdb-exploration/).

`goodcrap` was developed to enable:
- AI learners to generate their own custom datasets
- AI practitioners to benchmark the scalability of their models and methods
- data engineers to test and benchmark their ETL/ELT data pipelines
- data engineers to benchmark query execution times against custom-made huge datasets

The data generated by `goodcrap` is, after all, crap. But it's good crap because:
- data values are configured based on `json` configuration files
- data can be generated to fill tables, databases, data warehouses and data lakes
- data values can be made totally random, or fulfill a certain distribution
- `goodcrap` server can generate time series data

## Installation

You can install `goodcrap` using the `pip` command as follows:

`pip install goodcrap`

## Basic usage

The simplest use-case scenario is generating a `csv` file with random data. `goodcrap` ships with a number of *template* tables that you can use. For example, let's generate 10,000 records in the `customers` table, using the random seed `3`:

`goodcrap --size 10000 --seed 3 --template_table customers --to_csv`

The file `customers.csv` will be generated. 

`goodcrap` populate databases with random data, in addition to filling `csv` files. You can set `goodcrap` to connect to your database via a database configuration file, the name of which is passed to `goodcrap` via the command line argument `--database_config`. This is a json file that looks like this (for a MySQL database):

```json
{
    "db_type": "mysql",
    "host":"localhost",
    "port":"3306",
    "user":"root",
    "passwd":"",
    "database":"goodcrap"
}
```

Here is an example command to create and fill the `customers` table in the database:

`goodcrap --size 1000 --seed 3 --database_config mysql_config --template_table customers --to_csv`

where `mysql_config` is the name of the configuration `json` file (`mysql_config.json`).

For every table `mytable` you want to fill with random values, you must provide either:
- a file `mytable.crap_labels.json`: this file tells `goodcrap` what sort of random values to generate for each record
- a sample database table or `csv` file with matching structure and with some values: `goodcrap` will learn how to generate new random values based on the sample values

### Supported destinations

Currently, `goodcrap` can write data to the following destinations:
- MySQL
- SQLite
- Snowflake
- `csv` file
- `json` file
- `parquet` file

### Template data structures

`goodcrap` has a number of template tables and databases that you can use. They are in the `templates/` directory.

## The `crap_labels.json` settings file

For every table you want to generate, you have to provide the `crap_labels.json` file. If you are using the python library, then you can pass the `crap_label` dictionary instead - as is explained below.

The dictionary in `crap_labels.json` tells `goodcrap` how to fill each column in the table with random values. You can either use any of the `faker` providers there, or you can use the ones in `crappers`.

## How random data is made: `faker` and `crappers`

*in progress*

## Python library

The class `GoodCrap` is your `goodcrap` interface. You instantiate it with the key settings, and then generate the data by using the member functions `write_csv()`, `get_dataframe()` or `run()`.
- `write_csv()`: writes a `csv` file
- `get_dataframe()`: returns a `pandas` `DataFrame` object populated with the random data
- `run()`: that's the more generic function that can generate tables and databases and populate them

And example usage for the `goodcrap` library is as follows. Here we are generating a `pandas` `DataFrame` for one of the template tables, `customers`:

```python
from goodcrap import GoodCrap
a = GoodCrap(seed=3,size=1000,template_table='customers')
df=a.get_dataframe()
```

The following example generates the data frame for some table, given its `crap_label` configuration object:

```python

gc = GoodCrap(size=10000,seed=123)
craplabels = {
    "customer_number": "ssn",
    "first_name": "first_name",
    "last_name": "last_name",
    "phone": "phone_number",
    "address_line": "street_address",
    "city": "city",
    "state": "state",
    "postalcode": "postalcode",
    "country": "current_country",
    "date_of_birth": "date",
    "credit_limit": {
        "type": "random_int",
        "min": 0,
        "max": 1000,
        "multiplier": 10
    },
    "income": {
        "type": "random_int",
        "min": 0,
        "max": 10000,
        "multiplier": 10
    }
}
df = gc.get_dataframe('customers',craplabels)
```

## How data for a foreign key column is generated

`goodcrap` will detect whether a column in a table is related to another table, and will fill that column with random selections of the related column. To demonstrate, run this command:

`goodcrap --size 1000 --seed 3 --database_config examples\mysql_config --template_database customers_orders`

This command will use the database settings in `examples\mysql_config.json` to generate the template database `customers_orders` and fill the tables with 1000 rows each. There are two tables here: `customers` and `orders`, and they are related: `orders` has a column `customer_number` that is tied to `customers` via the foreign key `customers.customer_number`. Therefore, that column is filled with random selections from `customers.customer_number`.

For a quick demo of generating the `orders` table: assuming you have setup up the `customers_orders` database and filled it with some data, the following code will generate an `orders` `DataFrame` using columns values from the `customers` table:

```python
from goodcrap import GoodCrap
a = GoodCrap(seed=3,size=1000,template_table='orders',database_config="../examples/mysql_config")
df=a.get_dataframe()
```

## `goodcrap` with `Mage`

`goodcrap` can be used in `Mage` as a `Data Loader`. You can generate as much data as you want from multiple random `goodcrap` Data Loaders into your pipelines for testing, such as for testing the convergence of data into a data warehouse. You can also schedule the generation of data from `goodcrap` sources to simulate time series data traffic. A typical test-case scenario here is to run an SQL query at the data destination while data is being continuously loaded.

Here is an example `goodcrap` source in `Mage`:

```python

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from goodcrap import GoodCrap

@data_loader
def load_data(*args, **kwargs):
    gc = GoodCrap(size=10000,seed=123)
    craplabels = {
        "customer_number": "ssn",
        "first_name": "first_name",
        "last_name": "last_name",
        "phone": "phone_number",
        "address_line": "street_address",
        "city": "city",
        "state": "state",
        "postalcode": "postalcode",
        "country": "current_country",
        "date_of_birth": "date",
        "credit_limit": {
            "type": "random_int",
            "min": 0,
            "max": 1000,
            "multiplier": 10
        },
        "income": {
            "type": "random_int",
            "min": 0,
            "max": 10000,
            "multiplier": 10
        }
    }
    return gc.get_dataframe('customers',craplabels)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

```
*Note:* If you are planning to run a `Mage` pipeline multiple times, then make sure that it does not have columns that are generated using the faker.unique function. The columns should be universally unique.

## `goodcrap` generates `Mage` pipelines

`Mage` python files are generated using `Jinja` templates. Given that Mage will always be backwards compatible (according to communication with its authors), files and folders generated by `goodcrap` will always be valid. Here is an example command to generate pipelines for each of the tables in the template database `customers_orders`:

`goodcrap --size 1000 --seed 3 --database_config examples\mysql_config --template_database customers_orders --mage_pipeline`

Note that `goodcrap` currently will only generate `Mage` projects if the database configurations are defined.

## Writing to Snowflake

`goodcrap` supports writing your random table to Snowflake using two methods:
- row-by-row, which can be done by setting Snowflake as your database in the database configuration file
- bulk upload of the generated `pandas DataFrame`, which is enabled by the command line argument `--bulk_upload`.

The bulk upload is obviously preferred. Below is an example configuration settings file:

```json
{
    "db_type": "snowflake",
    "snowflake_database":"GOODCRAP",
    "snowflake_warehouse":"WH",
    "snowflake_user":"user",
    "snowflake_password":"password",
    "snowflake_account":"account",
    "snowflake_schema":"public",
    "snowflake_role":"role"
}
```

Suppose you want to create the `orders` table in Snowflake and fill it with 1,000,000 rows, and also get a few sample queries to try. You can get all that with the following command:

```
goodcrap --size 1000000 --seed 12 --database_config config --template_table orders --bulk_upload --queries 100
```

## Data warehouses

Some dimensions in data warehouses will required to be filled as part of the testing exercise, but should not be filled with random data. These are the *conformed* dimensions with rigid data, such as the Date, Countries, and Cities dimensions. `goodcrap` will be able to fill these dimensions using the `DimensionFiller` class by providing several options for featurization. Filling these tables will be performed before any other table is populated.

## Guessing the `crap_labels.json` settings

*in progress*

## Learning the values from a data sample

*in progress*

## Contributing to `goodcrap`

That would be much appreciated. Check [here](CONTRIBUTING.rst).

## License

`goodcrap` is licensed under the [GPL3](LICENSE) license.


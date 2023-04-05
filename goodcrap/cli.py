import argparse
import itertools
import logging
import os
import random
import sys
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, TextIO, TypeVar, Union


class CLI:
    def __init__(self, argv: Optional[str] = None) -> None:
        self.argv = argv or sys.argv[:]
        self.prog_name = Path(self.argv[0]).name
        self.formatter_class = argparse.RawDescriptionHelpFormatter
        self.epilog = 'Epilogue'
        self.version = '0.1.0'

        default_locale = os.environ.get("LANG", "en_US").split(".")[0]
        # if default_locale not in AVAILABLE_LOCALES:
        #     default_locale = DEFAULT_LOCALE

        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=f"{self.prog_name} version {self.version}",
            epilog=self.epilog,
            formatter_class=self.formatter_class,
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {self.version}"
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="verbosity"
        )

        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="set the seed for randomg number generator",
        )

        parser.add_argument(
            "-s",
            "--size",
            default=1000,
            type=int,
            help="size of the generated table(s)",
        )

        parser.add_argument(
            "--template_table",
            "-t",
            type=str,
            help="specify one of the tables in the template library",
        )

        parser.add_argument(
            "--template_database",
            "-d",
            type=str,
            help="specify one of the databases in the template library",
        )

        parser.add_argument(
            "--to_csv",
            action="store_const",
            const='to_csv',
            help="stores data to a csv file",
        )

        parser.add_argument(
            "--to_json",
            action="store_const",
            const='to_json',
            help="stores data to a csv file",
        )

        parser.add_argument(
            "--database_config",
            "-j",
            type=str,
            help="name of json file that includes the database configuration",
        )

        parser.add_argument(
            "--table_sql",
            "-q",
            type=str,
            help="name of sql file that includes the table data definition statements",
        )

        parser.add_argument(
            "--table_crap_labels",
            "-l",
            type=str,
            help="name of json file that includes the configuration of the table to be filled",
        )

        parser.add_argument(
            "--database_sql",
            "-Q",
            type=str,
            help="name of sql file that includes the data definition statements of the table in the database",
        )

        parser.add_argument(
            "--database_crap_labels",
            "-L",
            type=str,
            help="name of json file that includes the configuration of the table to be filled",
        )

        parser.add_argument(
            "--guess_crap_labels",
            "-g",
            type=str,
            help="infer the crap labels from the data in the provided csv file",
        )

        arguments = parser.parse_args(self.argv[1:])
        random.seed(arguments.seed)

        from .goodcrap import GoodCrap
        good_crap = GoodCrap(size=arguments.size,
                             seed=arguments.seed,
                             to_csv=arguments.to_csv,
                             to_json=arguments.to_json,
                             template_database=arguments.template_database,
                             template_table=arguments.template_table,
                             database_config=arguments.database_config,
                             table_sql=arguments.table_sql,
                             table_crap_labels=arguments.table_crap_labels,
                             database_sql=arguments.database_sql,
                             database_crap_labels=arguments.database_crap_labels
                             )

        good_crap.run()



def execute_cli(argv: Optional[str] = None) -> None:
    cli = CLI()

if __name__ == "__main__":
    execute_cli()
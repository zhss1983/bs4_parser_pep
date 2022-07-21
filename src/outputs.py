import csv
import logging
from datetime import datetime as dt

from prettytable import PrettyTable

from constants import BASE_DIR, DT_FILE_FORMAT


def file_output(results, cli_args):
    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    file_name = f"{cli_args.mode}_{dt.now().strftime(DT_FILE_FORMAT)}.csv"
    file_path = results_dir / file_name
    with open(file_path, mode="w", encoding="utf-8") as file:
        writer = csv.writer(file, dialect="unix")
        writer.writerows(results)
    logging.info("Файл с результатами был сохранён: %s", file_path)


def default_output(results, _=None):
    for row in results:
        print(*row)


def pretty_output(results, _=None):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = "l"
    table.align[results[0][1]] = "c"
    table.add_rows(results[1:])
    print(table)


OUTPUT = {
    "pretty": pretty_output,
    "file": file_output,
    None: default_output,
}


def control_output(results, cli_args):
    OUTPUT[cli_args.output](results, cli_args)

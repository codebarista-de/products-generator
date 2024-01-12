#!/usr/bin/env python

import glob
import os
import csv
import openpyxl
import pathlib
import shutil
import traceback

OUT_DIR = "Ausgabe"
ERROR_FILE = f"{OUT_DIR}/FEHLER.txt"

PRODUCT_NUMBER = "Artikelnummer"
PRODUCT_NAME = "Produktname"


def writeError(e: str):
    with open(ERROR_FILE, "w") as file:
        print("Fehler: " + e)
        file.write(e)


def readTemplate(path: str) -> str:
    with open(path, "r") as template:
        return template.read().strip()


def generateProductDescriptions(template_file: str, values_file: str):
    template = readTemplate(template_file)
    excel = openpyxl.Workbook(write_only=True)
    products_sheet = excel.create_sheet("Products")
    products_sheet.append(
        [
            "ID",
            "Produktnummer",
            "Name",
            "Beschreibung",
            "Meta Tite",
            "Meta Beschreibung",
            "Meta Keywords",
        ]
    )
    row_num = 1
    with open(values_file, newline="") as csvfile:
        for row in csv.DictReader(csvfile):
            product_number = row.get(PRODUCT_NUMBER, "").strip()
            product_name = row.get(PRODUCT_NAME).strip()
            if not product_number:
                raise ValueError(
                    f'In Zeile {row_num} von {values_file} fehlt der Wert für "{PRODUCT_NUMBER}"'
                )
            if not product_name:
                raise ValueError(
                    f'In Zeile {row_num} von {values_file} fehlt der Wert für "{PRODUCT_NAME}"'
                )
            product_description = createProductDescription(template, row)
            meta_titel = row.get("Meta Titel", "").strip()
            meta_description = row.get("Meta Beschreibung", "").strip()
            meta_keywords = row.get("Meta Keywords", "").strip()
            products_sheet.append(
                [
                    "",
                    product_number,
                    product_name,
                    product_description,
                    meta_titel,
                    meta_description,
                    meta_keywords,
                ]
            )
    out_file_name = pathlib.Path(values_file).stem + ".xlsx"
    excel.save(str(pathlib.Path(OUT_DIR, out_file_name)))


def createProductDescription(template: str, values: dict) -> str:
    description = template
    for key, value in values.items():
        description = description.replace(f"<{key}>", value)
    return description


if __name__ == "__main__":
    try:
        output_dir = pathlib.Path(OUT_DIR)
        if output_dir.is_dir():
            shutil.rmtree("Ausgabe")
        elif output_dir.is_file():
            output_dir.unlink()
        os.makedirs("Ausgabe", exist_ok=True)

        template = glob.glob("Eingabe/*.html")
        value_file = glob.glob("Eingabe/*.csv")

        if len(template) != 1:
            template_files = "\n".join(template)
            writeError(
                f"""Es muss genau eine .html Datei im Order Eingabe liegen.
    Anzahl der gefundenen .html Dateien: {len(template)}\n{template_files}"""
            )
            exit(1)

        if len(value_file) != 1:
            value_files = "\n".join(value_file)
            writeError(
                f"""Es muss genau eine .csv Datei im Order Eingabe liegen.
    Anzahl der gefundenen .csv Dateien: {len(value_file)}\n{value_files}"""
            )
            exit(1)

        generateProductDescriptions(template[0], value_file[0])

    except Exception:
        writeError(traceback.format_exc())

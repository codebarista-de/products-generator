# Products Generator

A fast way to update the description and other infos of products in your Shopware 6 store.

Generates an EXCEL file with product data from a CSV file and an HTML template compatible with the Shopware Desktop Tool.

The Shopware Desktop Tool is a desktop application that allows you to manage the product data in your Shopware-Store with Excel.
If you are interested in the Shopware Desktop Tool, please [contact us](https://codebarista.de/en/contact/).

## How it works

Here is an example:

`products.csv`
```
Artikelnummer,Produktname,Color
SW10001,T-Shirt,green
SW10002,T-Shirt,blue
SW10003,Trouser,yellow
```

`description-template.html`
```
<p>Have fun with your <Color> <Produktname></p>
```

If you put those two files in a folder named "Eingabe"
```
./Product-Generator
  Eingabe/
    products.csv
    description-template.html
```

and then run the generator an Excel file named `products.xlsx` be generated in a folder called "Ausgabe" with the following content:

| ID | Produktnummer | Name    | Beschreibung                                    |...|
| ---|---------------| --------|-------------------------------------------------|---|
|    | SW10001       | T-Shirt | \<p\>Have fun with your green T-Shirt\</p\>         |...|
|    | SW10002       | T-Shirt | \<p\>Have fun with your blue T-Shirt\</p\>          |...|
|    | SW10003       | Trouser | \<p\>Have fun with your yellow Trouser\</p\>        |...|

The Excel file can then be imported with the Shopware Desktop Tool into a Shopware 6 store to update the name,
description and other properties of the products `SW10001`, `SW10002` and `SW10003`.


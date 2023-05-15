# RSS Feed Generator

## Description

This project is an extension of the wonderful _RSS Feed Generator_ by [@drego85](https://github.com/drego85/RSSFeedGenerator).

It is a web API in Python + Flask. It provides RSS feeds for popular websites which do not provide them. The websites are scraped manually, so eventual changes to their layouts may break the feed. If yo find a broken feed, please open an issue on the GitHub page.

The API is available as a Docker image over `ghcr.io/mfranzil/rssfeedgenerator`.

For additional information, visit the aforelinked GitHub page.

## Installation

Using any virtual enviroment is recommended. This project was developed using `miniforge/conda 23.1.0` and `python 3.11.3` on macOS Ventura `13.3.1 (a)`.

To get started, first install the dependencies.

```bash
pip install -r requirements.txt
```

Then run the server:

```bash
python server.py
```

A `direnv` installation is recommended for automatically adding the `PYTHONPATH` variable to the shell and allow easy local debugging.

## Available sources

* [Domani](https://editorialedomani.it/)
* [Unione Sarda](https://www.unionesarda.it)
* [Ferrovie.it](https://www.ferrovie.it/)
* [Eclectic Light](https://eclecticlight.co/) - only news with the MacOS tag
* [AeroBA Fondazione Mach](https://aeroba.fmach.it/bollettino) -  news on pollen concentration in Trentino from Fondazione Bruno Mach
* [Federazione Italiana Pallacanestro](https://fip.it/) - official communications by the CIA (Comitato Italiano Arbitri), the Veneto committee, and the Trentino-Alto-Adige committee

## Credits

* [Andrea Draghetti](https://twitter.com/AndreaDraghetti) - original author
* [Padraic Cunningham](http://stackexchange.com/users/2456564/padraic-cunningham?tab=accounts) - original author, code support
* [Matteo Franzil](https://github.com/mfranzil) - adapted the original RSS Feed Generator

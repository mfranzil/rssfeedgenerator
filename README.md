# RSS Feed Generator


## Description

This project is an extension of the wonderful _RSS Feed Generator_ by [@drego85](https://github.com/drego85/RSSFeedGenerator).

It is an Azure Functions-ready web API in Python + Flask. It provides RSS feeds for popular websites which do not provide them. The websites are scraped manually, so eventual changes to their layouts may break the feed.

For additional information, visit the aforelinked GitHub page.

A temporary instance of this project is currently available at [https://mfranzil-rssgenerator.azurewebsites.net/](https://mfranzil-rssgenerator.azurewebsites.net/).

## Installation

Using any virtual enviroment is recommended. This project was developed using `miniforge 4.12.0` and `python 3.9.7` on macOS Monterey `12.3.1`. Please take note that `python 3.10` or later is not currently (2022-05-07) supported on Azure Functions.

To get started, first install the dependencies.

```bash
pip install -r requirements.txt
```

Then run the server:

```bash
python server.py
```

A `direnv` installation is recommended for automatically adding the `PYTHONPATH` variable to the shell and allow easy local debugging.

### Credits

* [Andrea Draghetti](https://twitter.com/AndreaDraghetti) - original author
* [Padraic Cunningham](http://stackexchange.com/users/2456564/padraic-cunningham?tab=accounts) - original author, code support
* [Matteo Franzil](https://github.com/mfranzil) - adapted the original RSS Feed Generator

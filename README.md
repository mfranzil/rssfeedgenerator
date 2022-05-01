# RSS Feed Generator


## Description

This project is an extension of the wonderful _RSS Feed Generator_ by [@drego85](https://github.com/drego85/RSSFeedGenerator).

It is an Azure Functions-ready web API in Python + Flask. It provides RSS feeds for popular websites which do not provide them. The websites are scraped manually, so eventual changes to their layouts may break the feed.

For additional information, visit the aforelinked GitHub page.

A temporary instance of this project is currently available at [https://mfranzil-rssgenerator.azurewebsites.net/](https://mfranzil-rssgenerator.azurewebsites.net/).

## Installation

Using a virtual enviroment of one's choice is recommended. First install the dependencies:

```bash
pip install -r requirements.txt
```

Then run the server:

```bash
python server.py
```


### Credits

* [Andrea Draghetti](https://twitter.com/AndreaDraghetti) - original author
* [Padraic Cunningham](http://stackexchange.com/users/2456564/padraic-cunningham?tab=accounts) - original author, code support
* [Matteo Franzil](https://github.com/mfranzil) - adapted the original RSS Feed Generator

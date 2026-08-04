# MassLandlords Scraper

<img width="421" alt="mll_screenshot" src="https://user-images.githubusercontent.com/10646361/225936089-c8fa5233-72bd-46c2-b211-99d2ddf37e51.png">

An exremely simple Python scraper to collect weekly [eviction filing counts from MassLandlords](https://masslandlords.net/policy/eviction-data/). We use these counts to validate the number of filings we're retrieving using our [filing downloader tool](https://github.com/Unnamed-Lab-DUSP/filing_downloader). It fetches all counts starting from the week ending 10-24-2020 and continuing through the most recent available week.

## Contributors

+ [Eric Robsky Huntley, PhD](https://github.com/ericrobskyhuntley) (💻, 🤔)
+ [Ever Real](https://github.com/anastasia) (💻, 🤔)

## Setting Up Your Environment

The Python environment necessary for this tool is managed using [`uv`](https://github.com/astral-sh/uv), an extremely fast Python package and project manager that replaces `pip`, `pipenv`, and `pyenv`. 

### Install `uv`

If you haven't installed uv yet, follow the [official installation guide](https://github.com/astral-sh/uv). For most systems, this is a single command: 

```sh
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Requirements

`uv` will automatically manage your Python version and virtual environment based on the project configuration. Simply run: 

```bash
uv sync
```

This creates a .venv directory and installs all dependencies exactly as specified in the lockfile. 

## Running the Tool

To run the rool, use `uv run`:

```bash
uv run masslandlords_scraper
```

## Activating Your Environment

If you need to enter the environment for development (e.g., to run arbitrary commands), use:

```bash
source .venv/bin/activate # On Windows: .venv\Scripts\activate
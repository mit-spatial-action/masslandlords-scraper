# MassLandlords Scraper

<img width="421" alt="mll_screenshot" src="https://user-images.githubusercontent.com/10646361/225936089-c8fa5233-72bd-46c2-b211-99d2ddf37e51.png">

A very simple scraper to collect weekly and monthly[eviction filing counts from MassLandlords](https://masslandlords.net/policy/eviction-data/). We use these counts to validate the number of filings we're retrieving from MassCourts using our semi-automated internal systems. It fetches all counts starting from the week ending 10-24-2020 and continuing through the most recent available week. __Note that MassLandlords stopped posting weekly reports in July of 2023, so no weekly counts will be retrieved beyond that date.__

## Contributors

+ [Eric Robsky Huntley](https://github.com/ericrobskyhuntley) (💻, 🤔)
+ [Ever Real](https://github.com/qbious) (💻, 🤔)

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

### Command Line Usage

We provide a few arguments to support querying for subsets (by date) and selecting the location of output files.

| Short | Long Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `-s` | `--start` | `String` | `2020-10-24` | Start date. |
| `-e` | `--end` | `String` | `datetime.today().strftime("%Y-%m-%d")` | End date. |
| `-p` | `--path`| `String`| `./` | Path to output CSV files. |

## Activating Your Environment

If you need to enter the environment for development (e.g., to run arbitrary commands), use:

```bash
source .venv/bin/activate # On Windows: .venv\Scripts\activate
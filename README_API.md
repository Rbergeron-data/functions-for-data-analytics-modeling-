# FBI Crime Data Explorer (CDE) API Wrapper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A specialized Python utility designed to simplify data extraction from the [FBI Crime Data Explorer API](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi). This tool automates the injection of path variables, handles authentication, and aggregates multi-year datasets into a single Pandas DataFrame.

## 🚀 Overview

The FBI API often requires specific URL pathing (e.g., `/state/MA/burglary`). This wrapper streamlines the process by:
1.  **Parsing dynamic endpoints** and prompting the user for required variables.
2.  **Initializing sessions** to verify API key validity.
3.  **Automating multi-year fetches** to overcome the single-year limit of standard API calls.



---

## 🛠️ Prerequisites

Before running the script, ensure you have your API key and the necessary libraries:

1.  **API Key:** Obtain one for free at [api.data.gov](https://api.data.gov/signup/).
2.  **Dependencies:**
    ```bash
    pip install requests pandas regex
    ```

---

## 📖 Usage

### 1. Basic Initialization
Define your base URL and the endpoint path. Use `{curly_braces}` for any variables the API requires in the URL string.

```python
from fbi_api_tool import initialize_FBI_API, MultiYearPull

MyKey = "YOUR_API_KEY_HERE"
base = "[https://api.usa.gov/crime/fbi/cde/](https://api.usa.gov/crime/fbi/cde/)"

# The function will prompt you to enter 'state_abbr' in the console
path = "reporting-agency-level/{state_abbr

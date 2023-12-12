# OSINT Dashboard
OSINT Dashboard is a web-based Open Source Intelligence (OSINT) tool designed to consolidate and streamline the analysis of various data sources. This tool provides users with the ability to gather and examine information from URLs, image files, and phone numbers. The primary data that the dashboard collects include:

* URL Analysis:
    * IP/Server Information
    * Domain(Whois)
    * Screenshots
    * Cookies
    * Headers
    * DNS Records
    * SSL Certificates
    * Page Redirects
    * Sitemaps
    * Internal/External Links
    * Open Ports
    * Linked Phone Numbers
    * Linked Emails

* Exif Data Viewer
* Phone Number Lookup

The OSINT Dashboard will not only collect and present this information, but will also provide users with insight on the information that it finds. It aims to simplify the process of gathering data from diverse sources, making it a valuable resource for OSINT investigators and researchers. The OSINT Dashboard is currently deployed using Microsoft Azure, at http://osintdashboard.info/.

# Installation

Before you begin, make sure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.11 or higher)

## Getting Started

1. Clone the Repository:

    ```bash
    git clone https://github.com/campwill/osint-dashboard/
    cd osint-dashboard
    ```

2. Install Dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Creating .env File:

   You will need to create a configuration file named .env and move it to the osint-dashboard directory.
   This file will hold you API keys. The file should be layed out like this:
   ```
   IPINFO_API_KEY=[insert_value_here] 
   SECRET_KEY=[insert_value_here]
   NUM_API_KEY=[insert_value_here]
   ```
   The first key is an API key for [ipinfo.io](https://ipinfo.io/), the second is a Flask secret key, and the last is an API key for [NumVerify](https://numverify.com/).

## Running the Flask Application

1. Set Flask App:

    ```bash
    python app.py
    ```

   This will start the development server. By default, you can access the application at [http://127.0.0.1:5001/](http://127.0.0.1:5001/) in your web browser.

## Stopping the Application

To stop the Flask development server, press `Ctrl+C` in the terminal where it is running.

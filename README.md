# BTC Key Info Viewer

BTC Key Info Viewer is a Python-based GUI tool that allows users to analyze Bitcoin private keys in both WIF and HEX formats. The tool displays detailed information, including the public key (compressed and uncompressed), BTC addresses, and balance using the Mempool API.

## Features

- Accepts private keys in WIF or HEX format.
- Displays compressed and uncompressed public keys and BTC addresses.
- Retrieves BTC balance via Mempool API.
- Dark-themed interface with green text for better visibility.

## Installation

Clone this repository:
   
   `git clone https://github.com/franklin-lol/BTC_HEX-2-key.git
   cd BTC_HEX-2-key`

Install dependencies:


   `pip install -r requirements.txt`

Run the application:


   `python BTC_HEX-2-key.py`

## Usage

Enter your private key in either WIF or HEX format.
Select the key format (WIF or HEX) using the radio buttons.
Click "Show" to view the details.
The application will display the following:
Private key in WIF and HEX formats.
Compressed and uncompressed public keys.
Corresponding BTC addresses.
Current BTC balance.
Screenshots
Main Interface

## Requirements
Python 3.8 or higher
Active internet connection for balance retrieval



## License
This project is licensed under the MIT License. See the LICENSE file for details.

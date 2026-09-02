# veracode-assign-apps-to-single-team
Reads a list of applications and replaces their current team assignment for the specified team

## Requirements:
- Python 3.12+

## Setup

Clone this repository:

    git clone https://github.com/cadonuno/veracode-assign-apps-to-single-team

Install dependencies:

    cd veracode-assign-apps-to-single-teamv
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Preparation
The script reads a file named ``applications.txt``, this file should contain the names of **ALL** applications you want to update, one per line.

## Run
If you have saved credentials as above you can run:

    python assign-apps-to-single-team.py

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python assign-apps-to-single-team.py

When running, you will be prompted for the team name, it is not case-sensitive,  but must contain the full name.

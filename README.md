# TwitterDataAnalysis
FWPM Applied Data Science with Python Project at OTH Regensburg.
This project let the user fetch tweets, users, followers of a user and tweets of a follower 
for an entered topic through which he/she can browse. Moreover, he can analyse the polarity of
each tweet.

For more have a look at the Documenation at `docs/Documentation.pdf`.

>**Table of Contents**
>  - [Prerequisites](#Prerequisites)
>  - [Installation](#Installation)
>  - [Usage](#Usage)
>  - [Usage without TwitterClient](#Usage-without-TwitterClient)


## Prerequisites
- For executing the project any python version higher than python3.8 is required.
- This project only works on Linux Systems due the use of the simple-term-menu library! 
Please use either a Linux VM (of any distribution) or setup the Windows Subsystem Linux (WSL) on Windows.
- Create a twitter developer account and app. Save your generated bearer token, which you will have to set (see [Usage](#usage)).
- (optional) To keep your system clean the recommendation is to create a venv with 'python3 -m venv'.

## Installation
Clone the GitHub repository or download the source code and de-zip it.

Install all needed modules listed in requirements.txt or run:
```bash
pip install -r requirements.txt
```

## Usage
To start the program, ensure you are on the toplevel of this project.

To enable the Twitterclient set your bearer token as environment variable:
```bash
export TWITTER_BEARER_TOKEN=<your bearer token>
```

Then run:
```bash
python3 main.py
```

## Usage without TwitterClient
Actually this program is even usable without setting the bearer token for the Twitterclient.
Obviously it's not possible to fetch data from twitter then but besides that the program is fully
usable for prefetched dataset.
Only run following command to start the program:
```bash
python3 main.py
```

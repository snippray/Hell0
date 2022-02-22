# Introduction

At first, I am not a developer! I am just an information security enthusiast interested in automating security operations. I hope my interest matches yours, and by your contribution, we could enhance this program and make it more beneficial for those concerned about their privacy and security in cyberspace.
So, let's get down to business. **Hello Zero** is a straightforward yet powerful and effective tool designed to be a part of the organization's vulnerability and risk management program. It has been designed to gather zero-day system exploits by extracting information about all hardware and software installed on your system. It automatically scrapes the dark web every day to track zero-day exploits that affect your system. The current version is 1.0, which only supports the **`Windows`** platform at the moment.


## Prerequisites

Required libraries:

- Python-Levenshtein
- FuzzyWuzzy
- PySocks
- Mechanize
- BeautifulSoup4
- PyQt5
- Packaging
- PySimpleGUI

  
The prerequisites can be effortlessly installed via `pip install -r requirements.txt` command.
It also requires TOR, MySQL (or any other databases), and Python 3.


## Getting Started
The only thing you need to do is run the app and set the E-mail address you would like to receive alerts in "Emails.txt," and **Hello Zero** will do the rest for you.


## How it works

After collecting all information about software/hardware installed on your system and their corresponding version, Hello Zero automatically crawls the dark web for you to track any zero-day exploits that might affect your system. After finding any defects, it will e-mail you with suitable information about what you should notice to avoid these exploits.

NOTE: Hello Zero uses **fuzzy string matching** as well as string metrics to calculate the difference between sequences.

## Why do I need to use this tool?

As mentioned earlier, **Hello Zero** has been designed to complement your vulnerability and risk management programs. Aside from patch management policies, we must be aware of the vulnerabilities traded on the dark web and affect our systems without patches. Therefore, if you are concerned about zero-day threats, this tool is right for you.

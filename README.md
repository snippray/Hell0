# Introduction

At first, I'm not a developer! I'm just an information security enthusiast that is interested in automating security operations. I hope my interest matches yours and by your contribution we could improve this program and make it more useful for those who are concerned about their security hygiene in cyberspace. 

So, lets get down to business.
**Hello Zero** is a very simple to use, yet powerful and effective tool designed to be a part of vulnerability and risk management program in the organization. It has been designed to gather zero-day exploits related to your system by extracting information about all hardware and software installed on your system and automatically scrap the darkweb everyday to track zero-day exploits that affect your system.
This is the version 1.0 and it currently supports **`Windows`** platform.


## Prerequisites

Required libraries:

- python-levenshtein
- fuzzywuzzy
- pysocks
- mechanize
- beautifulsoup4
- PyQt5
- packaging
- PySimpleGUI
  
You can easily install them through `pip install -r requirements.txt`
  
It requires TOR, MySQL(or any other database) and **Python 3** as well.


## Getting Started
The only thing you need to do is to run the app and set the E-mail address you would like to receive alerts in "Emails.txt".

**Hello Zero** will do the rest for you.


## How it works

After collecting all information about software/hardware installed on your system and their corresponding version, Hello Zero automatically crawl the dark web for you to track any 0day exploits that might affect your system. After find any, it will send an E-mail to you about what you should notice.
> NOTE: **Hello Zero** uses fuzzy string matching as well as string metric to calculate the difference between sequences.

## Why i need to use this tool?

As mentioned earlier, **Hello Zero** has been designed to be a complement to your vulnerability and risk management program.
Beside of patch management policy we need to be aware of the vulnerabilities that are traded in the dark web and affect our system while there is no patch for them.

So, if you are concerned about zero-day threats this tool is right for you.

## Contributing

First off, thank you for considering contributing to **Hello Zero**. It's people like you that make it such a useful tool.
For contributing to this repository, please drop me a line and discuss the change you wish to make before making a change.

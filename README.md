# Introduction

At first, I'm not a developer! I'm only an information security enthusiast which is interested in automating security operations. I hope my interest match yours and by your contribution we could improve this program and make it more useful for those who are concerned about the security hygiene in cyberspace. 
So, lets get down to business.
**Hello Zero** helps you extract information about all hardware and software installed on your system and automatically crawl the darkweb everyday to track zero-day exploits which affect hardware/software you have on your system.
This is the version 1.0 and it currently supports **`Windows`** platform.


## Prerequisites

Required libraries:

  python-levenshtein
  fuzzywuzzy
  pysocks
  mechanize
  beautifulsoup4
  
You can easily install them through `pip install -r requirements.txt`
  
It requires TOR, MySQL(or any other database) and **Python 3** as well.


## Getting Started
The only thing you need to do is to specify an email address of a person you want to get notified if related zero-day vulnerabilities are found and put that address in Email.txt.

**Hello Zero** will do the rest for you.

```shell
Hell0.py -u -db SysInfo.db -e emails.txt
```
## How it works

After collecting all information about software/hardware installed on your system and their corresponding version, Hello Zero authomaticlally crawl the dark web for you to track any 0day that might affect your system. After find any, it will send an E-mail to you about what you should notice.
> NOTE: **Hello Zero** uses fuzzy string matching as well as string metric to calculate the difference between sequences.

## Why i need to use this tool?

**Hello Zero** is designed to be a complement for your vulnerability management program.
Beside of a Patch management policy we need to be aware of the vulnerabilities that are traded in the dark web and affect our system while there is no patch for them.
So, if you are concerned about zero-day threats this tool is right for you.

## Contributing

First off, thank you for considering contributing to **Hello Zero**. It's people like you that make it such a great tool.
For contributing to this repository, please drop me a line and discuss the change you wish to make before making a change.

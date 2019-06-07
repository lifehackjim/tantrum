# Origin

Tantrum is based off of [pytan3](https://github.com/lifehackjim/pytan3).

## Features removed

There are a number of things removed from PyTan 3 to make Tantrum easier for me to maintain:

* Removed all documentation (Might add back later)
* Removed all tests (Might add back later)
* Removed the SSL magic from HttpClient (Might add back later, for now you have to get & use SSL certs yourself)
* Removed encrypted credentials support provided by AuthStore (You will have to figure that out on your own)
* Removed support for Tanium's REST API (too much work for me to maintain on my own, and SOAP API will be around for a while)
* Removed support for prompting and colorization of prompts (No plans to add command line wrappers for the foreseeable future)
* Removed depndencies: cert_human, colorama, humanfriendly, privy, dotenv, pathlib2
* Tantrum will only be manually tested against python 3.6 for now. No automatic tests and no manual tests against python 2.
* Tantrum will only be tested against versions I have access to while doing work.

## Features added

On the flipside, Tantrum has some new stuff:

* Workflows for asking questions/getting result data.
* Workflows for getting a list of clients.

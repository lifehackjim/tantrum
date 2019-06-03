[![MIT
license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Tantrum: Tanium Instrumental API wrapper

Tantrum is meant to be an API wrapper for [Tanium](https://www.tanium.com). It makes the Tanium API actually usable by providing native python objects for working with API objects, and also provides workflows for complex multi-call operations.

Tantrum is based off of [pytan3][https://github.com/lifehackjim/pytan3]. I am no longer employed with Tanium, but I will be maintaining Tantrum as I use it to support work I do on contracts. 

Feel free to submit PR's for bug fixes, features, or whatever.

There are a number of things removed from PyTan 3 to make Tantrum easier for me to maintain:

* Removed all documentation (Might add back later)
* Removed all tests (Might add back later)
* Removed the SSL magic from HttpClient (Might add back later, for now you have to get & use SSL certs yourself)
* Removed encrypted credentials support provided by AuthStore (You will have to figure that out on your own)
* Removed support for Tanium's REST API (too much work for me to maintain on my own, and SOAP API will be around for a while)
* Removed support for prompting and colorization of prompts (No plans to add command line wrappers for the foreseeable future)
* Removed depndencies: cert_human, colorama, humanfriendly, privy, dotenv, pathlib2
* Tantrum will only be manually tested against python 3.6 for now. No automatic tests and no python 2 tests.
* Tantrum will only be tested against versions I have access to while doing contract API work.

On the flipside, Tantrum has some new stuff:

* Basic workflow support for asking a question/getting result data.
* Basic workflow for getting a list of clients.

## Installing

Installing tantrum via [pip](https://pypi.org/project/pip/) or [pipenv](https://pipenv.readthedocs.io/en/latest/) will automatically install all of the necessary dependencies.


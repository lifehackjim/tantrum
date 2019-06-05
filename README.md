[![MIT
license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<!-- MarkdownTOC -->

- [Tantrum: Tanium Instrumental API wrapper](#tantrum-tanium-instrumental-api-wrapper)
  - [Installing](#installing)
  - [Examples](#examples)
    - [Connection basics](#connection-basics)
    - [Fun with users](#fun-with-users)
      - [Getting a user by name](#getting-a-user-by-name)
      - [Getting a user by ID](#getting-a-user-by-id)
      - [Adding a user](#adding-a-user)
      - [Modifying a user](#modifying-a-user)
    - [Fun with clients](#fun-with-clients)
      - [Get all clients with no paging and no filters](#get-all-clients-with-no-paging-and-no-filters)
    - [Get all clients with paging but no filter](#get-all-clients-with-paging-but-no-filter)
    - [Get all clients with a filter](#get-all-clients-with-a-filter)

<!-- /MarkdownTOC -->

# Tantrum: Tanium Instrumental API wrapper

Tantrum is meant to be an API wrapper for [Tanium](https://www.tanium.com). It makes the Tanium API actually usable by providing native python objects for working with API objects, and also provides workflows for complex multi-call operations.

Tantrum is based off of [pytan3](https://github.com/lifehackjim/pytan3). Feel free to submit PR's for bug fixes, features, or whatever.

There are a number of things removed from PyTan 3 to make Tantrum easier for me to maintain:

* Removed all documentation (Might add back later)
* Removed all tests (Might add back later)
* Removed the SSL magic from HttpClient (Might add back later, for now you have to get & use SSL certs yourself)
* Removed encrypted credentials support provided by AuthStore (You will have to figure that out on your own)
* Removed support for Tanium's REST API (too much work for me to maintain on my own, and SOAP API will be around for a while)
* Removed support for prompting and colorization of prompts (No plans to add command line wrappers for the foreseeable future)
* Removed depndencies: cert_human, colorama, humanfriendly, privy, dotenv, pathlib2
* Tantrum will only be manually tested against python 3.6 for now. No automatic tests and no manual tests against python 2.
* Tantrum will only be tested against versions I have access to while doing contract API work.

On the flipside, Tantrum has some new stuff:

* Basic workflow support for asking a question/getting result data.
* Basic workflow for getting a list of clients.

## Installing

Installing tantrum via [pip](https://pypi.org/project/pip/) or [pipenv](https://pipenv.readthedocs.io/en/latest/) will automatically install all of the necessary dependencies.

## Examples

These examples are fairly basic and not intended to be full show & tells. More detailed examples will be added over time.

### Connection basics

First, create a file named tantrum_creds.py that has the following:
```
url = "https://192.168.1.32"
username = "USERNAME"
password = "PASSWORD"
```

Then run tantrum_shell.py in python interactive mode to get an adapter established:
```
pipenv run python3 -i tantrum_shell.py
```

You can then access the adapter:
```
>>> print(adapter)
tantrum.adapters.Soap(
  api_objects=tantrum.api_objects.ApiObjects(type='soap', version='7.3.314.3424'),
  api_client=tantrum.api_clients.Soap(url='https://192.168.1.32:443'),
  http_client=tantrum.http_client.HttpClient(url='https://192.168.1.32:443'),
  auth_method=tantrum.auth_methods.Credentials(logged_in=False, last_used_secs=0, expiry_dt=None),
)
```

### Fun with users

There are no workflows for working with users as of yet, but you can use the low-level API objects with the adapter directly to do anything you would want to do.

#### Getting a user by name

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Since the API doesn't allow us to search for user objects by name, we have to get all users and use python locally to filter for our user name:

```
>>> find_obj = api_objects.UserList()
>>> result_obj = adapter.cmd_get(obj=find_obj)
>>> all_users = result_obj()
>>> print(all_users)
UserList() with 37 User objects
```

Now we can use a python list comprehension:
```
>>> admin_user = [u for u in all_users if u.name == "Administrator"][0]
>>> print(admin_user)
User(id=1, name='Administrator', display_name=None)
```

Or we can use a utility method attached to ApiList models:
```
>>> admin_user = all_users.get_item_by_attr(value="Administrator", attr="name")
>>> print(admin_user)
User(id=1, name='Administrator', display_name=None)
```

#### Getting a user by ID

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

The API supports getting users by ID, so:
```
>>> find_obj = api_objects.User(id=1)
>>> result_obj = adapter.cmd_get(find_obj)
>>> admin_user = result_obj()
>>> print(admin_user)
User(id=1, name='Administrator', display_name=None)
```

#### Adding a user

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Establish a user object with a name and add it:
```
>>> add_obj = api_objects.User(name="test_add_1234")
>>> result_obj = adapter.cmd_add(obj=add_obj)
>>> new_user = result_obj()
>>> print(new_user)
User(id=838, name='test_add_1234', display_name=None)
```

#### Modifying a user

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Get the user, change the display name, and save it:
```
>>> find_obj = api_objects.UserList()
>>> result_obj = adapter.cmd_get(obj=find_obj)
>>> all_users = result_obj()
>>> user_obj = all_users.get_item_by_attr(value="test_add_1234", attr="name")
>>> print(user_obj)
User(id=838, name='test_add_1234', display_name=None)
>>> user_obj.display_name = "tantrum testing user"
>>> result_obj = adapter.cmd_update(obj=user_obj)
>>> user_obj_updated = result_obj()
>>> print(user_obj_updated)
User(id=838, name='test_add_1234', display_name='tantrum testing user')
```

### Fun with clients

Clients is the same as the Administration -> System Status page from the GUI.

#### Get all clients with no paging and no filters

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Use the Clients workflow to get all clients with paging disabled and no filter:
```
>>> clients = tantrum.workflows.Clients.get_all(adapter=adapter, cache_paging=0)
>>> print(clients)
tantrum.workflows.Clients(count=3)
>>> print(clients.obj)
SystemStatusList(aggregate=SystemStatusAggregate(send_forward_count=1, send_backward_count=1, send_none_count=0, send_ok_count=1, receive_forward_count=1, receive_backward_count=1, receive_none_count=0, receive_ok_count=1, slowlink_count=0, blocked_count=0, leader_count=2, normal_count=1, registered_with_tls_count=0, versions=VersionAggregateList() with 2 VersionAggregate objects), cache_info=CacheInfo(expiration='2019-06-05T11:44:23')) with 3 ClientStatus objects
>>> for i in clients.obj:
...   print(i)
...
```

### Get all clients with paging but no filter

This will get clients 1 at a time, then return an object that has all of the clients returned. Don't do this :) You should usually get clients at something like 1000 at a time (which is the default if you don't supply cache_paging as an argument).

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Use the Clients workflow to get all clients with cache_paging set a number:
```
>>> clients = tantrum.workflows.Clients.get_all(adapter=adapter, cache_paging=1)
>>> print(clients)
tantrum.workflows.Clients(count=3)
```

### Get all clients with a filter

Load up tantrum_shell:
```
pipenv run python3 -i tantrum_shell.py
```

Use the Clients workflow to get all clients that have registered in the last 5 minutes:
```
>>> filters = tantrum.workflows.Clients.build_last_reg_filter(
...     adapter=adapter, last_reg=300, operator="greaterequal", not_flag=False
... )
>>> print(filters)
CacheFilterList() with 1 CacheFilter objects
>>> clients = tantrum.workflows.Clients.get_all(adapter=adapter, filters=filters)
>>> print(clients)
tantrum.workflows.Clients(count=3)
```

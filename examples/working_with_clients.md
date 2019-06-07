# Fun with clients

Clients is the same as the Administration -> System Status page from the GUI.

For all of these examples, load up tantrum_shell:

```
pipenv run python3 -i tantrum_shell.py
```

## Get all clients with no paging and no filters

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

## Get all clients with paging but no filter

This will get clients 1 at a time, then return an object that has all of the clients returned. Don't do this :) You should usually get clients at something like 1000 at a time (which is the default if you don't supply cache_paging as an argument).

Use the Clients workflow to get all clients with cache_paging set a number:
```
>>> clients = tantrum.workflows.Clients.get_all(adapter=adapter, cache_paging=1)
>>> print(clients)
tantrum.workflows.Clients(count=3)
```

# Get all clients with a filter

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

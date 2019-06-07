# Fun with clients

Clients is the same as the Administration -> System Status page from the GUI.

For all of these examples, load up [tantrum_shell](connection_basics.md).

## Get all clients with no paging and no filters

Use the Clients workflow to get all clients with paging disabled and no filter:
```
clients = tantrum.workflows.Clients.get_all(adapter=adapter, paging=0)
```

clients looks like:
```
>>> clients
tantrum.workflows.Clients(count=3)
>>> print(clients.obj)
SystemStatusList(aggregate=SystemStatusAggregate(send_forward_count=1, send_backward_count=1, send_none_count=0, send_ok_count=1, receive_forward_count=1, receive_backward_count=1, receive_none_count=0, receive_ok_count=1, slowlink_count=0, blocked_count=0, leader_count=2, normal_count=1, registered_with_tls_count=0, versions=VersionAggregateList() with 2 VersionAggregate objects), cache_info=CacheInfo(expiration='2019-06-07T14:25:51')) with 3 ClientStatus objects
```

## Get all clients with paging but no filter

This will get clients 1 at a time, then return an object that has all of the clients returned. Don't do this :) You should usually get clients at something like 1000 at a time (which is the default if you don't supply paging as an argument).

Use the Clients workflow to get all clients with paging set a number:
```
clients = tantrum.workflows.Clients.get_all(adapter=adapter, paging=1)
```

# Get all clients with a filter

Create a set of filters that limits the clients return to only those that have a last_registered field in the past 5 minutes:
```
filters = tantrum.workflows.Clients.build_last_reg_filter(
    adapter=adapter, last_reg=300, operator="greaterequal", not_flag=False
)
```

filters looks like:
```
>>> filters
CacheFilterList(filter=["CacheFilter(value='2019-06-07T14:16:14', type='Date')"])
```

Get clients with filters:
```
clients = tantrum.workflows.Clients.get_all(adapter=adapter, filters=filters)
```

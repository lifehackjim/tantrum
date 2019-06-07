
# Fun with users

There are no workflows for working with users as of yet, but you can use the low-level API objects with the adapter directly to do anything you would want to do.

For all of these examples, load up tantrum_shell:

```
pipenv run python3 -i tantrum_shell.py
```

## Getting a user by name

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

## Getting a user by ID

The API supports getting users by ID, so:
```
>>> find_obj = api_objects.User(id=1)
>>> result_obj = adapter.cmd_get(find_obj)
>>> admin_user = result_obj()
>>> print(admin_user)
User(id=1, name='Administrator', display_name=None)
```

## Adding a user

Establish a user object with a name and add it:
```
>>> add_obj = api_objects.User(name="test_add_1234")
>>> result_obj = adapter.cmd_add(obj=add_obj)
>>> new_user = result_obj()
>>> print(new_user)
User(id=838, name='test_add_1234', display_name=None)
```

## Modifying a user

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

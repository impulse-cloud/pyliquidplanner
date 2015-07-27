PyLiquidPlanner
===============

Python wrapper for the Liquid Planner REST API.

The code is inspired by [PyXero](http://github.com/freakboy3742/pyxero), and aims to offer an ORM style of accessing the API.

## Installation

At present, the library is not available in PyPI but can be installed from GitHub:

```
pip install git+git://github.com/impulse-cloud/pyliquidplanner.git
```

Alternatively, if you don't have Git installed:

```
pip install --upgrade https://github.com/impulse-cloud/pyliquidplanner/tarball/master
```

## Quickstart:

In addition to the instructions shown here, you will need to follow the [Liquid Planner API Guide](http://www.liquidplanner.com/assets/api/liquidplanner_API.pdf) and the [Types Documentation](https://app.liquidplanner.com/api/help/types) to see which fields are available.

Use your Liquid Planner login to construct some credentials:

```python
>>> from liquidplanner.auth import BasicCredentials
>>> credentials = BasicCredentials(<email>, <password>)
```

Then create an API instance:

```python
>>> from liquidplanner import LiquidPlanner
>>> lp = LiquidPlanner(credentials)
```

You can then access the various types of entities by name. For example, here is a list of all the projects in your workspace:

```python
>>> projects = lp.projects.all()
>>> for p in projects:
>>>     print p['name']
```

## Workspaces

With the exception of `account` and `workspaces`, all other entities require a workspace to be specified. When instantiated, the API requests a list of available workspaces and defaults to the first returned. You can disable this check by passing the `use_first_workspace` argument.

```python
>>> lp = LiquidPlanner(credentials, use_first_workspace=False)
```

You must then set the API's `workspace_id` manually.

```python
>>> workspaces = lp.workspaces.all()
>>> lp.workspace_id = workspaces[1]['id']
```

## Using the API

The following entities are supported at present:

* Account
* Workspaces
* Clients
* Projects
* Tasks

### Reading

This library wraps the objects returned in a `dict` like object. This is done so that related
items can be accessed via the objects returned (see [Associated Objects](#associated-objects) below). Otherwise the data is returned as-is, except for dates which are converted into Python `datetime.datetime` objects. 

Use `all()` to get a full list of entities.

```python
>>> all_clients = lp.clients.all()
```
Most API options are supported, including:

* `include` - fetch related entities too
* `filters` - filter the list of items returned
* `order` - sort order of results
* `limit` - limit the number of objects returned

Use `get()` to fetch a specific entity by id.

```python
>>> client = lp.clients.get(1234)
```

Most API options are supported, including:

* `include` - fetch related entities too
* `depth` - max depth when fetching tree items

### Creating

Use `create()` to insert a new entity. 

Note: The LiquidPlanner REST API requires the data to be wrapped with the single entity name. For example `{'client': {'name': 'My Client'}}`. This library takes care of the outer part, so you only need to worry about `{'name': 'My Client'}}`.

```python
>>> client = lp.clients.create({'name': 'My Client'})
```

### Updating

Updating records is similar to creating. The record id can either be in the dictionary, or passed as a parameter.

```python
>>> client = lp.clients.update({'name': 'New Client Name', 'id': 1234})
>>> # OR
>>> client = lp.clients.update({'name': 'New Client Name'}, 1234)
```

### Associated Objects

The objects returned by `all()` and `get()` look and behave like Python `dict`s, but have a few properties available that allow access to associated objects. These properties have all the functionality of the main API endpoints.

For example, you can retrieve comments for a given task:

```python
>>> task = lp.tasks.get(1234)
>>> comments = task.comments.all()
```

Or create a comment for a given task:

```python
>>> task = lp.tasks.get(1234)
>>> comment = task.comments.create({"description": "This is my comment"})
```

Updating and deleting works similarly.

Note: This functionality is not available when you use the `include` parameter to make associated objects available for an `all()` or `get()` request. Only the outer object(s) have associated objects available.

## Future

This library is very new and still a work in progress. Some things I would like to support in future include:

* Support for the 'convenience methods' (e.g. assignments, re-ordering)
* Save and retrieve of attachments
* More tests

## Tests

To run the unit tests, run the following from the root directory of the project:

```
$ python setup.py test
```

This is will install any test dependencies (Mock) into your environment and execute the unit tests.

## Contributing

Contributions are most welcome by submitting a pull request. Please try to include test coverage of any new features or bug fixes.

If you have any problems with PyLiquidPlanner, you can [log an issue](http://github.com/impulse-cloud/pyliquidplanner/issues) on GitHub.


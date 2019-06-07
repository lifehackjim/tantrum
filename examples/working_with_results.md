# Poll for question answers to come in

Defaults to waiting for 99% of answers to come in:

```
question.answers_poll(
    poll_pct=99, poll_secs=0, poll_total=0, poll_sleep=5, max_poll_count=0
)
```

# Getting answers

## Get the result data all at once

```
datas = question.answers_get_data(hashes=False)
```

## Get the result data using paging

```
datas = question.answers_get_data_paged(
    page_size=1000,
    max_page_count=0,
    max_row_count=0,
    cache_expiration=900,
    hashes=False,
    sleep=5,
)
```

## Get the result data using server side export to CEF

```
# start the SSE and get an export id
export_id = question.answers_sse_start_cef(leading="", trailing="")

# poll for the SSE to be finished
question.answers_sse_poll(export_id=export_id, poll_sleep=5, max_poll_count=0)

# get the SSE data (since CEF, it will be a string)
data = question.answers_sse_get_data(export_id=export_id, return_dict=False, return_obj=True)
```

## Get the result data using server side export to CSV

```
# start the SSE and get an export id
# can pass flatten=True to have SSE flatten the returned rows
export_id = question.answers_sse_start_csv(flatten=False, headers=True, hashes=False)

# poll for the SSE to be finished
question.answers_sse_poll(export_id=export_id, poll_sleep=5, max_poll_count=0)

# get the SSE data (since CSV, it will be a string)
data = question.answers_sse_get_data(export_id=export_id, return_dict=False, return_obj=True)
```

## Get the result data using server side export to XML

```
# start the SSE and get an export id
export_id = question.answers_sse_start_xml(hashes=False)

# poll for the SSE to be finished
question.answers_sse_poll(export_id=export_id, poll_sleep=5, max_poll_count=0)

# get the SSE data as a raw XML string
data = question.answers_sse_get_data(export_id=export_id, return_dict=False, return_obj=False)

# get the SSE data as a python dict
data = question.answers_sse_get_data(export_id=export_id, return_dict=True, return_obj=False)

# get the SSE data as a tantrum API ResultSet object
data = question.answers_sse_get_data(export_id=export_id, return_dict=False, return_obj=True)
```

# Working with answers

Most all get_data calls return a tantrum API ResultSetList object, and the first ResultSet object is the only one. 
## Serialize into dict

```
data = datas[0]
data_ser = data.serialize()
```

## Serialize into json

```
data = datas[0]
data_ser = data_serialize_json()
```

## Python magic

You can iterate over the rows and get a dict of column:values for each row:

```
data = datas[0]
for row in data.rows:
    row_values = row.get_values()
    # row_values like: {'Computer Name': ['monkey'], 'Count': ['1']}
```

# Fun with parsed questions

You can ask the API to parse some text into a question using the ParsedQuestion workflow.

For the most part, if you use question text produced by the question parser or builder in the GUI, it will be an exact match to a parser result. This workflow will automatically use that result if no specific index is provided.

## Simple query

```
text = "computer name and ip address and Running Applications"
parsed = tantrum.workflows.ParsedQuestion.parse(adapter=adapter, text=text, lvl="debug")
```

parsed looks like:
```
>>> parsed
tantrum.workflows.ParsedQuestion(parse matches: 1, has exact match: True)
```


Let the workflow pick the exact match, ask it, and return the asked question as a Question workflow:
```
question = parsed.pick(index=None, use_exact_match=True, use_first=False)
```

question looks like:
```
>>> question
tantrum.workflows.Question(
  id='55204',
  query_text='Get Computer Name and IP Address and Running Applications from all machines',
  expiration='2019-06-07 13:20:40',
  expire_in='0:09:53.133480',
  expire_ago='0:00:00',
  expired='False',
)
```

See [Working with results](working_with_results.md) to poll for/get answers on a question workflow.

## Parsing query with parameters

Any query that has parameters will never be an exact match. 

```
text = "Get Computer ID and Computer Name and Application Crashes in Last X Days[5] from all machines"
parsed = tantrum.workflows.ParsedQuestion.parse(adapter=adapter, text=text, lvl="debug")
```

parsed looks like:
```
>>> parsed
tantrum.workflows.ParsedQuestion(parse matches: 2, has exact match: False)
```

If we use parsed.pick() with the defaults, it will throw an exception:
```
>>> question = parsed.pick(index=None, use_exact_match=True, use_first=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/gh/tantrum/tantrum/workflows/__init__.py", line 1532, in pick
    raise exceptions.ModuleError(err)
tantrum.workflows.exceptions.ModuleError: No index supplied, no exact matching parsed result, and use_first is False!
Supply an index of a parsed result:
  index: 0, result: 'Get Computer ID and Computer Name and "Application Crashes in Last X Days" from all machines', params: [5], exact: False
  index: 1, result: 'Get Computer ID and Computer Name and "Number of Application Crashes in Last X Days" from all machines', params: [5], exact: False
```

So either supply use_first=True, or index=N

```
question = parsed.pick(index=None, use_exact_match=True, use_first=True)
```

question looks like:
```
>>> question
tantrum.workflows.Question(
  id='55212',
  query_text='Get Computer ID and Computer Name and Application Crashes in Last X Days[5] from all machines',
  expiration='2019-06-07 13:35:39',
  expire_in='0:09:34.417945',
  expire_ago='0:00:00',
  expired='False',
)
```

See [Working with results](working_with_results.md) to poll for/get answers on a question workflow.

## Even more complex question text

This was built by the question builder in the GUI. It's got a lot of parameters on the left, and it has some right hand filters as well, with some of the right hand filters using parameters.

```
text = 'Get Computer ID and Computer Name and Application Crashes in Last X Days[5] and High Memory Processes[3] and Deploy - Deployments Statuses[22,66] from all machines with ( Application Crashes in Last X Days[51] contains ":Process" and High Memory Processes[3] contains 3 and Computer Name contains eaf )'
parsed = tantrum.workflows.ParsedQuestion.parse(adapter=adapter, text=text, lvl="debug")
```

parsed looks like:
```
>>> parsed
tantrum.workflows.ParsedQuestion(parse matches: 2, has exact match: False)
```

parsed.result_indexes looks like:
```
>>> print(parsed.result_indexes)
  index: 0, result: 'Get Computer ID and Computer Name and "Application Crashes in Last X Days" and High Memory Processes and Deploy - Deployments Statuses from all machines with ( "Application Crashes in Last X Days" contains ":Process" ) and ( High Memory Processes contains 3 ) and ( Computer Name contains eaf )', params: [5, 3, 22, 66, 51, 3], exact: False
  index: 1, result: 'Get Computer ID and Computer Name and "Number of Application Crashes in Last X Days" and High Memory Processes and Deploy - Deployments Statuses from all machines with ( "Application Crashes in Last X Days" contains ":Process" ) and ( High Memory Processes contains 3 ) and ( Computer Name contains eaf )', params: [5, 3, 22, 66, 51, 3], exact: False
```

Pick the first parse result:
```
question = parsed.pick(index=None, use_exact_match=True, use_first=True)
```

question looks like:
```
>>> question
tantrum.workflows.Question(
  id='55215',
  query_text='Get Computer ID and Computer Name and Application Crashes in Last X Days[5] and High Memory Processes[3] and Deploy - Deployments Statuses[22,66] from all machines with ( Application Crashes in Last X Days[51] contains ":Process" and High Memory Processes[3] contains 3 and Computer Name contains eaf )',
  expiration='2019-06-07 13:41:30',
  expire_in='0:09:47.885503',
  expire_ago='0:00:00',
  expired='False',
)
```

See [Working with results](working_with_results.md) to poll for/get answers on a question workflow.

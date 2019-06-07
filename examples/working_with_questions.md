# Fun with questions

You can use the Question workflow to manually build a fairly limited question right now. It only supports adding sensors to the left hand side of the question. The right hand side will come later.

## create a new question workflow

```
question = tantrum.workflows.Question.new(adapter=adapter, lvl="debug")
```

## Get sensors and add to question

Do this for as many sensors as you want to include on the left hand side of the question.

### get a sensor workflow by sensor name

```
sensor = tantrum.workflows.Sensor.get_by_name(adapter=adapter, name="Computer Name")
```

### Set sensor parameters

Check if any parameters are defined:

```
sensor.params_defined
```

If so, set them:

```
sensor.set_parameter(key="parameter key", value="whatever")
```

### Set sensor filter

If you want to filter this sensors column values:

```
sensor.set_filter(
    value=".*FINANCE.*",
    operator="regex",
    ignore_case_flag=True,
    not_flag=False,
    all_values_flag=False,
    max_age_seconds=0,
    type=None,
)
```

### add the sensor to the left hand side of the question

```
question.add_left_sensor(
    sensor=sensor, set_param_defaults=True, allow_empty_params=False
)
```

## ask the question

```
question.ask()
```

## Poll for or get answers

See [Working with results](working_with_results.md)

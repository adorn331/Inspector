# Inspector
a Inspector that can check if your input data is valid according to the schema given.


## usage
give the shema (which is a dict) of the requirement of the data,
the format should be like:
```python
rule = {
    'name': {
        'required': {
            'error_code': 1,
            'alert': 'name is required'
        },
        'type': {
            'error_code': 2,
            'alert': 'name must be a str!!',
            'type': 'str'
        },
        'regex': {
            'error_code': 3,
            'alert': 'name regex fail',
            'pattern': 'abc*'
        },
        'range': {
            'error_code': 4,
            'alert': 'length of name out of range!',
            'max': 10,
            'min': 5
        }
    },
    'age': {
        'required': {
            'error_code': 5,
            'alert': 'age is required'
        },
        'type': {
            'error_code': 6,
            'alert': 'age must be a int!!',
            'type': 'int'
        },
        'range':{
            'error_code': 7,
            'alert': 'age out of range!!',
            'max': 30
        }
    }
}
```
NOTE:for each require item, the 'error_code' ,'alert' and specific feature like('pattern' for 'regex' requirement)
are necessary, else it will raise the schema error.


then use `inspector.parse_schema` to parse the schema into the `Inspector` object
like
`inspector = inspector.parse_schema(rule)`
then give check the input data:
```python
data = {
    'name': 'abcccccc',
    'age': 99,
    'other_data1': '111',
    'other_data2': '222',
    'other_data3': '333'
}

try:
  inspector.inspect(data)
 except Excpetion as e:
  YOUR_ERROR_HANDLE()
```
if there the input data do not fit in with the schema, it will raise the specific error defined in error.py.

NOTE: if you want the inspector not to raise error driectly when  checking data later,
use the param:
```python
inspector = inspector.parse_schema(rule, raise_error=False)
error_list = inspector.inspect(data).error()
```
`inspector.inspect(data).error()` will return a list of all error appear in input data.



## How to extend
the module only support checking regex/type/reuqired option now, but it's easy to extend
you can follow the following steps:
1. add your new error type in error.py
2. add your parse rule for new require item in parse_schema(), you have a guide here to imitate
3. define what is on error in PropertyValidder.is_valid(), you alse have a guide here to imitate
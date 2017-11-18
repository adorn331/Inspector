import newinspector

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
            'pattern': 'abc'
        },
    },
    'age': {
        'required': {
            'error_code': 4,
            'alert': 'age is required'
        },
        'type': {
            'error_code': 5,
            'alert': 'age must be a int!!',
            'type': 'int'
        },
    }
}

data = {
    'name': 'chui*&',
    'age': '16',
    'other_data1': '111',
    'other_data2': '222',
    'other_data3': '333'
}


#raise the frist error capture
inspector = newinspector.parse_schema(rule)
inspector.inspect(data)

#not raise error version: just return the error list

# inspector = newinspector.parse_schema(rule, False)
# print(inspector.inspect(data).error())
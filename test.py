import inspector

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
            'max': 30,
        }
    }
}

data = {
    'name': 'abcccccc',
    'age': 99,
    'other_data1': '111',
    'other_data2': '222',
    'other_data3': '333'
}


#aise error version: raise the frist captured error

inspector = inspector.parse_schema(rule)
inspector.inspect(data)

#not raise error version: just return the error list

# inspector = inspector.parse_schema(rule, False)
# print(inspector.inspect(data).error())
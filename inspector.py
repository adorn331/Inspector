import error
import re

INSPECT_ITEMS = ('required', 'regex', 'type', 'range')  # the support inspect item in schema


class PropertyValidder(object):
    """Represent the standard of a specific property,
            which can valid the input specific property and raise corresponding error.
    """

    def __init__(self, name, feature_mapping, error_mapping):
        """
        :param
            - name: specific name of the property.
            - feature_mapping: contain the require_item's detail description
            - error_mapping:  specific error to be raised when given data not fitting feature.
        """
        self.name = name
        self.feature_mapping = feature_mapping
        self.error_mapping = error_mapping
        self.valid_errors = []

    def is_valid(self, value):
        """
        :param
            - value: the input specific property

        :return
            True if the input specific property is valid

        :note
            If a given data not fitting required features, the error will store in self.valid_errors instand of raise it.
        """
        valid = True
        for require_item, require_detail in self.feature_mapping.items():

            if require_item == 'type':
                data_type = eval(require_detail)
                if not isinstance(value, data_type):
                    self.valid_errors.append(self.error_mapping['type'])
                    valid = False

            if require_item == 'regex':
                pattern = require_detail
                if not isinstance(value, str) or not re.match(pattern, value):
                    self.valid_errors.append(self.error_mapping['regex'])
                    valid = False

            """=============== extend here========================
                you can extend new require_item like:

                if require_item == 'YOUR_REQUIRED_ITEM':
                    YOUR_REQUIRED_ITEM_FEATURE = require_detail
                    if not FIT YOUR EQUIRED_ITEM_FEATURE:
                        self.valid_errors.append(self.error_mapping['regex'])
                        valid = False
            """

            # can validate the range of int or length of str.
            if require_item == 'range':
                maximum = require_detail['max']
                minimum = require_detail['min']
                if isinstance(value, str):
                    if not minimum < len(value) < maximum:
                        self.valid_errors.append(self.error_mapping['range'])
                        valid = False
                if isinstance(value, int):
                    if not minimum < value < maximum:
                        self.valid_errors.append(self.error_mapping['range'])
                        valid = False

        return valid


class Inspector(object):
    """Inspector can inspect if the input data are valid
        refers to the PropertyValidders given
    """

    def __init__(self, inspect_properties=[], raise_error=True):
        """
        :param
            - inspect_properties: the list of PropertyValidder, which are the property need to inpect according to schema
            - raise_error: decide the Inspector whether to raise the error or store all errors in a list
        """
        self.inspect_properties = inspect_properties
        self.raise_error = raise_error
        self._errors = []

    def inspect(self, data):
        """
        :param
            - data: the input data to be inpect refers to schema rule.

        :note
            If decide not to raise error, all errors will be store in self._errors,
                                                    which is available by self.error()
            or first met error will be raised.
        """
        # to check if all the "required" property are in data
        for required_property in filter(lambda x: x.error_mapping.get('required', None), self.inspect_properties):
            if required_property.name not in data:
                raise required_property.error_mapping['required']

        for key, value in data.items():
            if key in map(lambda x: x.name, self.inspect_properties):
                inspected_property = next(x for x in self.inspect_properties if x.name == key)
                if not inspected_property.is_valid(value):
                    self._errors += inspected_property.valid_errors
                    if self.raise_error:  # need to raise error.
                        raise inspected_property.valid_errors[0]

        return self

    def error(self):
        return self._errors


def parse_schema(schema, raise_error=True):
    """Parse the schema into a list of PropertyValidder.

        :param
        - schema: schema given by user, which is a dict
        - raise_error: decide the Inspector whether to raise the error or store all errors in a list

        :return
            a Inspector can inspect the data obey the rule defined by schema
    """
    inpsect_properties = []

    for property_name, requirements in schema.items():
        error_mapping = {}
        feature_mapping = {}
        for require_item, require_detail in requirements.items():
            # check if the inspect items in schema are supported
            if require_item not in INSPECT_ITEMS:
                raise error.SchemaError('Not support the option: %s now' % require_item, -1)  # 不在支持验证选项中

            # get the error code and alert of the specific require_item,
            # add to the feature mapping of this PropertyValidder's error_mapping
            try:
                err_statu = require_detail['error_code']
                err_msg = require_detail['alert']
            except Exception:
                raise error.SchemaError("at '%s' config" % require_item, -1)

            # get the detail requirement of the specific require_item,
            # add to the feature mapping of this PropertyValidder's feature_mapping
            if require_item == 'required':
                error_mapping['required'] = error.MissingError(err_statu, err_msg)

            if require_item == 'regex':
                try:
                    pattern = require_detail['pattern']
                except Exception:
                    raise error.SchemaError("at 'regex' config", -1)
                error_mapping['regex'] = error.RegexError(err_statu, err_msg, pattern)
                feature_mapping['regex'] = pattern

            if require_item == 'type':
                try:
                    data_type = require_detail['type']
                except Exception:
                    raise error.SchemaError("at 'type' config", -1)
                error_mapping['type'] = error.TypeError(err_statu, err_msg, data_type)
                feature_mapping['type'] = data_type

            """"=================extend here like===========================
                extend new require item like:

                if require_item == 'YOUR_REQUIRE_ITEM':
                    try:
                        data_type = require_detail['YOUR_REQUIRE_ITEM']
                    except Exception:
                        raise error.SchemaError("at 'YOUR_REQUIRE_ITEM' config", -1)
                    error_mapping['type'] = error.YOURERROR(err_statu, err_msg)
                    feature_mapping['YOUR_REQUIRE_ITEM'] = YOUR_REQUIRE_ITEM_FEATURE
            """
            # can validate the range of int or length of str.
            # support only given min or max. the default value is 0 and infinite
            if require_item == 'range':
                maximum = require_detail.get('max', None)
                minimum = require_detail.get('min', None)
                if not maximum and not minimum:  # neither set max nor min, raise schema error
                    raise error.SchemaError("at 'range' config", -1)
                if not maximum:
                    maximum = float('inf')
                if not minimum:
                    minimum = 0
                error_mapping['range'] = error.RangeError(err_statu, err_msg, maximum, minimum)
                feature_mapping['range'] = {'max': maximum, 'min': minimum}

        inpsect_properties.append(PropertyValidder(property_name, feature_mapping, error_mapping))

    return Inspector(inpsect_properties, raise_error)
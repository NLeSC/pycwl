from .recognizer_test_loader import run_recognizer

from pycwl.parser.v2_0.recognizers.common import has_key, get_by_key
from pycwl.parser.v2_0.recognizers.custom_types import *

import pytest

def test_recognize_array_type_description():
    test_data = '''
            itemType: string
            '''
    result = run_recognizer(recognize_array_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!ArrayTypeDescription'

    assert has_key(result, 'itemType')
    assert get_by_key(result, 'itemType').value == 'string'

def test_recognize_enum_type_descriptino():
    test_data = '''
            symbols:
                - red
                - green
                - blue
            '''
    result = run_recognizer(recognize_enum_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!EnumTypeDescription'

    assert has_key(result, 'symbols')
    symbols = get_by_key(result, 'symbols').value

    assert isinstance(symbols[0], yaml.ScalarNode)
    assert symbols[0].value == 'red'
    assert symbols[1].value == 'green'
    assert symbols[2].value == 'blue'

def test_recognize_enum_type_description_2():
    test_data = '''
            symbols:
                red: 1
                green: 2
                blue: 3
            '''
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_enum_type_description, test_data)

def test_recognize_record_type_description():
    test_data = '''
            record:
                - name: field1
                  type: int
                - name: field2
                  type: string
            '''
    result = run_recognizer(recognize_record_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordTypeDescription'

    assert has_key(result, 'fields')
    fields = get_by_key(result, 'fields').value

    assert isinstance(fields[0], yaml.MappingNode)
    assert get_by_key(fields[0], 'name').value == 'field1'
    assert get_by_key(fields[0], 'type').value == 'int'
    assert get_by_key(fields[1], 'name').value == 'field2'
    assert get_by_key(fields[1], 'type').value == 'string'

def test_recognize_record_type_description_2():
    test_data = '''
            fields:
                - name: field1
            '''
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_record_type_description, test_data)

def test_recognize_record_type_description_3():
    test_data = '''
            record:
                field1:
                    type: int
                field2:
                    type: string
            '''
    result = run_recognizer(recognize_record_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordTypeDescription'

    assert has_key(result, 'fields')
    fields = get_by_key(result, 'fields').value

    assert isinstance(fields[0], yaml.MappingNode)
    assert get_by_key(fields[0], 'name').value == 'field1'
    assert get_by_key(fields[0], 'type').value == 'int'
    assert get_by_key(fields[1], 'name').value == 'field2'
    assert get_by_key(fields[1], 'type').value == 'string'

def test_recognize_record_field_description():
    test_data = '''
            name: field1
            type: int
            '''
    result = run_recognizer(recognize_record_field_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordFieldDescription'

    assert has_key(result, 'name')
    assert get_by_key(result, 'name').value == 'field1'

    assert has_key(result, 'type')
    assert get_by_key(result, 'type').value == 'int'

def test_recognize_record_field_description_2():
    test_data = '''
            doc: A test field for testing
            name: field1
            type: int
            '''
    result = run_recognizer(recognize_record_field_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordFieldDescription'

    assert has_key(result, 'doc')
    assert get_by_key(result, 'doc').value == 'A test field for testing'

    assert has_key(result, 'name')
    assert get_by_key(result, 'name').value == 'field1'

    assert has_key(result, 'type')
    assert get_by_key(result, 'type').value == 'int'

def test_recognize_record_field_description_3():
    test_data = '''
            name: field1
            '''
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_record_field_description, test_data)

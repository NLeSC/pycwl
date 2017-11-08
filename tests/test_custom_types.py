from .recognizer_test_loader import run_recognizer

from pycwl.parser.v2_0.recognizers.common import has_key, get_by_key
from pycwl.parser.v2_0.recognizers.custom_types import *

import pytest

def test_recognize_type_definition():
    test_data = '''
            name: png_file
            description:
                format: http://example.com/file_types/png
                streamable: true
            '''
    result = run_recognizer(recognize_type_definition, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!TypeDefinition'
    assert get_by_key(result, 'name').value == 'png_file'
    description = get_by_key(result, 'description')

    assert isinstance(description, yaml.MappingNode)
    assert description.tag == '!FileTypeDescription'

def test_recognize_type_definition_2():
    test_data = '''
            name: StringArray
            descriptin:
                arrayOf: string
            '''
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_type_definition, test_data)

def test_recognize_type_description():
    test_data = '''
            doc: A description of the PNG file format
            format: http://example.com/filetypes/png
            streamable: true
            '''
    result = run_recognizer(recognize_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!FileTypeDescription'
    assert get_by_key(result, 'doc').value == 'A description of the PNG file format'
    assert get_by_key(result, 'format').value == 'http://example.com/filetypes/png'
    assert get_by_key(result, 'streamable').value == True

def test_recognize_type_description_2():
    test_data = '''
            arrayOf: int
            '''
    result = run_recognizer(recognize_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!ArrayTypeDescription'

    assert has_key(result, 'doc')
    assert get_by_key(result, 'doc').value == ''
    assert has_key(result, 'itemType')
    assert get_by_key(result, 'itemType').value == 'int'

def test_recognize_type_description_3():
    test_data = '''
            symbols:
                - red
                - green
                - blue
            '''
    result = run_recognizer(recognize_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!EnumTypeDescription'

    assert has_key(result, 'symbols')
    symbols = get_by_key(result, 'symbols').value

    assert isinstance(symbols[0], yaml.ScalarNode)
    assert symbols[0].value == 'red'
    assert symbols[1].value == 'green'
    assert symbols[2].value == 'blue'

def test_recognize_type_description_4():
    test_data = '''
            record:
                - name: field1
                  type: bool
                - name: field2
                  type: float
            '''
    result = run_recognizer(recognize_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordTypeDescription'

    assert has_key(result, 'fields')
    fields = get_by_key(result, 'fields').value

    assert isinstance(fields[0], yaml.MappingNode)
    assert get_by_key(fields[0], 'name').value == 'field1'
    assert get_by_key(fields[0], 'type').value == 'bool'
    assert get_by_key(fields[1], 'name').value == 'field2'
    assert get_by_key(fields[1], 'type').value == 'float'

def test_recognize_type_description_5():
    test_data = '''
            not_a_type_description: 13
            '''
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_type_description, test_data)

def test_recognize_type_description_6():
    test_data = '''
            record:
              - name: field1
                type:
                  symbols:
                    - red
                    - green
                    - blue
              - name: field2
                type: float
              - name: field3
                type:
                  arrayOf: int
            '''
    result = run_recognizer(recognize_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!RecordTypeDescription'

    defs = get_by_key(result, 'fields')
    assert isinstance(defs, yaml.SequenceNode)

    field1 = get_by_index(defs, 0)
    assert get_by_key(field1, 'name').value == 'field1'
    field1_type = get_by_key(field1, 'type')
    field1_symbols = get_by_key(field1_type, 'symbols')
    assert get_by_index(field1_symbols, 0).value == 'red'
    assert get_by_index(field1_symbols, 1).value == 'green'
    assert get_by_index(field1_symbols, 2).value == 'blue'

    field2 = get_by_index(defs, 1)
    assert get_by_key(field2, 'name').value == 'field2'
    assert get_by_key(field2, 'type').tag == '!Type'

    field3 = get_by_index(defs, 2)
    assert get_by_key(field3, 'name').value == 'field3'
    field3_type = get_by_key(field3, 'type')
    assert field3_type.tag == '!ArrayTypeDescription'

    assert get_by_key(field3_type, 'itemType').tag == '!Type'
    assert get_by_key(field3_type, 'itemType').value == 'int'

def test_recognize_file_type_description():
    test_data = '''
            format: http://example.com/filetypes/png
            '''
    result = run_recognizer(recognize_file_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!FileTypeDescription'
    assert get_by_key(result, 'format').value == 'http://example.com/filetypes/png'
    assert get_by_key(result, 'streamable').value == False

def test_recognize_file_type_description_2():
    test_data = '''
            format: http://example.com/filetypes/png
            streamable: false
            '''
    result = run_recognizer(recognize_file_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!FileTypeDescription'
    assert get_by_key(result, 'format').value == 'http://example.com/filetypes/png'
    assert get_by_key(result, 'streamable').value == False

def test_recognize_file_type_description_3():
    test_data = '''
            format: http://example.com/filetypes/png
            streamable: 10
            '''
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_file_type_description, test_data)

def test_recognize_array_type_description():
    test_data = '''
            arrayOf: string
            '''
    result = run_recognizer(recognize_array_type_description, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!ArrayTypeDescription'

    assert has_key(result, 'itemType')
    assert get_by_key(result, 'itemType').value == 'string'

def test_recognize_enum_type_description():
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

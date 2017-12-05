import pytest
import yaml

from .recognizer_test_loader import run_recognizer

from pycwl.parser.experimental.recognizers.common import has_key
from pycwl.parser.experimental.recognizers.common import get_by_index
from pycwl.parser.experimental.recognizers.common import get_by_key
from pycwl.parser.experimental.recognizers.processes import *

def test_recognize_parameter():
    test_data = '''
            id: in_file
            '''
    result = run_recognizer(recognize_parameter, test_data, 'InputParameter')

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!InputParameter'

    assert has_key(result, 'id')
    assert get_by_key(result, 'id').value == 'in_file'
    assert has_key(result, 'label')
    assert get_by_key(result, 'label').value == ''
    assert get_by_key(result, 'doc').value == ''
    assert get_by_key(result, 'type') is None

def test_recognize_parameter_2():
    test_data = '''
            id: in_file
            label: The input file to process
            doc: This parameter describes an input file to be processed.
            type:
                format: http://example.com/files/png
            streamable: true
            '''
    result = run_recognizer(recognize_parameter, test_data, 'InputParameter')

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!InputParameter'

    assert get_by_key(result, 'id').value == 'in_file'
    assert get_by_key(result, 'label').value == 'The input file to process'
    assert get_by_key(result, 'doc').value == 'This parameter describes an input file to be processed.'
    assert get_by_key(result, 'type').tag == '!FileTypeDescription'
    assert get_by_key(result, 'streamable').value == True

def test_recognize_parameter_3():
    test_data = '''
            id: out_file
            label: The output file produced
            doc: This parameter describes an output file that is produced.
            type:
                format: http://example.com/files/png
            streamable: false
            '''
    result = run_recognizer(recognize_parameter, test_data, 'OutputParameter')

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!OutputParameter'

    assert get_by_key(result, 'id').value == 'out_file'
    assert get_by_key(result, 'label').value == 'The output file produced'
    assert get_by_key(result, 'doc').value == 'This parameter describes an output file that is produced.'
    assert get_by_key(result, 'type').tag == '!FileTypeDescription'
    assert get_by_key(result, 'streamable').value == False

def test_recognize_inputs():
    test_data = '''
            - id: in1
              type: int
            - id: in2
              type: str
              default: Test
    '''
    result = run_recognizer(recognize_inputs, test_data)
    in1 = get_by_index(result, 0)
    assert in1.tag == '!InputParameter'
    assert get_by_key(in1, 'id').value == 'in1'
    in2 = get_by_index(result, 1)
    assert get_by_key(in2, 'type').value == 'str'
    assert get_by_key(in2, 'default').tag == '!ConstantExpression'

def test_recognize_inputs_2():
    test_data = '''
            in1: int
            in2: str
    '''
    result = run_recognizer(recognize_inputs, test_data)
    in1 = get_by_index(result, 0)
    assert in1.tag == '!InputParameter'
    assert get_by_key(in1, 'id').value == 'in1'
    assert get_by_key(in1, 'type').value == 'int'
    in2 = get_by_index(result, 1)
    assert get_by_key(in2, 'id').value == 'in2'
    assert get_by_key(in2, 'type').value == 'str'

def test_recognize_inputs_3():
    test_data = '''
            in1:
                format: http://example.com/files/png
                streamable: false
            in2: str
    '''
    result = run_recognizer(recognize_inputs, test_data)
    in1 = get_by_index(result, 0)
    assert in1.tag == '!InputParameter'
    assert get_by_key(in1, 'id').value == 'in1'
    assert get_by_key(in1, 'type').tag == '!FileTypeDescription'
    in2 = get_by_index(result, 1)
    assert get_by_key(in2, 'id').value == 'in2'
    assert get_by_key(in2, 'type').value == 'str'

def test_recognize_outputs():
    test_data = '''
            - id: out1
              type: int
            - id: out2
              type: str
    '''
    result = run_recognizer(recognize_outputs, test_data)
    out1 = get_by_index(result, 0)
    assert out1.tag == '!OutputParameter'
    assert get_by_key(out1, 'id').value == 'out1'
    out2 = get_by_index(result, 1)
    assert get_by_key(out2, 'type').value == 'str'


def test_recognize_outputs_2():
    test_data = '''
            out1: int
            out2: str
    '''
    result = run_recognizer(recognize_outputs, test_data)
    out1 = get_by_index(result, 0)
    assert out1.tag == '!OutputParameter'
    assert get_by_key(out1, 'id').value == 'out1'
    out2 = get_by_index(result, 1)
    assert get_by_key(out2, 'type').value == 'str'


def test_recognize_process_description():
    # This is missing extensions, should figure out what to do with them
    test_data = '''
            id: test_process
            label: This is a process for testing
            doc: Here is some documentation for this process
            inputs:
              in1: str
              in2: File
            outputs:
              out1: str
              out2: File
            results:
              out1: $(inputs.in1)
              out2: $(inputs.in2)
    '''
    result = run_recognizer(recognize_process_description, test_data)
    assert result.tag == '!ExpressionTool'
    assert get_by_key(result, 'id').value == 'test_process'
    assert get_by_key(result, 'label').value == 'This is a process for testing'
    assert get_by_key(result, 'doc').value == \
            'Here is some documentation for this process'

    inputs = get_by_key(result, 'inputs')
    assert isinstance(inputs, yaml.SequenceNode)
    in1 = get_by_index(inputs, 0)
    assert get_by_key(in1, 'id').value == 'in1'
    assert get_by_key(in1, 'type').value == 'str'
    in2 = get_by_index(inputs, 1)
    assert get_by_key(in2, 'id').value == 'in2'
    assert get_by_key(in2, 'type').value == 'File'

    outputs = get_by_key(result, 'outputs')
    assert isinstance(outputs, yaml.SequenceNode)
    out1 = get_by_index(outputs, 0)
    assert get_by_key(out1, 'id').value == 'out1'
    assert get_by_key(out1, 'type').value == 'str'
    out2 = get_by_index(outputs, 1)
    assert get_by_key(out2, 'id').value == 'out2'
    assert get_by_key(out2, 'type').value == 'File'

    results = get_by_key(result, 'results')
    assert isinstance(results, yaml.MappingNode)
    assert results.tag == 'tag:yaml.org,2002:map'
    out1 = results.value[0]
    assert out1[0].value == 'out1'
    assert out1[1].tag == '!ReferenceExpression'
    assert len(get_by_key(out1[1], 'selectors').value) == 2

    out2 = results.value[1]
    assert out2[0].value == 'out2'
    assert out2[1].tag == '!ReferenceExpression'
    assert len(get_by_key(out2[1], 'selectors').value) == 2



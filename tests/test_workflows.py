import pytest
import yaml

from .recognizer_test_loader import run_recognizer

from pycwl.parser.experimental.recognizers.common import has_key
from pycwl.parser.experimental.recognizers.common import get_by_index
from pycwl.parser.experimental.recognizers.common import get_by_key
from pycwl.parser.experimental.recognizers.workflows import *

def test_recognize_connection():
    test_data = '''
            id: input1
            default: bla
            valueFrom: $(inputs.in1)
    '''
    result = run_recognizer(recognize_connection, test_data)
    assert result.tag == '!Connection'

    assert has_key(result, 'id')
    assert get_by_key(result, 'id').value == 'input1'

    assert has_key(result, 'default')
    default = get_by_key(result, 'default')
    assert default.tag == '!ConstantExpression'
    assert get_by_key(default, 'value').value == 'bla'

    assert has_key(result, 'valueFrom')
    value_from = get_by_key(result, 'valueFrom')
    assert value_from.tag == '!ReferenceExpression'
    get_by_key(value_from, 'selectors').value[0] == 'inputs'

def test_recognize_connections():
    test_data = '''
            input1:
              default: bla
            input2: $(inputs.in1)
            input3:
              default: 13
              valueFrom: $(inputs.in2)
    '''
    result = run_recognizer(recognize_connections, test_data)
    assert isinstance(result, yaml.SequenceNode)
    assert len(result.value) == 3

    input1 = get_by_index(result, 0)
    assert get_by_key(input1, 'id').value == 'input1'
    assert get_by_key(input1, 'default').tag == '!ConstantExpression'

    input2 = get_by_index(result, 1)
    assert get_by_key(input2, 'id').value == 'input2'
    assert not has_key(input2, 'default')
    assert get_by_key(input2, 'valueFrom').tag == '!ReferenceExpression'

    input3 = get_by_index(result, 2)
    assert get_by_key(input3, 'id').value == 'input3'
    assert get_by_key(input3, 'default').tag == '!ConstantExpression'
    assert get_by_key(input3, 'valueFrom').tag == '!ReferenceExpression'

def test_recognize_step_outputs():
    test_data = '''
            - out1
            - out2
    '''
    result = run_recognizer(recognize_step_outputs, test_data)
    assert isinstance(result, yaml.SequenceNode)
    assert len(result.value) == 2

    assert get_by_index(result, 0).value == 'out1'
    assert get_by_index(result, 1).value == 'out2'

def test_recognize_process():
    test_data = '''step1'''
    result = run_recognizer(recognize_process, test_data)
    assert isinstance(result, yaml.ScalarNode)
    assert result.tag == 'tag:yaml.org,2002:str'
    assert result.value == 'step1'

def test_recognize_process_2():
    test_data = '''
            id: test_process
            inputs:
              in1: str
            outputs:
              out1: str
            results:
              out1: $(inputs.in1)
    '''
    result = run_recognizer(recognize_process, test_data)
    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!ExpressionTool'

def test_recognize_workflow():
    # This is missing extensions, should figure out what to do with them
    test_data = '''
            id: test_process
            label: This is a process for testing
            doc: Here is some documentation for this process
            inputs:
              in1: str
              in2: File
            outputs:
              out1: File
              out2: File
            steps:
              step1:
                label: This is a test step
                doc: With some documentation
                in:
                  parameter1:
                    default: bla
                    valueFrom: $(inputs.in1)
                out: [output1]
                run: steps/step.cwl
            results:
              out1: $(step1.output1)
              out2: $(inputs.in2)
    '''
    result = run_recognizer(recognize_workflow, test_data)
    assert result.tag == '!Workflow'
    assert has_key(result, 'steps')

    steps = get_by_key(result, 'steps')
    assert isinstance(steps, yaml.SequenceNode)
    assert len(steps.value) == 1

    step1 = steps.value[0]
    assert get_by_key(step1, 'id').value == 'step1'
    assert get_by_key(step1, 'label').value == 'This is a test step'
    assert get_by_key(step1, 'doc').value == 'With some documentation'
    assert has_key(step1, 'in')

    inputs = get_by_key(step1, 'in')
    assert isinstance(inputs, yaml.SequenceNode)
    assert len(inputs.value) == 1

    parameter1 = inputs.value[0]
    assert get_by_key(parameter1, 'id').value == 'parameter1'


import pytest
import yaml

from .recognizer_test_loader import run_recognizer

from pycwl.parser.experimental.recognizers.common import has_key
from pycwl.parser.experimental.recognizers.common import get_by_index
from pycwl.parser.experimental.recognizers.common import get_by_key
from pycwl.parser.experimental.recognizers.expressions import *

def test_recognize_reference_expression():
    test_data = '$(inputs.input_1)'
    result = run_recognizer(recognize_reference_expression, test_data)

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!ReferenceExpression'

    assert has_key(result, 'selectors')
    selectors = get_by_key(result, 'selectors').value

    assert len(selectors) == 2
    assert selectors[0] == 'inputs'
    assert selectors[1] == 'input_1'

def test_recognize_reference_expression_2():
    test_data = 'arbitrary string'
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_reference_expression, test_data)

def test_recognize_reference_expression_3():
    test_data = '10'
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_reference_expression, test_data)

def test_recognize_constant_expression():
    test_data = '10'
    result = run_recognizer(recognize_constant_expression, test_data)
    assert result.tag == '!ConstantExpression'
    assert has_key(result, 'value')
    assert get_by_key(result, 'value').value == '10'

def test_recognize_constant_expression_2():
    test_data = '[10, 20]'
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_constant_expression, test_data)

def test_recognize_merge_expression():
    test_data = '''
        mergeMethod: merge_flattened
        sources: [step1/output1, step2/output2]
    '''
    result = run_recognizer(recognize_expression, test_data)
    assert result.tag == '!MergeExpression'

    assert has_key(result, 'mergeMethod')
    assert get_by_key(result, 'mergeMethod').value == 'merge_flattened'

    assert has_key(result, 'sources')
    sources = get_by_key(result, 'sources')
    assert sources.tag == 'tag:yaml.org,2002:seq'
    assert sources.value[0].value == 'step1/output1'
    assert sources.value[1].value == 'step2/output2'

def test_recognize_merge_expression_2():
    test_data = '''
        mergeMethod: merge_something
        sources: [step1/output1, step2/output2]
    '''
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_merge_expression, test_data)

def test_recognize_file_description():
    test_data = 'file_location: file:///home/user/myfile.txt'
    result = run_recognizer(recognize_file_description, test_data)

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!FileDescription'

    assert has_key(result, 'file_location')
    assert get_by_key(result, 'file_location').value == 'file:///home/user/myfile.txt'

def test_recognize_file_description_2():
    test_data = '''
            file_location: file:///home/user/myfile.txt
            type: text/plain
            secondaryFiles:
                - file_location: file:///home/user/myfile.meta
                  type: metadata
            '''
    result = run_recognizer(recognize_file_description, test_data)

    assert isinstance(result, yaml.MappingNode)
    assert result.tag == '!FileDescription'

    assert has_key(result, 'file_location')
    assert get_by_key(result, 'file_location').value == 'file:///home/user/myfile.txt'

    assert has_key(result, 'type')
    assert get_by_key(result, 'type').value == 'text/plain'

    assert has_key(result, 'secondaryFiles')
    secondary_files = get_by_key(result, 'secondaryFiles').value
    assert len(secondary_files) == 1
    assert get_by_key(secondary_files[0], 'file_location').value == 'file:///home/user/myfile.meta'
    assert get_by_key(secondary_files[0], 'type').value == 'metadata'

def test_recognize_file_description_3():
    test_data = 'dir_location: http://example.com/files'
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_file_description, test_data)

def test_recognize_directory_description():
    test_data = 'dir_location: http://example.com/files'
    result = run_recognizer(recognize_directory_description, test_data)

    assert result.tag == '!DirectoryDescription'
    assert has_key(result, 'dir_location')
    assert get_by_key(result, 'dir_location').value == 'http://example.com/files'

def test_recognize_directory_description_2():
    test_data = 'di_location: http://example.com/file.txt'
    with pytest.raises(RuntimeError):
        run_recognizer(recognize_directory_description, test_data)

def test_recognize_file_constructor():
    test_data = 'file_contents: 42'
    result = run_recognizer(recognize_file_constructor, test_data)

    assert result.tag == '!FileConstructor'
    assert has_key(result, 'file_contents')

    contents = get_by_key(result, 'file_contents')
    assert contents.tag == '!ConstantExpression'
    assert has_key(contents, 'value')
    assert get_by_key(contents, 'value').value == '42'

def test_recognize_file_constructor_2():
    test_data = 'file_content: Hello, World!'
    with pytest.raises(RuntimeError):
        result = run_recognizer(recognize_file_constructor, test_data)

def test_recognize_file_constructor_3():
    test_data = '''
            file_contents: 42
            extra_attribute: Testing
            '''
    result = run_recognizer(recognize_file_constructor, test_data)

    assert result.tag == '!FileConstructor'
    assert has_key(result, 'file_contents')

    contents = get_by_key(result, 'file_contents')
    assert contents.tag == '!ConstantExpression'
    assert has_key(contents, 'value')
    assert get_by_key(contents, 'value').value == '42'

def test_recognize_directory_constructor():
    test_data = '''
            dir_contents:
                'file.txt':
                    file_location: file:///home/user/myfile.txt
                'file2.txt': $(inputs.input_1)
                'file3.txt':
                    file_contents: $(inputs.input_2)
                subdir:
                    dir_contents:
                        'file4.txt': $(inputs.input_3)
                subdir2: $(inputs.input_4)
            '''
    result = run_recognizer(recognize_directory_constructor, test_data)
    print(result)
    assert result.tag == '!DirectoryConstructor'
    assert has_key(result, 'dir_contents')

    contents = get_by_key(result, 'dir_contents')
    assert has_key(contents, 'file.txt')

    file_txt = get_by_key(contents, 'file.txt')
    assert file_txt.tag == '!FileDescription'

    file2_txt = get_by_key(contents, 'file2.txt')
    assert file2_txt.tag == '!ReferenceExpression'

    file3_txt = get_by_key(contents, 'file3.txt')
    assert file3_txt.tag == '!FileConstructor'

    subdir = get_by_key(contents, 'subdir')
    assert subdir.tag == '!DirectoryConstructor'

    subdir_contents = get_by_key(subdir, 'dir_contents')
    file4_txt = get_by_key(subdir_contents, 'file4.txt')
    assert file4_txt.tag == '!ReferenceExpression'

    subdir2 = get_by_key(contents, 'subdir2')
    assert subdir2.tag == '!ReferenceExpression'

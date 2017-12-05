from .common import *

from .custom_types import recognize_type
from .expressions import recognize_expression

def recognize_parameter(node, imbue):
    """
    Recognize a Parameter, with a preferred subclass.

    A Parameter can be an InputParameter or an OutputParameter, and \
    this is ambiguous. So this function takes a hint as to which type \
    is preferred, based on the context, and will try to imbue this \
    type on the recognised node. If the node is not compatible, then \
    an error is raised.

    Args:
        node (yaml.MappingNode): The node to recognize.
        imbue (str): The name of the subclass to prefer.

    Returns:
        (yaml.MappingNode): The tagged node
    """
    require_keys(node, ['id'])

    set_key_default(node, 'label', '')
    set_key_default(node, 'doc', '')
    if has_key(node, 'type'):
        update_key(node, 'type', recognize_type)
    else:
        set_key_default(node, 'type', None)
    set_key_default(node, 'streamable', False)
    interpret_as_bool(get_by_key(node, 'streamable'))

    if imbue == 'InputParameter':
        node = recognize_input_parameter(node)
    elif imbue == 'OutputParameter':
        node.tag = u'!OutputParameter'
    else:
        raise RuntimeError('Implementation error: Ambiguous Parameter.')

    return node

def recognize_input_parameter(node):
    if has_key(node, 'default'):
        update_key(node, 'default', recognize_expression)
    set_key_default(node, 'default', None)
    node.tag = '!InputParameter'
    return node

def recognize_inputs(node):
    node = pairs_to_sequence(node, 'id', 'type', False)
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a list of inputs'.format(
            node.start_mark, os.linesep))
    update_each_item(node, recognize_parameter, imbue='InputParameter')
    return node

def recognize_outputs(node):
    node = pairs_to_sequence(node, 'id', 'type', False)
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a list of outputs'.format(
            node.start_mark, os.linesep))
    update_each_item(node, recognize_parameter, imbue='OutputParameter')
    return node

def recognize_results(node):
    if not isinstance(node, yaml.MappingNode):
        raise RuntimeError('{}{}Expected a mapping of output names to expressions'.format(
            node.start_mark, os.linesep))

    new_results = []
    for key, value in node.value:
        require_type(key, 'tag:yaml.org,2002:str')
        new_results.append((key, recognize_expression(value)))
    node.value = new_results

    return node

def recognize_process_description(node):
    require_keys(node, ['outputs', 'results'])
    set_key_default(node, 'id', '')
    set_key_default(node, 'label', '')
    set_key_default(node, 'doc', '')
    set_key_default(node, 'inputs', [])
    set_key_default(node, 'extensions', [])

    update_key(node, 'inputs', recognize_inputs)
    update_key(node, 'outputs', recognize_outputs)
    update_key(node, 'results', recognize_results)
    update_key(node, 'extensions', recognize_process_extensions)
    update_key(node, 'results', recognize_results)

    # ExpressionTool is least specific, so match it last
    #node = optionally(recognize_workflow, node)
    #node = optionally(recognize_command_line_tool, node)
    node = optionally(recognize_expression_tool, node)

    # ExpressionTool will always match, no need to check
    return node

def recognize_process_extensions(node):
    # not implemented yet
    return node

def recognize_expression_tool(node):
    # Any process that is not something else is an ExpressionTool
    if isinstance(node, yaml.MappingNode):
            node.tag = u'!ExpressionTool'
    return node


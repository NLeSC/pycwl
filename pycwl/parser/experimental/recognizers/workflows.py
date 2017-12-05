from .common import *

from .expressions import recognize_expression
from .processes import recognize_process_description

def recognize_connection(node):
    require_keys(node, ['id'])
    require_type(get_by_key(node, 'id'), 'tag:yaml.org,2002:str')
    if has_key(node, 'default'):
        update_key(node, 'default', recognize_expression)
    if has_key(node, 'valueFrom'):
        update_key(node, 'valueFrom', recognize_expression)
    node.tag = u'!Connection'
    return node

def recognize_connections(node):
    node = pairs_to_sequence(node, 'id', 'valueFrom', merge_value=True)
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a mapping or list of connections'.format(
                           node.start_mark, os.linesep))
    update_each_item(node, recognize_connection)
    return node

def recognize_step_outputs(node):
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a list of strings with output names'.format(
                           node.start_mark, os.linesep))
    update_each_item(node, require_type, tag='tag:yaml.org,2002:str')
    return node

def recognize_process(node):
    if isinstance(node, yaml.ScalarNode):
        require_type(node, 'tag:yaml.org,2002:str')
    else:
        node = recognize_process_description(node)
    return node

def recognize_workflow_step(node):
    require_keys(node, ['id', 'in', 'out', 'run'])

    update_key(node, 'in', recognize_connections)
    update_key(node, 'run', recognize_process)
    node.tag = u'!WorkflowStep'
    return node

def recognize_workflow_steps(node):
    node = mapping_to_sequence(node, 'id')
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a mapping or list of steps'.format(
                           node.start_mark, os.linesep))

    update_each_item(node, recognize_workflow_step)
    return node

def recognize_workflow(node):
    require_keys(node, ['steps'])
    update_key(node, 'steps', recognize_workflow_steps)
    node.tag = u'!Workflow'
    return node

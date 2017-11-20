from .common import *

def recognize_expression_tool(node):
    # Any process that is not something else is an ExpressionTool
    if isinstance(node, yaml.MappingNode):
        node.tag = u'!ExpressionTool'
    return node

def recognize_workflow(node):
    # A Workflow is a Process with steps
    require_keys(node, ['steps'])
    update_key(node, 'steps', recognize_workflow_steps)
    node.tag = u'!Workflow'
    return node

from .common import *

import os
import re

def recognize_expression(node):
    # References go first, otherwise they're recognized as constant strings
    node = optionally(recognize_reference_expression, node)
    node = optionally(recognize_constant_expression, node)
    node = optionally(recognize_file_description, node)
    node = optionally(recognize_directory_description, node)
    node = optionally(recognize_file_constructor, node)
    node = optionally(recognize_directory_constructor, node)
    node = optionally(recognize_merge_expression, node)

    if not was_recognized(node):
        raise RuntimeError('{}{}Invalid expression'.format(
            node.start_mark, os.linesep))
    return node

def recognize_reference_expression(node):
    # TODO: support array indexing
    require_type(node, 'tag:yaml.org,2002:str')
    if re.match('\$\([^)]*\)', node.value.strip()):
        selectors = [s.strip() for s in node.value[2:-1].split('.')]
        key = yaml.ScalarNode('tag:yaml.org,2002:str', 'selectors')
        value = yaml.SequenceNode('tag:yaml.org,2002:seq', selectors)
        new_node = yaml.MappingNode('!ReferenceExpression', [(key, value)])
        return new_node
    else:
        raise RuntimeError('{}{}Invalid reference syntax.'.format(
            node.start_mark, os.linesep))

def recognize_constant_expression(node):
    if not isinstance(node, yaml.ScalarNode):
        raise RuntimeError('{}{}A constant expression must be a scalar'.format(
            node.start_mark, os.linesep))

    key = yaml.ScalarNode('tag:yaml.org,2002:str', 'value')
    new_node = yaml.MappingNode('!ConstantExpression', [(key, node)])
    return new_node

def recognize_merge_method(node):
    require_type(node, 'tag:yaml.org,2002:str')
    merge_methods = ['merge_flattened', 'merge_nested']
    if node.value not in merge_methods:
        raise RuntimeError('{}{}Invalid merge method; must be either ' \
                '"merge_flattened" or "merge_nested"'.format(
                    node.start_mark, os.linesep))
    return node

def recognize_merge_expression(node):
    require_keys(node, ['mergeMethod', 'sources'])
    update_key(node, 'mergeMethod', recognize_merge_method)
    node.tag = u'!MergeExpression'
    return node

def recognize_file_description(node):
    require_keys(node, ['file_location'])
    set_key_default(node, 'secondaryFiles', [])
    node.tag = '!FileDescription'
    return node

def recognize_directory_description(node):
    require_keys(node, ['dir_location'])
    node.tag = '!DirectoryDescription'
    return node

def recognize_file_constructor(node):
    require_keys(node, ['file_contents'])
    update_key(node, 'file_contents', recognize_expression)
    node.tag = '!FileConstructor'
    return node

def recognize_directory_constructor(node):
    require_keys(node, ['dir_contents'])
    update_key(node, 'dir_contents', update_dir_contents)

    node.tag = '!DirectoryConstructor'
    return node

def update_dir_contents(node):
    update_each_value(node, recognize_expression)
    return node

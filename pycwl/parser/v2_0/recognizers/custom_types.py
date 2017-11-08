from .common import *

import os

def recognize_type_definition(node):
    require_keys(node, ['name', 'description'])
    require_type(get_by_key(node, 'name'), 'tag:yaml.org,2002:str')

    update_key(node, 'description', recognize_type_description)
    node.tag = '!TypeDefinition'
    return node

def recognize_type(node):
    node = optionally(recognize_type_description, node)

    if not was_recognized(node):
        if not (
                isinstance(node, yaml.ScalarNode) and
                node.tag == 'tag:yaml.org,2002:str'
                ):
            raise RuntimeError('{}{}Invalid input: expected a type name or a type description'.format(
                node.start_mark, os.linesep))
        node.tag = '!Type'
    return node

def recognize_type_description(node):
    node = optionally(recognize_file_type_description, node)
    node = optionally(recognize_array_type_description, node)
    node = optionally(recognize_enum_type_description, node)
    node = optionally(recognize_record_type_description, node)

    if not was_recognized(node):
        raise RuntimeError('{}{}Invalid type description'.format(
            node.start_mark, os.linesep))

    set_key_default(node, 'doc', '')
    return node

def recognize_file_type_description(node):
    require_keys(node, ['format'])
    require_type(get_by_key(node, 'format'), 'tag:yaml.org,2002:str')

    set_key_default(node, 'streamable', False)
    interpret_as_bool(get_by_key(node, 'streamable'))
    require_type(get_by_key(node, 'streamable'), 'tag:yaml.org,2002:bool')

    node.tag = '!FileTypeDescription'
    return node

def recognize_array_type_description(node):
    require_keys(node, ['arrayOf'])
    rename_key(node, 'arrayOf', 'itemType')
    update_key(node, 'itemType', recognize_type)
    node.tag = '!ArrayTypeDescription'
    return node

def recognize_enum_type_description(node):
    require_keys(node, ['symbols'])
    symbols = get_by_key(node, 'symbols')
    if not isinstance(symbols, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a list of symbols'.format(
                node.start_mark, os.linesep))

    for symbol in symbols.value:
        require_type(symbol, 'tag:yaml.org,2002:str')

    node.tag = '!EnumTypeDescription'
    return node

def recognize_record_type_description(node):
    require_keys(node, ['record'])
    rename_key(node, 'record', 'fields')

    update_key(node, 'fields', mapping_to_sequence, 'name')
    fields = get_by_key(node, 'fields')
    update_each_item(fields, recognize_record_field_description)

    node.tag = '!RecordTypeDescription'
    return node

def recognize_record_field_description(node):
    require_keys(node, ['name', 'type'])
    update_key(node, 'type', recognize_type)
    node.tag = '!RecordFieldDescription'
    return node

import logging
import yaml
import sys
from pycwl.pycwl import *

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def parse_cwlfile(cwlfile):
        '''parse workflow from CWL file'''
        with open(cwlfile, 'r') as cwlstream:
            return Parser.parse_cwlstream(cwlstream)

    @staticmethod
    def parse_cwlstream(cwlstream):
        '''parse workflow from CWL file stream'''
        logger.info('parsing CWL file {}'.format(cwlstream.name))
        try:
            cwldict = yaml.load(cwlstream)
        except yaml.composer.ComposerError as e:
            raise CWLParseException('Invalid CWL file') from e

        logger.debug('Raw CWL yaml content: {}'.format(str(cwldict)))
        if not (cwldict.get('cwlVersion') == 'v1.0'):
            raise Exception('cwlVersion not equal to v1.0')
        cwltype = cwldict.get('class')
        logger.debug('Parsing {}'.format(cwltype))
        if (cwltype == 'CommandLineTool'):
            return Parser.parse_commandlinetool(cwldict)
        elif (cwltype == 'Workflow'):
            return Parser.parse_workflow(cwldict)
        else:
            raise CWLParseException('CWL type is not of type CommandLineTool' +
                                    ' or Workflow: {}'.format(cwltype))

    @staticmethod
    def parse_job_object(job_object_file):
        '''parse CWL job object'''
        logger.info('parsing job object {}'.format(job_object_file.name))
        jobdict = yaml.load(job_object_file)
        logger.debug('Raw job object yaml content: {}'.format(str(jobdict)))
        job_object = 3
        return job_object

    @staticmethod
    def parse_commandlinetool(cwldict):
        '''parse commandlinetool from yaml dictionary'''
        # parse baseCommand
        basecommand = cwldict.get('baseCommand')
        if basecommand is None:
            basecommand = []
        elif not type(basecommand) is list:
            # create a list of the string
            basecommand = [str(basecommand)]
        else:
            # make sure everything is a string in the list
            basecommand = [str(x) for x in basecommand]
        # parse inputs
        inputs = cwldict.get('inputs')
        if inputs is None:
            raise CWLParseException('Required field inputs is not defined')
        else:
            inputs = Parser.to_dict(inputs)
        # define input objects
        input_objects = {}
        for k, v in inputs.items():
            datatype = v.get('type')
            input_objects[k] = IO(datatype=datatype)
        # parse output
        outputs = cwldict.get('outputs')
        if outputs is None:
            raise CWLParseException('Required field outputs is not defined')
        else:
            outputs = Parser.to_dict(outputs)
        # define output objects
        output_objects = {}
        for k, v in outputs.items():
            datatype = v.get('type')
            output_objects[k] = IO(datatype=datatype)
        # create CommandLineTool object
        commandlinetool = CommandLineTool(baseCommand=cwldict.get(
                                          'baseCommand'),
                                          inputs=input_objects,
                                          outputs=output_objects)
        return commandlinetool

    @staticmethod
    def to_list(iterable):
        '''convert iterable to list'''
        if type(iterable) is list:
            return iterable
        elif type(iterable) is dict:
            results = []
            for k, v in iterable.items():
                v['id'] = k
                results.append(v)
            return results
        else:
            raise CwlParseException(
                'Expected list or dict, got {} ({})'.format(
                    iterable, type(iterable)))

    @staticmethod
    def to_dict(iterable):
        '''convert iterable to dict'''
        if type(iterable) is dict:
            return iterable
        elif type(iterable) is list:
            results = {}
            for item in iterable:
                results[item.get('id')] = item
                del item['id']
            return results
        else:
            raise CwlParseException(
                'Expected list or dict, got {} ({})'.format(
                    iterable, type(iterable)))


class CWLParseException(Exception):
    pass

'''
#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: echo
inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs: []
'''

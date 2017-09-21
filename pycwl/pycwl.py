#TODO: add docstrings
from graphviz import Digraph


class IO(object):
    def __init__(self, datatype='string', default_value='', output_type=''):

        self.datatype = datatype
        self.def_value = default_value
        self.output_type = output_type

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        self._datatype = value

    @property
    def def_value(self):
        return self._def_value

    @def_value.setter
    def def_value(self, value):
        self._def_value = value

    @property
    def output_type(self):
        return self._output_type

    @output_type.setter
    def output_type(self, value):
        self._output_type = value


class Process(object):
    def __init__(self, cwlVersion='', inputs=None, outputs=None):

        self.cwlVersion = cwlVersion

        if inputs is None:
            self.inputs = {}
        else:
            self.inputs = inputs

        if outputs is None:
            self.outputs = {}
        else:
            self.outputs = outputs

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        self._outputs = value

    @property
    def cwlVersion(self):
        return self._cwlVersion

    @cwlVersion.setter
    def cwlVersion(self, value):
        self._cwlVersion = value


class CommandLineTool(Process):
    def __init__(
            self,
            cwlVersion='',
            inputs=None,
            outputs=None,
            baseCommand=None,
            stdout='',
            successCodes='',
            permanentFailCodes='',
            arguments='',
        ):

        super(CommandLineTool, self).__init__(
            cwlVersion=cwlVersion,
            inputs=inputs,
            outputs=outputs,
        )

        if baseCommand is None:
            self.baseCommand = []
        else:
            self.baseCommand = baseCommand

        self.stdout = stdout
        self.successCodes = successCodes
        self.permanentFailCodes = permanentFailCodes
        self.arguments = arguments

    @property
    def baseCommand(self):
        return self._baseCommand

    @baseCommand.setter
    def baseCommand(self, value):
        self._baseCommand = value

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, value):
        self._stdout = value

    @property
    def successCodes(self):
        return self._successCodes

    @successCodes.setter
    def successCodes(self, value):
        self._successCodes = value

    @property
    def permanentFailCodes(self):
        return self._permanentFailCodes

    @permanentFailCodes.setter
    def permanentFailCodes(self, value):
        self._permanentFailCodes = value

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value


class Workflow(Process):
    def __init__(
            self,
            cwlVersion='',
            inputs=None,
            outputs=None,
            steps=None,
        ):

        super(Workflow, self).__init__(
            cwlVersion=cwlVersion,
            inputs=inputs,
            outputs=outputs,
        )

        if steps is None:
            self.steps = {}
        else:
            self.steps = steps

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value

    def get_dot(self):
        dot = Digraph() # comment='The Round Table')
        for s in self.steps:
            dot.node(s, s, shape="box")

            for step_output in self.steps[s].outputs:
                dot.node(step_output,step_output)
                dot.edge(s, step_output)

            for outputn in self.steps[s].input_map:
                inputn = self.steps[s].input_map[outputn]

                if not outputn in self.inputs:
                    dot.node(inputn, inputn)

                    if "/" in outputn:

                        p, o = outputn.split("/")
                        #dot.node(o, o)
                        dot.edge(o, inputn)
                    else:
                        dot.edge(outputn, inputn)

                dot.edge(inputn, s)

                #print outputn, inputn
        for flow_input in self.inputs:
            dot.node(flow_input, flow_input)
            for s in self.steps:
                if flow_input in self.steps[s].input_map:
                    dot.edge(flow_input, self.steps[s].input_map[flow_input], color="blue")

        for flow_output in self.outputs:
            dot.node(flow_output, flow_output)
            if "/" in flow_output:
                p, o = flow_output.split("/")
                dot.edge(o, flow_output, color="blue")

        return dot


class Step(object):
    def __init__(self, process=None, input_map=None, outputs=None):

        self.process = process

        if input_map is None:
            self.input_map = {}
        else:
            self.input_map = input_map

        if outputs is None:
            self.outputs = set()
        else:
            self.outputs = outputs

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, value):
        self._process = value

    @property
    def input_map(self):
        return self._input_map

    @input_map.setter
    def input_map(self, value):
        self._input_map = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        self._outputs = value

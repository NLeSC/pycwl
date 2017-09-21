

class IO(object):
    def __init__(self, **args):
        self.key_datatype = "datatype"
        self.key_def_value = "default_value"
        self.key_output_type = "output_type"

        self.default_datatype = "string"
        self.default_def_value = ""  # Nice!!
        self.default_output_type = ""

        if self.key_datatype in args:
            self.datatype = args[self.key_datatype]
        else:
            self.datatype = self.default_datatype

        if self.key_def_value in args:
            self.def_value = args[self.key_def_value]
        else:
            self.def_value = self.default_def_value

        if self.key_output_type in args:
            self.output_type = args[self.key_output_type]
        else:
            self.output_type = self.default_output_type

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


# ------------------------------------------------------------------------------------
class Process(object):

    def __init__(self, **args):
        # self.name = None
        self.key_cwlVersion = "cwlVersion"
        self.key_inputs = "inputs"
        self.key_outputs = "outputs"

        self.default_cwlVersion = ""
        self.default_inputs = {}
        self.default_outputs = {}

        if self.key_cwlVersion in args:
            self.cwlVersion = args[self.key_cwlVersion]
        else:
            self.cwlVersion = self.default_cwlVersion

        if self.key_inputs in args:
            self.inputs = args[self.key_inputs]
        else:
            self.inputs = self.default_inputs

        if self.key_outputs in args:
            self.outputs = args[self.key_outputs]
        else:
            self.outputs = self.default_outputs

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


# ------------------------------------------------------------------------------------
class CommandLineTool(Process):

    def __init__(self, **args):
        super(CommandLineTool, self).__init__(**args)
        self.key_baseCommand = "baseCommand"
        self.key_stdout = "stdout"
        self.key_successCodes = "successCodes"
        self.key_permanentFailCodes = "permanentFailCodes"
        self.key_arguments = "arguments"

        self.default_baseCommand = []
        self.default_stdout = ""
        self.default_successCodes = ""
        self.default_permanentFailCodes = ""
        self.default_arguments = ""

        if self.key_baseCommand in args:
            self.baseCommand = args[self.key_baseCommand]
        else:
            self.baseCommand = self.default_baseCommand

        if self.key_stdout in args:
            self.stdout = args[self.key_stdout]
        else:
            self.stdout = self.default_stdout

        if self.key_successCodes in args:
            self.successCodes = args[self.key_successCodes]
        else:
            self.successCodes = self.default_successCodes

        if self.key_permanentFailCodes in args:
            self.permanentFailCodes = args[self.key_permanentFailCodes]
        else:
            self.permanentFailCodes = self.default_permanentFailCodes

        if self.key_arguments in args:
            self.arguments = args[self.key_arguments]
        else:
            self.arguments = self.default_arguments

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


# ------------------------------------------------------------------------------------
from graphviz import Digraph

class Workflow(Process):
    
    def __init__(self, **args):

        super(Workflow, self).__init__(**args)

        self.key_steps = "steps"

        self.default_steps = {}

        if self.key_steps in args:
            self.steps = args[self.key_steps]
        else:
            self.steps = self.default_steps

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

    # def  __init__(self, process=None, input_map=None, outputs=None):
    #     self.process == process
    #     if input_map is None:
    #         self.input_map = {}
    #     else:
    #         self.input_map = input_map
            
    #     self.outputs= set() 

    def __init__(self, **args):

        self.key_process = "process"
        self.key_input_map = "input_map"
        self.key_outputs = "outputs"

        self.default_process = None
        self.default_input_map = {}
        self.default_outputs = {}

        if self.key_process in args:
            self.process = args[self.key_process]
        else:
            self.process = self.default_process

        if self.key_input_map in args:
            self.input_map = args[self.key_input_map]
        else:
            self.input_map = self.default_input_map

        if self.key_outputs in args:
            self.outputs = args[self.key_outputs]
        else:
            self.outputs = self.default_outputs

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

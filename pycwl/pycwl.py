

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
        # Note for working with subgraphs:
        # For things to render as subgraphs you need to give the main graph a filename (filename="cluster.gv").
        # And the subgraphs need to have a name that starts with the filename (cluster_) and then have incremental 
        # values
        flow_g = Digraph(filename="cluster.gv")
        flow_g.graph_attr.update(size='10', rankdir="TB", rank='max')

        print "Step nodes: "
        with flow_g.subgraph(name="cluster_1") as dot:
            dot.graph_attr.update(color="white")
            for s in self.steps:
                dot.node(s, s, shape="box", color="blue")
                print s

                for step_output in self.steps[s].outputs:
                    print step_output
                    dot.node(step_output,step_output)
                    dot.edge(s, step_output)

                for outputn in self.steps[s].input_map:
                    inputn = self.steps[s].input_map[outputn]

                    if not outputn in self.inputs:
                        dot.node(inputn, inputn)
                        print inputn

                        if "/" in outputn:

                            p, o = outputn.split("/")
                            #dot.node(o, o)
                            dot.edge(o, inputn)
                        else:
                            dot.edge(outputn, inputn)
                    #print (inputn, s)
                    dot.edge(inputn, s)

        
        print ("flow_inputs:")
        with flow_g.subgraph(name="cluster_0") as flow_top:
            for flow_input in self.inputs:
                print flow_input   
                flow_top.node(flow_input, flow_input, color="red")#, rank='max')#, rank=1)
                for s in self.steps:
                    if flow_input in self.steps[s].input_map:
                        flow_top.edge(flow_input, self.steps[s].input_map[flow_input], color="blue")



        print "flow outputs: "
        with flow_g.subgraph(name="cluster_2") as bot_g:
            bot_g.graph_attr.update(rank='3')
            for flow_output in self.outputs:
                bot_g.node(flow_output, flow_output, color="red")
                print flow_output
                if "/" in flow_output:
                    p, o = flow_output.split("/")
                    flow_g.edge(o, flow_output, color="blue")

        #flow_g.subgraph(dot)
        return flow_g


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

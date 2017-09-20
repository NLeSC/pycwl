

class IO(object):
	def __init__(self, **args):
		self.key_datatype = "datatype"
		self.key_def_value = "default_value"

		self.default_datatype = "string"
		self.default_def_value = "" # Nice!!

		if self.key_datatype in args:
			self.datatype = args[self.key_datatype]
		else:
			self.datatype = self.default_datatype


		if self.key_def_value in args:
			self.def_value = args[self.key_def_value]
		else:
			self.def_value = self.default_def_value


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






class Process(object):

	def __init__(self):
		self.name = None

	def get_name(self):
		return self.name
	def set_name(self, name):
		self.name=name



class CommandLineTool(Process):



	def __init__(self, **args):
		self.key_baseCommand = "baseCommand"
		self.key_cwlVersion = "cwlVersion"	
		self.key_stdout = "stdout"
		self.key_inputs = "inputs"
		self.key_outputs = "outputs"
		self.key_successCodes = "successCodes"
		self.key_permanentFailCodes = "permanentFailCodes"
		self.key_arguments = "arguments"

		self.default_baseCommand = ""
		self.default_cwlVersion = ""
		self.default_stdout = ""
		self.default_inputs = {}
		self.default_outputs = {}
		self.default_successCodes = ""
		self.default_permanentFailCodes = ""
		self.default_arguments = ""

		if self.key_baseCommand in args:
			self.baseCommand = args[self.key_baseCommand]
		else:
			self.baseCommand = self.default_baseCommand

		if self.key_cwlVersion in args:
			self.cwlVersion = args[self.key_cwlVersion]
		else:
			self.cwlVersion = self.default_cwlVersion
				
		if self.key_stdout in args:
			self.stdout = args[self.key_stdout]
		else:
			self.stdout = self.default_stdout

		if self.key_inputs in args:
			self.inputs = args[self.key_inputs]
		else:
			self.inputs = self.default_inputs

		if self.key_outputs in args:
			self.outputs = args[self.key_outputs]
		else:
			self.outputs = self.default_outputs

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


		#print self.


		# self._inputs		= set([])
		# self._outputs		= set([])
		# self._successCodes 	= 0
		# self._permanentFailCodes = 33

	@property
	def inputs(self):
		return self._inputs
	@inputs.setter
	def inputs(self, value):
		self._inputs = value

	@property
	def cwlVersion(self):
		return self._cwlVersion
	@cwlVersion.setter
	def cwlVersion(self, value):
		self._cwlVersion = value

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

	def __init__(self):
		self.cwlVersion		= ""
		self.inputs			= set([])
		self.outputs		= set([])
		self.steps			= set([]) # Set of work_node's


class Step(object):

	def __init__(self):

		self.process 		= None
		self.input_map 		= None
		self.output 	= None



class InvalidCommandError(Exception):
	"""Exception raised when a command is detected as invalid"""
	pass
		

class Command:
	def __init__(self, name: str, args: list = None, func=None,
		  accepts_args=False):

		def f(smth=True):
			if smth: pass
			pass

		if args is None:
			args = []

		if func is None:
			func = f

		self.name = name
		self.args = args
		self.args_num = len(args)
		self.acc_args = accepts_args
		self.func = func

	def exe(self):
		if self.acc_args:
			self.func(self.args)

		else:
			if self.args:
				raise TypeError

			self.func()


def parse(cmd_string: str, key: str, mapping: dict, float_func=None,
	  float_func_args=None):

	if len(cmd_string) == 0 or cmd_string[0] not in key:
		return None

	args = cmd_string.split()
	for i in range(len(args)):
		args[i] = args[i].lower()

	cmd = args[0]
	args = args[1:]

	quotes_open = []
	quotes_close = []

	# Merges every element in args that is between one with the fist
	# character that is " and one with the last character that is "
	for i, arg in enumerate(args):
		if len(arg) >= 1 and arg[0] == '"': quotes_open.append(i)
		elif len(arg) >= 1 and arg[-1] == '"': quotes_close.append(i)

	if len(quotes_open) != len(quotes_close):
		raise InvalidCommandError

	for open_quotes, close_quotes in zip(quotes_open, quotes_close):
		for arg in args[open_quotes + 1:close_quotes + 1]:
			args[open_quotes] += f" {arg}"

		args[open_quotes] = args[open_quotes].replace('"', "")

	for arg in range(len(args) - 1, -1, -1):
		for i in range(len(quotes_open)):
			if quotes_open[i] < arg <= quotes_close[i]:
				del args[arg]

	for i, arg in enumerate(args):
		try:
			if float_func is not None:
				if float_func_args is not None:
					possible_float = float_func(arg, float_func_args)
				else:
					possible_float = float_func(arg)

			else:
				possible_float = float(arg)
		except ValueError:
			possible_float = None

		if possible_float is not None:
			args[i] = possible_float

		elif arg == "false": args[i] = False

		elif arg == "true":  args[i] = True

	try:
		function = mapping[cmd]["func"]
		acc_args = mapping[cmd]["args"]

	except KeyError:
		raise InvalidCommandError

	return Command(cmd, args, function, acc_args)

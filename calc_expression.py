################################
# Local dependencies
################################
import lang
import literals
import settings as sets


class Expression:
	def __init__(self, expression):
		self._nums = expression[0]
		self._operators = expression[1]
		self._opening_prth = expression[2]
		self._closing_prth = expression[3]

	def optimized_calculation(self):
		if None in self._nums:
			return None, "syntax_error"

		operations = ["R", "^", "*/%", "+-"]
		error_occurred = ""

		for prth_pos in range(len(self._closing_prth)):
			total_calculations = 0
			not_to_calculate_nums = []
			opening_prth = self._opening_prth[prth_pos]
			closing_prth = self._closing_prth[prth_pos]

			for i in range(opening_prth):
				not_to_calculate_nums.append(self._nums[i])

			to_calculate_nums = self._nums[opening_prth:closing_prth + 1].copy()

			for operation in operations:
				calculations = 0
				for i in range(closing_prth - opening_prth - total_calculations):
					num_1 = to_calculate_nums[i     - calculations]
					num_2 = to_calculate_nums[i + 1 - calculations]
					operator = self._operators[i + opening_prth - calculations]

					try:
						if operator not in operation: continue

						elif operator == "+": to_calculate_nums[i - calculations] = num_1 + num_2

						elif operator == "-": to_calculate_nums[i - calculations] = num_1 - num_2

						elif operator == "*": to_calculate_nums[i - calculations] = num_1 * num_2

						elif operator == "/": to_calculate_nums[i - calculations] = num_1 / num_2

						elif operator == "%": to_calculate_nums[i - calculations] = num_1 % num_2

						elif operator == "^":
							if num_1 == num_2 == 0:
								error_occurred = "undefined"
							else:
								to_calculate_nums[i - calculations] = num_1 ** num_2

						elif operator == "R":
							if type(num_1) is literals.Pol:
								try:
									to_calculate_nums[i - calculations] = num_2.root(num_1)

								except TypeError: raise literals.NonIntRootError

							else:
								to_calculate_nums[i - calculations] = num_2 ** (1 / num_1)

						if sets.settings["debug_mode"]:
							if operator == "R":
								print("calc " + str(num_1), "\bR", num_2)
							else:
								print("calc " + str(num_1) + ", ", num_2, f"-> '{operator}'")
							# print("repr", repr(num_1), repr(num_2))


						if sets.settings["debug_mode"]:
							print("result", to_calculate_nums[i - calculations])
							# print("repr_result", repr(to_calculate_nums[i - calculations]))

						del to_calculate_nums[i + 1 - calculations]
						del self._operators[i + opening_prth - calculations]
						total_calculations += 1
						calculations += 1

					except OverflowError:
						error_occurred = "infinity"

						lang.write_error_log(
							"OverflowError",
							"calc_expression.py|class|def|for|for|for|except",
							sets.settings["debug_mode"]
						)

						break

					except ZeroDivisionError:
						error_occurred = "undetermined" if num_1 == 0 else "impossible"

						lang.write_error_log(
							"ZeroDivisionError",
							"calc_expression.py|class|def|for|for|for|except",
							sets.settings["debug_mode"]
						)

						break

					except literals.ImpossibleDivError:
						error_occurred = "impossible_div_error"

						lang.write_error_log(
							"ImpossibleDivError",
							"calc_expression.py|class|def|for|for|for|except",
							sets.settings["debug_mode"]
						)

						break

					except literals.NonIntPowError:
						error_occurred = "non_int_pow_error"

						lang.write_error_log(
							"NonIntPowError",
							"calc_expression.py|class|def|for|for|for|except",
							sets.settings["debug_mode"]
						)

						break

					except literals.NonIntRootError:
						error_occurred = "non_int_root_error"

						lang.write_error_log(
							"non_int_root_error",
						    "calc_expression.py|class|def|for|for|for|except",
							sets.settings["debug_mode"]
						)

						break

			not_to_calculate_nums += to_calculate_nums

			for i in range(closing_prth + 1, len(self._operators) + 1 + total_calculations):
				not_to_calculate_nums.append(self._nums[i])

			for i in range(len(self._closing_prth)):
				self._closing_prth[i] -= total_calculations

				if self._opening_prth[i] >= closing_prth:
					self._opening_prth[i] -= total_calculations

			self._nums = not_to_calculate_nums.copy()

		result = self._nums[0]

		return result, error_occurred

# =========================Constants=========================
MON_DICT = {"": 1.0}


def make_pol(number): return Pol(Mon(float(number)))


################################
# Exceptions
################################
class NonSimMonError(Exception):
    """Exception raised when trying to add or subtract two non-similar monomial"""
    pass


class ImpossibleDivError(Exception):
    """Exception raised when dividing two monomials and one of the exponents becomes negative"""
    pass


class NonIntPowError(Exception):
    """Exception raised when trying to make a non-integer power on a monomial"""
    pass


class NonIntRootError(Exception):
    """Exception raised when trying to calculate a negative root or that contains letters"""
    pass


################################
# Monomials
################################
class Mon:
    """Defines monomials and how they operate.
    The dunder methods defined are:
    __init__, __str__, __repr__, __add__, __sub__, __truediv__, __floordiv__, __mul__, __pow__, __eq__, __abs__, __neg__

    The custom methods are:
    is_similar(self, other) -> returns True if self.lt == other.lt
    is_opposite(self, other) -> returns True if self + other == Mon(0)
    grade(self) -> returns the sum of the exponents of the monomial

    each method is so large because it has to be able to deal with floats, Mons and Pols respectively
    """

    # =========================Custom methods=========================
    def is_similar(self, other) -> bool:
        if self.num == 0 or other.num == 0: return True  # Doesn't matter if it's zero

        return self.lt == other.lt

#-----------------------------------------------------------------------------------------------------------------------
    def is_opposite(self, other) -> bool:
        return self + other == 0

#-----------------------------------------------------------------------------------------------------------------------
    def grade(self):
        grade = 0
        for letter in self.lt:
            if letter != "":
                if type(self.lt[letter]) is not float: return None
                grade += self.lt[letter]

        return grade

#-----------------------------------------------------------------------------------------------------------------------
    def fix(self):
        if self.num == 0: self.lt = MON_DICT
        if type(self.lt[""]) is float:
            self.num **= self.lt[""]
            self.lt[""] = 1

    # =========================Dunder methods=========================
    def __init__(self, number: float, letters: dict = None):
        if letters is None: letters = MON_DICT

        self.num = number
        self.lt = letters

#-----------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        self.fix()

        if self.num == 1:
            temp_str = ""

        elif self.num == -1:
            temp_str = "-"

        else: temp_str = str(self.num)

        if self.lt[""] != 1:  # I assume that it's not float
            temp_str = f"{str(self.num)}^"
            power = str(self.lt[""])
            if len(power) == 1: temp_str += power
            else: temp_str += f"({power})"

        for letter in self.lt:
            if letter == "": continue
            temp_str += letter
            if self.lt[letter] != 1:
                if type(self.lt[letter]) is float: temp_str += f"^{str(self.lt[letter])}"
                else:
                    power = str(self.lt[letter])
                    if len(power) == 1: temp_str += f"^{power}"
                    else: temp_str += f"^({power})"

        if temp_str == "": temp_str = "1"
        elif temp_str == "-": temp_str = "-1"

        return temp_str

#-----------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"Mon({self.num}, {self.lt})"

#-----------------------------------------------------------------------------------------------------------------------
    def __add__(self, other):
        if type(other) is float or type(other) is int:
            if self.lt != MON_DICT: raise NonSimMonError
            total = self.num + other
            new_lt = self.lt.copy()

        elif type(other) is Mon:
            if not self.is_similar(other): raise NonSimMonError
            total = self.num + other.num
            new_lt = self.lt if self.num != 0 else other.lt

        else:  # In theory can be only Pol
            if len(other) != 1: raise NonSimMonError

            return self + other.first_mon()


        return Mon(total, new_lt if total != 0 else MON_DICT)

#-----------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            if self.lt != MON_DICT: raise NonSimMonError

            total = self.num - other

        elif type(other) is Mon:
            if not self.is_similar(other): raise NonSimMonError

            total = self.num - other.num

        else:  # In theory it can be only Pol
            if len(other) != 1: raise NonSimMonError

            return self - other.first_mon()

        return Mon(total, self.lt if total != 0 else MON_DICT)

#-----------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other):
        new_lt = MON_DICT

        if type(other) is float or type(other) is int:
            return Mon(self.num / other, self.lt)

        if type(other) is Mon:
            for key in other.lt:
                try:
                    if key not in self.lt:
                        raise ImpossibleDivError
                except KeyError:
                    raise ImpossibleDivError

            for key in other.lt:
                if key == "": continue

                new_lt[key] = self.lt[key] - other.lt[key]
                if new_lt[key] == 0:
                    del new_lt[key]

            return Mon(self.num / other.num, new_lt)

        else:
            if len(Pol) != 1: raise ImpossibleDivError
            return self / other.first_mon()

#-----------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other):

        if type(other) is float or type(other) is int:
            return Mon(self.num * other, self.lt if self.num * other != 0 else MON_DICT)

        elif type(other) is Mon:
            new_lt = self.lt.copy()

            for key in other.lt:
                if key != "":
                    try:
                        new_lt[key] += other.lt[key]

                    except KeyError:
                        new_lt[key] = other.lt[key]

            return Mon(self.num * other.num, new_lt)

        else:
            return other * self  # Will call the __mul__ dunder of the Pol class that can deal with monomials

#-----------------------------------------------------------------------------------------------------------------------
    def __pow__(self, power, modulo=None):

        if type(power) is float or type(power) is int:
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "": new_lt[letter] *= power

            return Mon(self.num ** power, new_lt)

        elif type(power) is Mon:
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "": new_lt[letter] *= power.num

            return Mon(self.num ** power.num, new_lt)

        else:
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "": new_lt[letter] = power.first_mon() * new_lt[letter]  # Calls the __mul__ method of Mon

            return Mon(self.num ** power.first_mon().num, new_lt)

#-----------------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        if type(other) is Mon:
            return self.num == other.num and self.lt == other.lt

        elif (type(other) is float  or type(other) is int) and self.lt == MON_DICT:
            return self.num == other

        elif type(other) is Pol and len(other) == 1:
            return self == other.first_mon()

        else: return False

#-----------------------------------------------------------------------------------------------------------------------
    def __abs__(self):
        return Mon(float(abs(self.num)), self.lt)  # self.num being an int could cause problems

#-----------------------------------------------------------------------------------------------------------------------
    def __neg__(self):
        return Mon(-self.num, self.lt)


################################
# Polynomials
################################
class Pol:
    """Defines how polynomials operate.
    Polynomials can only operate between other polynomials.
    The dunder methods defined are:
    __init__, __str__, __repr__, __add__, __sub__, __mul__, __truediv__, __pow__, __neg__, __len__, __eq__, __int__

    The custom methods are:
    grade(self) -> the highest grade of a Monomial
    order(self, letter: str, reverse: bool = False) -> orders the monomials by exponent of the letter
    complete(self, letter: str) -> completes the powers (from 0 to the highest) of a certain letter
    normal(self) -> sums similar monomials inside the polynomial
    clean(self) -> removes any monomial that has 0 as the number
    append_mon(self) -> appends a monomial to the end of the list
    copy(self) -> makes a copy of itself without creating aliases
    first_mon(self) -> returns the first monomial of the list
    root(self, rad_pow) -> calculates the root of the monomial (like a the power, but divides the exponents and the
                           number is being elevated to rad_pow ** -1)
    """


    # =========================Custom methods=========================

    # The highest grade of the monomials that contains
    def grade(self) -> int:
        grade = make_pol(0)
        for mon in self.mon:
            grade = mon.grade() if mon.grade() > grade else grade

        return grade

#-----------------------------------------------------------------------------------------------------------------------
    # Makes the polynomials ordered by a letter
    def order(self, letter: str, reverse: bool = False):

        if len(self.mon) > 1:

            # A simple bubble sort, there is no need for something faster
            for i in range(len(self.mon) - 1):
                for mon in range(len(self.mon) - (i + 1)):

                    try:
                        if self.mon[mon].lt[letter] > self.mon[mon + 1].lt[letter]:
                            self.mon[mon], self.mon[mon + 1] = self.mon[mon + 1], self.mon[mon]

                    except KeyError:
                        pass

        if reverse:
            self.mon.reverse()

#-----------------------------------------------------------------------------------------------------------------------
    def complete(self, letter: str):
        self.order(letter)
        for mon in range(len(self.mon)):
            pass

#-----------------------------------------------------------------------------------------------------------------------
    # Deletes any duplicates
    def normal(self):
        new_pl = self.copy()

        prev_len = len(self)
        new_pl = new_pl.__add__(Pol([]), normal_call=True)

        while prev_len > len(new_pl):
            new_pl = new_pl.__add__(Pol([]), normal_call=True)
            prev_len = len(new_pl)

        return new_pl

#-----------------------------------------------------------------------------------------------------------------------
    def clean(self):
        for i in range(len(self.mon) - 1, -1, -1):
            if self.mon[i].num == 0:
                del self.mon[i]

        if not self.mon: self.mon = [Mon(0)]

#-----------------------------------------------------------------------------------------------------------------------
    def append_mon(self, mon):
        self.mon.append(mon)

#-----------------------------------------------------------------------------------------------------------------------
    def copy(self):
        return Pol(self.mon.copy())

#-----------------------------------------------------------------------------------------------------------------------
    def first_mon(self):
        return self.mon[0]

#-----------------------------------------------------------------------------------------------------------------------
    def root(self, rad_pow):  # Radical power
        if len(self) != 1: raise NonIntRootError

        if type(rad_pow) is float or type(rad_pow) is int:
            return Pol(self.first_mon() ** (1 / rad_pow))

        elif type(rad_pow) is Mon:
            if rad_pow.lt != MON_DICT: raise NonIntPowError
            return Pol(self.first_mon() ** (1 / rad_pow.num))

        else:
            if len(rad_pow) != 1: raise NonIntPowError
            return Pol(self.first_mon() ** (1 / rad_pow.first_mon().num))


    # =========================Dunder methods=========================

    def __init__(self, monomials = None):
        if monomials is None: monomials = []
        if type(monomials) is not list: monomials = [monomials]

        self.mon = monomials

#-----------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        self.normal().clean()

        output_string = ""

        for monomial in self.mon:
            if monomial.num >= 0 and output_string == "":
                output_string += str(abs(monomial))

            elif monomial.num < 0 and output_string == "":
                output_string += str(monomial)

            elif monomial.num >= 0:
                output_string += " + " + str(monomial)

            else:
                output_string += " - " + str(abs(monomial))

        return output_string

#-----------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"Pol({self.mon})"

#-----------------------------------------------------------------------------------------------------------------------
    def __add__(self, other, normal_call=False):
        if type(other) is float or type(other) is int: pol_other = make_pol(other)

        elif type(other) is Mon: pol_other = Pol(other)

        else: pol_other = other

        new_pl = self.copy()

        for new_mon in pol_other.mon:
            add_mon = True

            for index in range(len(new_pl.mon)):
                try:
                    new_pl.mon[index] += new_mon
                    add_mon = False
                    break
                except NonSimMonError: pass

            if add_mon: new_pl.append_mon(new_mon)

        for index in range(len(new_pl.mon)):
            calculated_mons = 0

            for other_index in range(index, len(new_pl.mon)):
                if index != other_index:
                    try:
                        calculated_mon = new_pl.mon[index] + new_pl.mon[other_index - calculated_mons]
                        new_pl.mon[index] = calculated_mon
                        del new_pl.mon[other_index - calculated_mons]
                        calculated_mons += 1

                    except NonSimMonError: pass

        if not normal_call:
            return new_pl.normal()

        else:
            return new_pl

#-----------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):
        return self + (-other)

#-----------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other):
        new_pl = Pol()
        pol_other = other

        if type(other) is float or type(other) is int:
            pol_other = make_pol(other)

        elif type(other) is Mon:
            pol_other = Pol([other])

        for mon in self.mon:
            for other_mon in pol_other.mon:
                new_pl.append_mon(mon * other_mon)

        return new_pl.normal()

#-----------------------------------------------------------------------------------------------------------------------
    # I'm working on this to allow divisions between polynomials, not only monomials
    def __truediv__(self, other):
        new_pl = Pol()
        pol_other = other

        if type(other) is float or type(other) is int:
            pol_other = make_pol(other)

        elif type(other) is Mon:
            pol_other = Pol([other])

        if len(other) == 1:
            for mon in self.mon:
                new_pl.append_mon(mon / pol_other.mon[0])

            return new_pl.normal()

        else: raise ImpossibleDivError

#-----------------------------------------------------------------------------------------------------------------------
    def __pow__(self, power, modulo=None):
        if type(power) is float or type(power) is int:
            if int(power) != power: raise NonIntPowError
            pol_power = make_pol(power)

        elif type(power) is Mon:
            if power.lt != MON_DICT: raise NonIntPowError
            pol_power = Pol(power.num)

        else:
            if len(power) != 1 and len(self) != 1: raise NonIntPowError
            pol_power = power

        if len(self) != 1:
            mon = pol_power.first_mon()
            if mon.lt != MON_DICT or int(mon.num) != mon.num: raise NonIntPowError
            result = self.copy()
            for i in range(int(mon.num) - 1):
                result *= self
            return result.normal()

        else:
            return Pol(self.first_mon() ** pol_power)  # The __pow__ dunder of Mon can deal with the power being Pol

#-----------------------------------------------------------------------------------------------------------------------
    def __neg__(self):
        for i in range(len(self.mon)):
            self.mon[i] = -self.mon[i]

        return self

#-----------------------------------------------------------------------------------------------------------------------
    def __len__(self):
        return len(self.mon)

#-----------------------------------------------------------------------------------------------------------------------
    def __eq__(self, other):

        if type(other) is float or type(other) is int:
            if len(self) != 1: return False
            elif self.first_mon().lt != MON_DICT: return False
            else: return self.first_mon().num == other

        elif type(other) is Mon: return other == self

        elif type(other) is Pol: return self.mon == other.mon

        else: return False

#-----------------------------------------------------------------------------------------------------------------------
    def __gt__(self, other):
        if len(self) != 1 or self.first_mon().lt != MON_DICT: return False

        if type(other) is float or type(other) is int: return self.first_mon().num > other

        elif type(other) is Mon:
            if other.lt != MON_DICT: return False
            else: return self.first_mon().num > other.num

        # I assume that this can only be a polynomial at this point
        elif len(other) == 1 and other.first_mon().lt == MON_DICT:
            return self.first_mon().num > other.first_mon().num

        else: return False

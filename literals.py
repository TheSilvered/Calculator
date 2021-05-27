MON_DICT = {"": 1.0}

################################
# Exceptions
################################
class NonSimMonError(Exception):
    """
    Exception raised when trying to add or subtract two non-similar monomials.
    The similarity is defined by the is_similar(self, other) method of the Mon
    class.
    """
    pass


class ImpossibleDivError(Exception):
    """
    Exception raised both by the Mon and Pol classes.
    
    The Mon class raises it when in the divisor there are letters that don't
    appear in the dividend

    The Pol class raises it when the dividend is a polynomial, it is not raised
    when the dividend is of type Pol but has only one monomial
    """
    pass


class NonIntPowError(Exception):
    """
    Exception raised when the calculation of the power is impossible
    """
    pass


class NonIntRootError(Exception):
    """Exception raised the calculation of the root"""
    pass


class ImpossibleComparisonError(Exception):
    """
    Exception raised when a comparison between polynomials or monomials is
    impossible.
    This exception can be raised by: __ge__, __gt__, __eq__, __ne__, __le__,
    __lt__, is_similar
    """


################################
# Monomials
################################
class Mon:
    """Defines monomials and how they operate.

    The custom methods are:
    is_similar(self, other) -> returns True if self.lt == other.lt
    is_opposite(self, other) -> returns True if self + other == Mon(0)
    grade(self) -> returns the sum of the exponents of the monomial
    """

#-------------------------------------------------------------------------------        
    def is_similar(self, other) -> bool:
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__add__.__name__}: {type(other)}"

        if isinstance(other, (int, float)):
            return self.lt == MON_DICT

        elif isinstance(other, Mon):
            if self.num == 0 or other.num == 0:  # Doesn't matter if it's zero
                return True

            return self.lt == other.lt

        else:
            if len(other) != 1:
                raise ImpossibleComparisonError

            return self.is_similar(other.fm())

#-------------------------------------------------------------------------------
    def is_opposite(self, other) -> bool:
        return self + other == 0

#-------------------------------------------------------------------------------
    def grade(self):
        grade = 0
        for letter in self.lt:
            if letter != "":
                if not isinstance(self[letter], float): return None
                grade += self[lettter]

        return grade

#-------------------------------------------------------------------------------
    def fix(self):
        if self.num == 0: self.lt = MON_DICT
        if isinstance(self[""], float):
            self.num **= self[""]
            self.lt[""] = 1

#-------------------------------------------------------------------------------
    def __init__(self, number = 0.0, letters: dict = None):
        if letters is None:
            letters = MON_DICT

        if isinstance(number, int):
            number = float(number)

        if not "" in letters:
            letters[""] = 1

        for i in letters:
            if isinstance(letters[i], int):
                letters[i] = float(letters[i])

        self.num = number
        self.lt = letters

#-------------------------------------------------------------------------------
    def __str__(self):
        def is_whole(n):
            try:
                return int(n) == n
            except TypeError:
                return False

        self.fix()

        if self.num ==  1:
            return_string = ""

        elif self.num == -1:
            return_string = "-"

        else:
            if is_whole(self.num):
                return_string = str(int(self.num))
            else:
                return_string = str(self.num)

        # It should be automatically a monomial or a polynomial
        if self[""] != 1:
            return_string = f"{self.num}^({self['']})"

        for letter in self.lt:
            if letter == "":
                continue

            val = self[letter]
            return_string += letter

            if val != 1:
                if is_whole(val):
                    return_string += f"^{int(val)}"

                else:
                    return_string += f"^({val})"

        if return_string == "": return_string = "1"
        elif return_string == "-": return_string = "-1"

        return return_string

#-------------------------------------------------------------------------------
    def __repr__(self):
        return f"Mon({self.num}, {self.lt})"

#-------------------------------------------------------------------------------
    def __add__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__add__.__name__}: {type(other)}"

        if isinstance(other, (float, int)):
            if self.lt != MON_DICT: raise NonSimMonError
            total = self.num + other
            new_lt = self.lt.copy()

        elif isinstance(other, Mon):
            if not self.is_similar(other): raise NonSimMonError
            total = self.num + other.num
            new_lt = self.lt if self.num != 0 else other.lt

        else:  # In theory can be only Pol
            if len(other) != 1: raise NonSimMonError

            return self + other.fm()


        return Mon(total, new_lt if total != 0 else MON_DICT)

#-------------------------------------------------------------------------------
    def __sub__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__sub__.__name__}: {type(other)}"

        if isinstance(other, (float, int)):
            if self.lt != MON_DICT: raise NonSimMonError

            total = self.num - other

        elif isinstance(other, Mon):
            if not self.is_similar(other): raise NonSimMonError

            total = self.num - other.num

        else:  # In theory it can be only Pol
            if len(other) != 1: raise NonSimMonError

            return self - other.fm()

        return Mon(total, self.lt if total != 0 else MON_DICT)

#-------------------------------------------------------------------------------
    def __truediv__(self, other):
        new_lt = MON_DICT

        if isinstance(other, (float, int)):
            return Mon(self.num / other, self.lt)

        if isinstance(other, Mon):
            for key in other.lt:
                try:
                    if key not in self.lt:
                        raise ImpossibleDivError
                except KeyError:
                    raise ImpossibleDivError

            for key in other.lt:
                if key == "": continue

                new_lt[key] = self[key] - other[key]
                if new_lt[key] == 0:
                    del new_lt[key]

            return Mon(self.num / other.num, new_lt)

        else:
            if len(Pol) != 1: raise ImpossibleDivError
            return self / other.fm()

#-------------------------------------------------------------------------------
    def __mul__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__mul__.__name__}: {type(other)}"

        if type(other) is float or type(other) is int:
            lt = self.lt

            if self.num*other == 0:
                lt = MON_DICT

            return Mon(self.num * other, lt)

        elif isinstance(other, Mon):
            new_lt = self.lt.copy()

            for key in other.lt:
                if key != "":
                    try:
                        new_lt[key] += other[key]

                    except KeyError:
                        new_lt[key] = other[key]

            return Mon(self.num * other.num, new_lt)

        else:
            # Will call the __mul__ of the Pol class
            return other * self 

#-------------------------------------------------------------------------------
    def __pow__(self, power, modulo=None):
        assert isinstance(power, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__pow__.__name__}: {type(power)}"

        if isinstance(power, (float, int)):
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "": new_lt[letter] *= power

            return Mon(self.num ** power, new_lt)

        elif isinstance(power, Mon):
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "": new_lt[letter] *= power.num

            return Mon(self.num ** power.num, new_lt)

        else:
            new_lt = self.lt.copy()

            for letter in new_lt:
                if letter != "":
                    # Calls the __mul__ method of Mon
                    new_lt[letter] = power.fm() * new_lt[letter]

            return Mon(self.num ** power.fm().num, new_lt)

#-------------------------------------------------------------------------------
    def __abs__(self):
        return Mon(abs(self.num), self.lt)

#-------------------------------------------------------------------------------
    def __neg__(self):
        return Mon(-self.num, self.lt)

#-------------------------------------------------------------------------------
    def __gt__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__gt__.__name__}: {type(other)}"

        if not self.is_similar(other):
            raise ImpossibleComparisonError

        if isinstance(other, (int, float)):
            return self.num > other

        elif isinstance(other, Mon):
            return self.num > other.num

        else:
            return self.num > other.fm().num

#-------------------------------------------------------------------------------
    def __ge__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__ge__.__name__}: {type(other)}"

        if self == other:
            return True

        return self > other


#-------------------------------------------------------------------------------
    def __eq__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)) or other is None,\
          f"Invalid type for {self.__eq__.__name__}: {type(other)}"

        if isinstance(other, Mon):
            return self.num == other.num and self.lt == other.lt

        elif isinstance(other, (float, int)) and self.lt == MON_DICT:
            return self.num == other

        elif isinstance(other, Pol) and len(other) == 1:
            return self == other.fm()

        else: return False

#-------------------------------------------------------------------------------
    def __ne__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)) or other is None,\
          f"Invalid type for {self.__ne__.__name__}: {type(other)}"

        return not self == other

#-------------------------------------------------------------------------------
    def __lt__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__lt__.__name__}: {type(other)}"
        
        if not self.is_similar(other):
            raise ImpossibleComparisonError

        if isinstance(other, (int, float)):
            return self.num < other
            
        elif isinstance(other, Mon):
            return self.num < other.num

        else:
            return self.num < other.fm().num

#-------------------------------------------------------------------------------
    def __le__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__le__.__name__}: {type(other)}"

        if self == other:
            return True

        return self < other

#-------------------------------------------------------------------------------
    def __getitem__(self, key):
        try:
            return self.lt[key]

        except KeyError:
            return 0.0


################################
# Polynomials
################################
class Pol:
    """Defines how polynomials operate.
    Polynomials can only operate between other polynomials.
    The dunder methods defined are:
    __init__, __str__, __repr__, __add__, __sub__, __mul__, __truediv__,
    __pow__, __neg__, __len__, __eq__, __int__

    The custom methods are:
    grade(self) -> the highest grade of a Monomial
    order(self, letter: str, reverse: bool = False) -> orders the monomials by
      exponent of the letter
    complete(self, letter: str) -> completes the powers (from 0 to the highest)
      of a certain letter
    normal(self) -> sums similar monomials inside the polynomial
    clean(self) -> removes any monomial that has 0 as the number
    append(self) -> appends a monomial to the end of the list
    copy(self) -> makes a copy of itself without creating aliases
    fm(self) -> returns the first monomial of the list
    m(self, index) -> returns a monomial
    root(self, rad_pow) -> calculates the root of the monomial
    """


    # The highest grade between the monomials contained in the polynomial
    def grade(self) -> int:
        grade = Pol(0)
        for mon in self.mon:
            grade = mon.grade() if mon.grade() > grade else grade

        return grade

#-------------------------------------------------------------------------------
    # Makes the polynomials ordered by a letter
    def sort(self, lt: str, reverse: bool = False):
        if len(self) < 2:
            return

        # A simple bubble sort, there is no need for something faster
        for i in range(len(self)):
            for j in range(len(self) - i - 1):
                try:

                    a = self[j]
                    b = self[j + 1]

                    if a[lt] > b[lt]:
                        self[j], self[j + 1] = b, a

                except KeyError:
                    pass

        if reverse:
            self.reverse()

#-------------------------------------------------------------------------------
    def complete(self, lt: str):
        self.sort(lt)
        prev_exp = 0

        for i in range(len(self)):
            if self[i][lt] != prev_exp + 1:
                for j in range(int(prev_exp + 1), int(self[i][lt])):
                    self.append_mon(Mon(0, {lt: j}))

                prev_exp = self[i][lt]

        self.sort(lt)

#-------------------------------------------------------------------------------
    def normal(self):
        """Puts the polynomial to normal form summing similar monomials"""
        new_pl = self.copy()

        prev_len = len(self)
        new_pl = new_pl.__add__(Pol([]), normal_call=True)

        while prev_len > len(new_pl):
            new_pl = new_pl.__add__(Pol([]), normal_call=True)
            prev_len = len(new_pl)

        return new_pl

#-------------------------------------------------------------------------------
    def clean(self):
        for i in range(len(self) - 1, -1, -1):
            if self[i].num == 0:
                del self[i]

        if not self.mon: self.mon = [Mon(0)]

#-------------------------------------------------------------------------------
    def append_mon(self, mon):
        self.mon.append(mon)

#-------------------------------------------------------------------------------
    def copy(self):
        return Pol(self.mon.copy())

#-------------------------------------------------------------------------------
    def fm(self):
        return self.mon[0]

#-------------------------------------------------------------------------------
    def m(self, index):
        return self.mon[index]

#-------------------------------------------------------------------------------
    def me(self, mon, exp):
        return self[mon][exp]

#-------------------------------------------------------------------------------
    def has_sim(self, m: Mon, av_pos = None) -> int:  # Returns the index
        if av_pos is None:
            av_pos = []

        assert isinstance(m, (Mon, Pol)) and isinstance(av_pos, list),\
          f"Invalid type for {self.has_sim.__name__}: {type(m)}"

        if av_pos is None:
            av_pos = []

        if isinstance(m, Pol):
            m = m.fm()

        for i, n in enumerate(self.mon):
            if m.is_similar(n) and i not in av_pos:
                return i

        return None

#-------------------------------------------------------------------------------
    def reverse(self):
        self.mon.reverse()

#-------------------------------------------------------------------------------
    def root(self, rad_pow):
        assert isinstance(rad_pow, (int, float, Mon, Pol)),\
          f"Invalid type for {self.root.__name__}: {type(rad_pow)}"

        if len(self) != 1: raise NonIntRootError

        if isinstance(rad_pow, (float, int)):
            return Pol(self.fm() ** (1 / rad_pow))

        elif isinstance(rad_pow, Mon):
            if rad_pow.lt != MON_DICT: raise NonIntPowError
            return Pol(self.fm() ** (1 / rad_pow.num))

        else:
            if len(rad_pow) != 1: raise NonIntPowError
            return Pol(self.fm() ** (1 / rad_pow.fm().num))

#-------------------------------------------------------------------------------
    def __init__(self, mon = None):
        if mon is None:
            mon = [Mon()]

        if not isinstance(mon, list):
            mon = [mon]

        for i, n in enumerate(mon):
            if not isinstance(n, Mon):
                mon[i] = Mon(n)

        self.mon = mon

#-------------------------------------------------------------------------------
    def __str__(self):
        self.normal()
        self.clean()

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

#-------------------------------------------------------------------------------
    def __repr__(self):
        return f"Pol({self.mon})"

#-------------------------------------------------------------------------------
    # Normal call, when True, prevents the __add__ method from calling normal()
    def __add__(self, other, normal_call=False):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__add__.__name__}: {type(other)}"

        if isinstance(other, (float, int)):
            pol_other = Pol(other)

        elif isinstance(other, Mon):
            pol_other = Pol(other)

        else:
            pol_other = other

        new_pl = self.copy()

        for new_mon in pol_other.mon:
            add_mon = True

            for i in range(len(new_pl.mon)):
                try:
                    new_pl.mon[i] += new_mon
                    add_mon = False
                    break

                except NonSimMonError:
                    pass

            if add_mon: new_pl.append_mon(new_mon)

        for i in range(len(new_pl.mon)):
            c_mon = 0

            for j in range(i, len(new_pl.mon)):
                if i != j:
                    try:
                        new_pl.mon[i] = new_pl.m(i) + new_pl.m(j-c_mon)

                        del new_pl.mon[j-c_mon]
                        c_mon += 1

                    except NonSimMonError: pass

        if not normal_call:
            return new_pl.normal()

        else:
            return new_pl

#-------------------------------------------------------------------------------
    def __sub__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__sub__.__name__}: {type(other)}"

        return self + (-other)

#-------------------------------------------------------------------------------
    def __mul__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__mul__.__name__}: {type(other)}"

        new_pl = Pol()
        pol_other = other

        if isinstance(other, (float, int)):
            pol_other = Pol(other)

        elif isinstance(other, Mon):
            pol_other = Pol([other])

        for mon in self.mon:
            for other_mon in pol_other.mon:
                new_pl.append_mon(mon * other_mon)

        return new_pl.normal()

#-------------------------------------------------------------------------------
    def __truediv__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__truediv__.__name__}: {type(other)}"

        new_pl = Pol()
        pol_other = other

        if isinstance(other, (float, int)):
            pol_other = Pol(other)

        elif isinstance(other, Mon):
            pol_other = Pol([other])

        if len(other) == 1:
            for mon in self.mon:
                new_pl.append_mon(mon / pol_other.fm())

            return new_pl.normal()

        else:
            raise ImpossibleDivError

#-------------------------------------------------------------------------------
    def __pow__(self, power, modulo=None):
        assert isinstance(power, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__pow__.__name__}: {type(power)}"

        if isinstance(power, (float, int)):
            if int(power) != power: raise NonIntPowError
            pol_power = Pol(power)

        elif isinstance(power, Mon):
            if power.lt != MON_DICT: raise NonIntPowError
            pol_power = Pol(power.num)

        else:
            if len(power) != 1 and len(self) != 1: raise NonIntPowError
            pol_power = power

        if len(self) != 1:
            mon = pol_power.fm()
            if mon.lt != MON_DICT or int(mon.num) != mon.num:
                raise NonIntPowError
            result = self.copy()

            for i in range(int(mon.num) - 1):
                result *= self
            return result.normal()

        else:
            # Calls the __pow__ method of Mon
            return Pol(self.fm() ** pol_power)

#-------------------------------------------------------------------------------
    def __neg__(self):
        for i in range(len(self)):
            self[i] = -self[i]

        return self

#-------------------------------------------------------------------------------
    def __len__(self):
        return len(self.mon)

#-------------------------------------------------------------------------------
    def __gt__(self, other, lt_call = False):
        """
        If the other element is a monomial or a number the comparison is
        impossible len(self) != 1

        If the comparison is done between polynomials, the comparison will be
        true only if:
            - The polynomials have the same length
            - All the monomials have a similar counterpart
            - All of the monomials must be equal or greater than their
              counterpart
            - There must be at least one monomial greater

            In all other scenarios it's impossible to determine which is
            greater 
        """
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__gt__.__name__}: {type(other)}"

        if len(self) != 1 and isinstance(other, (int, float, Mon)):
            raise ImpossibleComparisonError

        elif isinstance(other, (int, float, Mon)):
            return self.fm() < other

        else:
            av_pos = []
            comparisons = []

            if len(self) != len(other):
                raise ImpossibleComparisonError

            for i in self.mon:
                if i is Pol and len(i) != 1:
                    raise ImpossibleComparisonError

                mon_pos = other.has_sim(i, av_pos)
                if mon_pos is None:
                    raise ImpossibleComparisonError

                other_mon = other.m(mon_pos)

                comparisons.append([i == other_mon, i > other_mon])
                av_pos.append(mon_pos)

            has_maj = False
            for i in comparisons:

                # if i < other_mon
                if (not i[0]) and (not i[1]):
                    if not lt_call:
                        return not self.__le__(other, True)

                    else:
                        raise ImpossibleComparisonError

                elif i[1]:
                    has_maj = True

            return has_maj

#-------------------------------------------------------------------------------
    def __ge__(self, other, lt_call = False):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__ge__.__name__}: {type(other)}"

        if self == other:
            return True

        return self.__gt__(other, lt_call)

#-------------------------------------------------------------------------------
    def __eq__(self, other):
        assert isinstance(other, (int, float, Mon, Pol)) or other is None,\
          f"Invalid type for {self.__eq__.__name__}: {type(other)}"

        if isinstance(other, (float, int)):
            if len(self) != 1:
                return False

            return self.fm() == other

        elif type(other) is Mon:
            return other == self  # Calls the __eq__ dunder of Mon

        elif isinstance(other, Pol):
            for i in self.mon:
                if i not in other.mon:
                    return False

            return True

        else:
            return False

#-------------------------------------------------------------------------------
    def __lt__(self, other, gt_call = False):
        """
        If the other element is a monomial or a number the comparison is
        impossible if len(self) != 1

        If the comparison is done between polynomials, the comparison will be
        true only if:
            - The polynomials have the same length
            - All the monomials have a similar counterpart
            - All of the monomials must be equal or minor than their
              counterpart
            - There must be at least one minor monomial

            In all other scenarios it's impossible to determine which is
            greater 
        """
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__lt__.__name__}: {type(other)}"

        if len(self) != 1 and isinstance(other, (int, float, Mon)):
            raise ImpossibleComparisonError

        elif isinstance(other, (int, float, Mon)):
            return self.fm() < other

        else:
            av_pos = []
            comparisons = []

            if len(self) != len(other):
                raise ImpossibleComparisonError

            for i in self.mon:
                if i is Pol and len(i) != 1:
                    raise ImpossibleComparisonError

                mon_pos = other.has_sim(i, av_pos)
                if mon_pos is None:
                    raise ImpossibleComparisonError

                other_mon = other.m(mon_pos)

                comparisons.append([i == other_mon, i < other_mon])
                av_pos.append(mon_pos)

            has_maj = False

            for i in comparisons:

                # if i > other_mon
                if (not i[0]) and (not i[1]):
                    if not gt_call:
                        return not self.__ge__(other, True)

                    else:
                        raise ImpossibleComparisonError

                elif i[1]:
                    has_maj = True

            return has_maj

#-------------------------------------------------------------------------------
    def __le__(self, other, gt_call = False):
        assert isinstance(other, (int, float, Mon, Pol)),\
          f"Invalid type for {self.__le__.__name__}: {type(other)}"

        if self == other:
            return True

        return self.__lt__(other, gt_call)

#-------------------------------------------------------------------------------
    def __getitem__(self, key):
        return self.mon[key]

#-------------------------------------------------------------------------------
    def __setitem__(self, key, value):
        self.mon[key] = value

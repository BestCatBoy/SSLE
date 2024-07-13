import re
import string

class _Descriptor:

    def __set_name__(self, owner, name):
        self.name = '__' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

class Equation:

    form = _Descriptor()
    args_A = _Descriptor()
    args_B = _Descriptor()
    vars_X = _Descriptor()

    __alphabet = string.ascii_letters
    __vars = {}
    __first = True

    def __init__(self, form):

        self.form = form
        self.__verify_form(form)
        self.__form_convert()

        self.args_A = self.__get_args(self.form)[:-1]
        self.args_B = self.__get_args(self.form)[-1:]

        if Equation.__first:
            Equation.__vars = self.vars_X = self.__get_vars(form)
            Equation.__first = False

        else: self.vars_X = Equation.__vars

    def __form_convert(self):

        """ Convert the given form into one necessary for
            interaction with the equation """

        new_form = getattr(self, 'form')

        indexes = []
        offset = 1

        for ch in range(len(new_form)):
            if (new_form[ch] in '+-=') and (new_form[ch+1] in self.__alphabet):
                indexes.append(ch+offset)
                offset += 1
            else:
                indexes.append(None)

        indexes = list(set(indexes))

        if new_form[0] in self.__alphabet:
            indexes.insert(0, 0)

        indexes.remove(None)

        if len(indexes) != 0:
            offset = 0
            for index in indexes:
                new_form = f'{new_form[:index+offset]}1{new_form[index+offset:]}'
                if offset == 0 and indexes[0] == 0:
                    offset += 1

        setattr(self, 'form', new_form)

    @classmethod
    def __verify_form(cls, form):


        """ Check the correctness of the entered data

        The equation should have the form:
        a1x1 + a2x2 + ... + anxn = b

        And be a string """

        def check_repetitions_operators(form, comparasion):

            """ Check for operators in adjacent indexes """

            entry = False

            for char in form:
                if char in comparasion and entry:

                    return True
                    break

                else: entry = False

                if char in comparasion:
                    entry = True

        def check_repetitions_vars(form):

            """ Check for duplicate variables """

            return len(cls.__get_vars(form)) != len(set(cls.__get_vars(form)))

        if not isinstance(form, str):
            raise TypeError("Equation should be represented by a string")

        elif (
            sum([True if form[i] in '0123456789' and form[i+1] in '+-' else
            False for i in range(len(form)-1)]) or
            '=' not in list(form) or
            form[0] in '+=' or
            form[form.index('=')-1] not in cls.__alphabet or
            check_repetitions_operators(form, '+-') or
            check_repetitions_operators(form, cls.__alphabet) or
            check_repetitions_vars(form)):

            raise SyntaxError(
                "Equation should have the form: a1x1 + a2x2 + ... + anxn = b")

    @classmethod
    def __get_args(cls, form):

        """ Get the vector of arguments (multipliers of unknown variables) """

        separators = '|'.join(cls.__alphabet)
        numbers = re.split(re.compile(separators), form)
        numbers[0] = float(numbers[0])

        for ch in range(1, len(numbers)):
            if numbers[ch][0] != '-':
                numbers[ch] = numbers[ch][1:]
            numbers[ch] = float(numbers[ch])

        return numbers

    @classmethod
    def __get_vars(cls, form):

        """ Get a vector with symbols of unknown variables """

        return list(re.compile('[^a-zA-Z]').sub('', form))

    @classmethod
    def system(cls, list_of_equations):

        """ Get a system of equations in the form of a dictionary
        divided into matrices A, B and X """

        system_dict = {'A': [obj.args_A for obj in list_of_equations],
        'X': cls.__vars,
        'B': [obj.args_B for obj in list_of_equations]}

        return system_dict
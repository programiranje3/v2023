#%%
"""
LAB 5, class Passenger
"""

"""
Create the Passenger class with the following methods:

- a constructor (__init__()) that receives four input arguments that are used to 
  initialise the following 4 attributes:
     - name - the passenger's name and surname
     - country - the passenger's country of origin
     - passport - the passenger's passport number
     - is_COVID_safe - a boolean indicator variable; it is true if the passenger is vaccinated 
     or has recently been tested negative; the default value of this argument is False

- get and set methods for the *passport* attribute (using appropriate decorators);
  designate this attribute as private and assure that it is a string of length 6,
  consisting of digits only.
  
- a method that returns a string representation of a Passenger object (__str__())

- a method (update_COVID_safe) that sets *is_COVID_safe* based on the value of its input parameters: 
  - evidence type: a string that should be either 'vaccinated' or 'tested_negative' (case insensitive)
  - evidence date: the date of vaccination / PCR test, as datetime value; if given as a string, it is 
  expected to be in the following format: %d/%m/%Y
  The method sets *is_COVID_safe* to True if:
  - the (last) vaccination was within the last 365 days OR
  - the negative test is not older than 3 days    
  Note: for datetime formatting codes, check this table:
  https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

- class method covid_free_Aussie_passenger for creating a passenger from Australia who is COVID safe
  (alternative constructor); the method receives the passenger's name and passport number.

- a method that checks for equality of the given Passenger object and another object
  that is passed to the method as its input parameter (__eq__()); two passenger objects
  are considered the same if they are citizens of the same country and have the same passport number
"""

#%%

from sys import stderr
from datetime import datetime

class Passenger:

    def __init__(self, name, country, passport, is_COVID_safe=False):
        self.name = name
        self.origin = country
        self.passport = passport
        self.is_COVID_safe = is_COVID_safe

    @property
    def passport(self):
        if not hasattr(self, '_Passenger__passport'):
            self.__passport = None
        return self.__passport

    @passport.setter
    def passport(self, value):
        if isinstance(value, str) and len(value) == 6 and all([ch.isdigit() for ch in value]):
            self.__passport = value
            return
        if isinstance(value, int) and len(str(value)) == 6:
            self.__passport = str(value)
            return
        stderr.write(f"Error occurred when trying to set passport value: wrong input ({value})\n")


    def __str__(self):
        passenger_str = f"Passenger {self.name}, from {self.origin}, "
        passenger_str += f"with passport {self.passport if self.passport else 'unknown'}, and "
        passenger_str += f"COVID status: {'safe' if self.is_COVID_safe else 'unsafe'}"
        return passenger_str

    @classmethod
    def covid_free_Aussie_passenger(cls, name, passport):
        return cls(name, "Australia", passport, True)

    def __eq__(self, other):
        if isinstance(other, Passenger):
            return False

        if self.origin and other.origin and self.passport and other.passport:
            return self.origin == other.origin and self.passport == other.passport

        stderr.write("Cannot compare the two  passenger objects as at least one of "
                     "the objects missing the data required for comparison\n")

    def update_COVID_safe(self, evidence_type, evidence_date):
        if evidence_type.lower() not in ['vaccinated', 'tested_negative']:
            stderr.write("update_COVID_safe: wrong value for the 'evidence type' parameter - cannot proceed!\n")
            return
        if not isinstance(evidence_date, (str, datetime)):
            stderr.write("update_COVID_safe: wrong value for the 'evidence date' parameter - cannot proceed!\n")
            return
        if isinstance(evidence_date, str):
            evidence_date = datetime.strptime(evidence_date, '%d/%m/%Y')
        dt_delta = datetime.now() - evidence_date
        self.is_COVID_safe = (evidence_type == 'vaccinated' and dt_delta.days < 365) or \
                (evidence_type == 'tested_negative' and dt_delta.days < 3)



if __name__ == '__main__':

    bob = Passenger("Bob Smith", "Serbia", "123456", True)
    john = Passenger("John Smith", "Spain", 987656, True)
    jane = Passenger("Jane Smith", "Italy", "987659")
    mike = Passenger.covid_free_Aussie_passenger("Mike Brown", "123654")

    print("PASSENGERS DATA:\n")
    print(bob)
    print(john)
    print(jane)
    print(mike)

    print("\nPASSENGERS DATA AFTER UPDATING COVID STATUS:\n")
    jane.update_COVID_safe('vaccinated', '15/01/2023')
    print(jane)

    mike.update_COVID_safe('tested_negative', '31/10/2023')
    print(mike)

    print()
    print("Checking if 'bob' and 'john' refer to the same passenger")
    print(bob == john)
    print("Checking if 'john' and 'johnny' refer to the same passenger")
    johnny = Passenger("Johnny Smith", "Spain", 987656, False)
    print(john == johnny)

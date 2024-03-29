#%%
"""
LAB 6, class Passenger
"""

#%%
"""
Modify the Passenger class from Lab5 as follows:

In addition to the existing attributes, the class should also have the following attributes:
- airfare - the price the passenger has paid for the flight
- checked_in - a boolean indicator, true if the passenger has checked in 
- services - the attribute represents a list of flight services available to the passenger; 
  these services are expected to be instances of the FlightService enumeration.

The following methods of the Passenger class need to be revised:

- constructor (__init__()) - it receives 6 input arguments, one for each attribute except the 
  *services* attributes. The arguments for the passenger's name, country, and passport 
  have to be specified; the arguments for *checked_in* and *is_COVID_safe* are False by default;
  the argument for *airfare* is None by default. The *services* attribute should be initialised 
  to an empty list.

- the property (getter) method for the *passport* attribute is done more in the Pythonic style, known as 
  "easier to ask for forgiveness than permission" or EAFP 

- a method that returns a string representation of a given Passenger object (__str__()) so that it describes 
  the passenger with the extended set of attributes.

Finally, the following new methods should be added:

- get and set methods (using appropriate decorators) for the *airfare* attribute; the attribute 
  should be made private; the set method: 
  i) should assure that a positive numeric value is assigned to this attribute, and 
  ii) should be able to handle both a float and a string value as the input argument

- get and set methods (using appropriate decorators) for the *checked_in* attribute; the attribute 
  should be made private; the set method should assure that a passenger can check in only if they 
  are COVID safe and have paid the airfare (*airfare* attribute is not None)
"""

#%%

from datetime import datetime, timedelta
from sys import stderr
from lab6.flight_enums import FlightService

class Passenger:

    def __init__(self, name, country, passport, is_covid_safe=False, checked_in=False, airfare=None):
        self.name = name
        self.origin = country
        self.passport = passport
        self.is_COVID_safe = is_covid_safe
        self.airfare = airfare
        self.checked_in = checked_in
        self.services = []

    @property
    def passport(self):
        try:
            return self.__passport
        except AttributeError:
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
        print(f"Invalid passport number ({value})")

    @property
    def airfare(self):
        try:
            return self.__airfare
        except AttributeError:
            self.__airfare = None
            return self.__airfare

    @airfare.setter
    def airfare(self, value):
        if not isinstance(value, (float, int, str)):
            stderr.write(f"Error! A value of inadequate type {type(value)} passed to the airfare setter.\n")
            return
        if isinstance(value, (int, str)):
            try:
                value = float(value)
            except ValueError as err:
                stderr.write(f"An error occurred while transforming airfare value into float:\n{err}\n")
                return
        if value > 0:
            self.__airfare = value
        else:
            stderr.write(f"Error! Incorrect value {value} passed to the airfare setter\n")

    @property
    def checked_in(self):
        return self.__checked_in

    @checked_in.setter
    def checked_in(self, value):
        # Option 1
        # self.__checked_in = value and self.is_COVID_safe and self.airfare
        # Option 2
        self.__checked_in = all([value, self.is_COVID_safe, self.airfare])

    def __str__(self):
        passenger_str = f"Passenger {self.name}, from {self.origin}, "
        passenger_str += f"with passport {self.passport if self.passport else 'unknown'}\n"
        passenger_str += f"\tCOVID status: {'safe' if self.is_COVID_safe else 'unsafe'}\n"
        passenger_str += f"\tchecked in: {'yes' if self.checked_in else 'not yet'}\n"
        passenger_str += f"\tairfare: {self.airfare if self.airfare else 'not paid yet'}\n"
        passenger_str += f"\textra services: {self.get_services_as_str(self.services)}"
        return passenger_str

    @staticmethod
    def get_services_as_str(services):
        return ", ".join([service.value for service in services]) if len(services) > 0 else "none"

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

    @classmethod
    def covid_free_Aussie_passenger(cls, name, passport):
        return cls(name, 'Australia', passport, True)

    def __eq__(self, other):
        if isinstance(other, Passenger):
            return False
        if self.passport and other.passport and self.origin and other.origin:
            return other.passport == self.passport and other.origin == self.origin
        else:
            print(f"Required data is missing for at least one passenger -> Cannot verify identity")
            return False


#%%
"""
Create the EconomyPassenger class that extends the Passenger class and has:

- method add_service_selection that receives a dictionary where keys are services the passenger has bought
  while values are the prices paid for those services. The services should be added to the passenger's 
  *services* list, while the prices should be used to increase the value of the *airfare* attribute, 
  BUT only if the main airfare has been paid.
  The method should also print a report about the added services and the resulting increase in the airfare. 
  Note: keys in the input dictionary are expected to be instances of the FlightService enumeration.  

- overridden __str__ method so that it first prints "Economy class passenger" and then the available information 
  about the passenger
"""

#%%

class EconomyPassenger(Passenger):

    def add_service_selection(self, services_dict):
        if not self.airfare:
            stderr.write(f"Passenger {self.name} has not paid the airfare and thus cannot buy extra services\n")
            return

        extra_total = 0
        services_to_add = []
        for service, price in services_dict.items():
            services_to_add.append(service)
            extra_total += price

        self.services.extend(services_to_add)
        print(f"Passenger {self.name} ({self.passport}) bought the following extra services:\n"
              f"{self.get_services_as_str(services_to_add)}")

        self.airfare += extra_total
        print(f"This resulted in the total cost being increased by {extra_total} to the total amount of {self.airfare}")

    def __str__(self):
        return "Economy class passenger " + super().__str__()


#%%
"""
Create class BusinessPassenger that extends the Passenger class and has:

- the constructor (__init__()) that receives the same arguments as the constructor of the upper class
  plus services to be assigned to the *services* attribute. This additional argument should be a tuple 
  of either strings (service names) or elements of the FlightService enumeration; its default value
  is FlightService.UNSPECIFIED. The method should check the validity of the tuple elements before adding 
  them to the *services* attribute. 
  Important: the constructor should be written in a way that makes the class ready for multiple inheritance.

- overridden __str__ method so that it first prints "Business class passenger" and then 
  the available information about the passengers

"""


#%%

class BusinessPassenger(Passenger):

    def __init__(self, services=(FlightService.UNSPECIFIED,), **kwargs):
        super().__init__(**kwargs)

        for s in services:
            if isinstance(s, FlightService):
                self.services.append(s)
            elif isinstance(s, str) and FlightService.valid_service_str(s):
                self.services.append(FlightService.get_service_from_str(s))

    def __str__(self):
        return "Business class passenger " + super().__str__()



#%%

if __name__ == '__main__':

    jim = EconomyPassenger("Jim Jonas", 'UK', '123456', airfare=450, is_covid_safe=True)
    print(jim)
    print()

    # Add extra services to Jim
    extra_services = {
        FlightService.REFRESHMENTS: 10,
        FlightService.ONBOARD_MEDIA: 15
    }
    jim.add_service_selection(extra_services)
    print()

    bob = EconomyPassenger("Bob Jones", 'Denmark', '987654')
    print(bob)
    print()

    mike = BusinessPassenger(name="Mike Stone", country="USA",
                             passport='234567', is_covid_safe=True,
                             services=(FlightService.PRIORITY_BOARDING, FlightService.ONBOARD_WIFI))
    print(mike)
    print()

    brian = BusinessPassenger(name="Brian Brown", country="UK",
                              passport='546234', is_covid_safe=True,
                              services=("priority boarding", "onboard media", "drinks"))
    print(brian)



#%%
"""
LAB 6, class Flight
"""

"""
Modify the Flight class from Lab5 as follows:

In addition to the flight_num, departure, and passengers attributes, the class should also have 
the following attributes:
- route - the route of the flight as a tuple of the form (origin, destination)
- operated_by - the company that operates the flight

The following methods of the Flight class need to be revised:

- the constructor (__init__()) - it should receive 4 input arguments for the *flight_num*, *departure*,
  *route*, and *operated_by* attributes; the arguments for the *route* and *operated_by* attributes have default 
  value None; the *passengers* attribute is initialised to an empty list

- the set method for the *departure* attribute, so that it properly handles situations when departure date 
  and time are given as a string in an unknown format (that is, in the format other than the *departure_format*)
  
- the property (getter) method for the *departure* attribute is done more in the Pythonic style, known as 
  "easier to ask for forgiveness than permission" or EAFP 

- the method that returns a string representation of the given Flight object (__str__()) so that it describes 
  the flight with the extended set of attributes

Furthermore, the following new methods should be added:

- get and set methods (using appropriate decorators) for the *route* attribute; the set method
  should allow for different ways of setting the route, that is, it should be able to handle input 
  value given as a list or a tuple (of two elements) or a string with the origin and destination 
  separated by a comma (Belgrade, Rome), a hyphen (Belgrade - Rome), or a '>' char (Belgrade > Roma)
  (Hint: consider using split method from the re (regular expressions) module)

- class method from_dict() for creating a Flight object (alternative constructor) out of the flight-related 
  data provided as a dictionary (the only input argument) with the following keys: 
  fl_num, departure, origin, destination, operator. 
  Consider that the dictionary might not contain all the expected items, that is, some dictionary keys might 
  not match the expected ones; in such a case, the method prints the keys that are available and creates a 
  Flight instance with the available data 
  
- a generator method that generates a sequence of passengers who have not yet checked in; the method should also 
  print the number of such passengers.

- a generator method that generates a sequence of candidate passengers for an upgrade to the business class; 
  those are the passengers of the economy class whose airfare exceed the given threshold (input parameter) 
  and who have checked in for the flight; the generated sequence should consider the passengers airfare, 
  so that those who paid more are prioritised for the upgrade option.

"""

#%%

from datetime import datetime, date
from sys import stderr
from lab6.passenger import Passenger, EconomyPassenger, BusinessPassenger


class Flight:

    departure_format = "%Y-%m-%d %H:%M"

    def __init__(self, flight_num, departure, route=None, operator=None):
        self.flight_num = flight_num
        self.departure = departure
        self.route = route
        self.operated_by = operator
        self.passengers = list()

    @classmethod
    def from_dict(cls, flight_dict):
        # fl_num, departure, origin, destination, operator
        def value_or_none(key):
            return flight_dict[key] if key in flight_dict.keys() else None

        try:
            return cls(flight_dict['fl_num'],
                       flight_dict['departure'],
                       (flight_dict['origin'], flight_dict['destination']),
                       flight_dict['operator'])
        except KeyError as err:
            stderr.write(f"Could not create a complete flight object due to the missing flight data: {err}\n")
            available_keys = ({'fl_num', 'departure', 'origin', 'destination', 'operator'} &
                              set(flight_dict.keys()))
            stderr.write(f"Instead, a flight object will be created with the following data items: "
                         f"{', '.join(available_keys)}\n")
            return cls(value_or_none('fl_num'),
                       value_or_none('departure'),
                       (value_or_none('origin'), value_or_none('destination')),
                       value_or_none('operator'))

    @property
    def departure(self):
        try:
            return self.__departure
        except AttributeError:
            self.__departure = None
            return self.__departure

    @departure.setter
    def departure(self, value):
        if not isinstance(value, (date, datetime, str)):
            stderr.write(f"departure setter: expected datetime or str value, got {type(value)}: cannot proceed\n")
            return
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, Flight.departure_format)
            except ValueError as err:
                stderr.write(f"An error occurred while parsing the departure date and time:\n{err}\n")
                return
        if value > datetime.now():
            self.__departure = value
        else:
            stderr.write("departure setter: departure date must be some future date\n")

    @property
    def route(self):
        try:
            return self.__route
        except AttributeError:
            self.__route = None
            return self.__route

    @route.setter
    def route(self, value):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            self.__route = tuple(value)
            return
        if isinstance(value, str):
            import re
            route_parts = re.split('[:->]', value) # alternative way for defining regular exapression: ':|-|>'
            if len(route_parts) == 2:
                self.__route = tuple(route_parts)
                return
        stderr.write("Error when setting route value\n")


    # Note that the following method has been modified as follows:
    # - in addition to receiving the passenger to be added, the method also receives the airfare paid by the passenger,
    #   which is, in case of successful addition to the list, assigned to the passenger's airfare attribute
    # - checking for valid COVID permit is now moved to the check-in setter
    def add_passenger(self, passenger, airfare):
        if not isinstance(passenger, Passenger):
            stderr.write("add passenger: the input argument is not of the type Passenger\n")
            return
        if passenger in self.passengers:
            stderr.write("add passenger: the passenger is already in the passenger list\n")
            return

        self.passengers.append(passenger)
        passenger.airfare = airfare
        print(f"Passenger {passenger.name} is successfully added to the passenger list")

    def __str__(self):
        flight_str = f"Flight number {self.flight_num}, "
        if self.departure:
            date_dep, time_dep = self.get_date_and_time_str()
            flight_str += f"scheduled for departure on {date_dep} at {time_dep}\n"
        else:
            flight_str += "departure date and time still not confirmed\n"
        if self.route:
            origin, dest = self.route
            flight_str += f"Route: {origin} -> {dest}\n"
        if self.operated_by:
            flight_str += f"Flight operator: {self.operated_by}\n"
        if len(self.passengers) == 0:
            flight_str += "No passengers checked in yet"
        else:
            flight_str += "Passengers:\n" + "\n".join([str(p) for p in self.passengers])
        return flight_str

    def get_date_and_time_str(self):
        date_str = datetime.strftime(self.departure, '%d/%m/%Y')
        time_str = datetime.strftime(self.departure, '%H:%M')
        return date_str, time_str

    def time_till_departure(self):
        if self.departure:
            depart_delta = self.departure - datetime.now()
            depart_days = depart_delta.days
            depart_hours, the_rest = divmod(depart_delta.seconds, 3600)
            depart_mins = the_rest // 60
            return depart_days, depart_hours, depart_mins

        print("Departure time is still unknown")
        return None

    def __iter__(self):
        self.__iter_counter = 0
        return self

    def __next__(self):
        if self.__iter_counter == len(self.passengers):
            raise StopIteration
        next_passenger = self.passengers[self.__iter_counter]
        self.__iter_counter += 1
        return next_passenger

    def not_checkedin_generator(self):
        # Option 1
        # not_checked_in_count = 0
        # for p in self.passengers:
        #     if not p.checked_in:
        #         not_checked_in_count += 1
        #         yield p
        # print(f"Still waiting for {not_checked_in_count} passengers to check in")
        #
        # Option 2
        not_checked_in = sum([not p.checked_in for p in self.passengers])
        print(f"Still waiting for {not_checked_in} passengers to check in")
        return (p for p in self.passengers if not p.checked_in)

    def candidates_for_upgrade_generator(self, threshold):
        candidates = []
        for p in self.passengers:
            if type(p) is EconomyPassenger and p.checked_in and p.airfare > threshold:
                candidates.append(p)

        # Option 1
        # for c in sorted(candidates, key=lambda passenger: passenger.airfare, reverse=True):
        #     yield c
        # Option 2
        return (c for c in sorted(candidates, key=lambda passenger: passenger.airfare, reverse=True))


#%%

if __name__ == '__main__':

    lh1411 = Flight('LH1411', '2024-03-20 6:50', ('Belgrade', 'Munich'))
    print(lh1411)
    print()

    lh992 = Flight('LH992', '2024-02-25 12:20', 'Belgrade -> Frankfurt', 'Lufthansa')
    print(lh992)
    print()

    lh1514_dict = {'fl_num':'lh1514',
                   'departure': '2023-12-30 16:30',
                   'operator': 'Lufthansa',
                   'origin': 'Paris',
                   'destination': 'Berlin'}

    lh1514 = Flight.from_dict(lh1514_dict)
    print(lh1514)
    print()

    jim = EconomyPassenger("Jim Jonas", 'UK', '123456')
    bill = EconomyPassenger("Billy Stone", 'USA', "917253", is_covid_safe=True)
    dona = EconomyPassenger("Dona Stone", 'Australia', "917251", is_covid_safe=True)
    kate = BusinessPassenger(name="Kate Fox", country='Canada', passport="114252", is_covid_safe=True)
    bob = BusinessPassenger(name="Bob Smith", country='UK', passport="123456")

    passengers = [jim, bill, dona, kate, bob]
    airfares = [450, 950, 1500, 1000, 475]
    for p, fare in zip(passengers, airfares):
        lh992.add_passenger(p, fare)

    print(f"\nAfter adding passengers to flight {lh992.flight_num}:\n")
    print(lh992)
    print()

    print("Last call to passengers who have not yet checked in!")
    # Option 1 (typically used one)
    for passenger in lh992.not_checkedin_generator():
        print(passenger)

    # # Option 2 (not ofter used, but illustrates how generators work)
    # g = lh992.not_checkedin_generator()
    # while True:
    #     try:
    #         print(next(g))
    #     except StopIteration:
    #         print("------- end of not-checked-in passengers list --------")
    #         break
    #
    # check in some economy class passengers to be able to test the next method
    dona.checked_in = True
    bill.checked_in = True

    # print()
    # print("Passengers offered an upgrade opportunity:")
    # # Option 1
    # for ind, passenger in enumerate(lh992.candidates_for_upgrade_generator(500)):
    #     print(f"{ind+1}. {passenger}")

    # print()
    # # Option 2
    # print("Candidates for upgrade to business class:")
    # g = lh992.candidates_for_upgrade_generator(500)
    # i = 1
    # try:
    #     while True:
    #         print(f"{i}. {next(g)}")
    #         i += 1
    # except StopIteration:
    #     print("--- end of candidates list ---")
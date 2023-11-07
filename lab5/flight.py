#%%
"""
LAB 5, class Flight
"""

"""
Create the Flight class with the following elements:

- class attribute *departure_format* representing the expected format for 
  the departure date and time; its value should be "%Y-%m-%d %H:%M"

- a constructor (__init__()) that receives two input parameters and uses them to initialise 
  *flight_num* (flight number) and *departure* (departure date and time) attributes; 
  it also initialises the *passengers* attribute (a list of objects of the Passenger class) 
  to an empty list

- get and set methods for the *departure* attribute (using appropriate decorators); 
  make this attribute private and assure that it is a datetime object that refers to 
  a moment in the future; if the input argument for the setter is string, it has to 
  be given in *departure_format* 

- a method for adding a passenger to the *passengers* list; the method adds a new passenger 
  only if the input parameter is of the Passenger class, if the passenger is not already 
  in the list, and if he/she is covid safe

- a method that returns a string representation of the given Flight object (__str__())

- a method that returns the time left till departure as a tuple of the form (days, hours, mins)

- methods for turning the given Flight object into an iterator (__iter__(), __next__()) over the 
  flight passengers (that is, elements of the *passengers* list)

"""

from datetime import datetime, date
from sys import stderr
from passenger import Passenger

class Flight:

    departure_format = '%Y-%m-%d %H:%M'

    def __init__(self, flight_number, departure_dt):
        self.flight_num = flight_number
        self.departure = departure_dt
        self.passengers = list()

    @property
    def departure(self):
        return self.__departure

    @departure.setter
    def departure(self, value):
        if not isinstance(value, (date, datetime, str)):
            stderr.write(f"departure setter: expected datetime or str value, got {type(value)}: cannot proceed\n")
            self.__departure = None
            return
        if isinstance(value, str):
            value = datetime.strptime(value, Flight.departure_format)
        if value > datetime.now():
            self.__departure = value
        else:
            self.__departure = None
            stderr.write("departure setter: departure date must be some future date\n")

    def add_passenger(self, passenger):
        if not isinstance(passenger, Passenger):
            stderr.write("add passenger: the input argument is not of the type Passenger\n")
            return
        if passenger in self.passengers:
            stderr.write("add passenger: the passenger is already in the passenger list\n")
            return
        if not passenger.is_COVID_safe:
            stderr.write("add passenger: the passenger does not have a valid evidence of being COVID safe\n")
            return

        self.passengers.append(passenger)
        print(f"Passenger {passenger.name} is successfully added to the passenger list")

    def __str__(self):
        flight_str = f"Flight number {self.flight_num}, "
        date_dep, time_dep = self.get_date_and_time_str(self.departure)
        flight_str += f"scheduled for departure on {date_dep} at {time_dep}"
        if len(self.passengers) == 0:
            flight_str += ", no passengers checked in yet"
        else:
            flight_str += ", passengers:\n" + "\n".join([str(p) for p in self.passengers])
        return flight_str

    @staticmethod
    def get_date_and_time_str(dt_obj):
        date_str = datetime.strftime(dt_obj, '%d/%m/%Y')
        time_str = datetime.strftime(dt_obj, '%H:%M')
        return date_str, time_str

    def time_till_departure(self):
        depart_delta = self.departure - datetime.now()
        depart_days = depart_delta.days
        depart_hours, the_rest = divmod(depart_delta.seconds, 3600)
        depart_mins = the_rest // 60
        return depart_days, depart_hours, depart_mins

    def __iter__(self):
        self.__next_index = 0
        return self

    def __next__(self):
        if self.__next_index == len(self.passengers):
            raise StopIteration
        next_item = self.passengers[self.__next_index]
        self.__next_index += 1
        return next_item


#%%


if __name__ == '__main__':

    lh1411 = Flight('LF1411', '2023-12-05 6:50')
    lh992 = Flight('LH992', '2023-11-25 12:20')

    print("\nFLIGHTS DATA:\n")
    print(lh1411)
    print()
    print(lh992)

    print()

    bob = Passenger("Bob Smith", "Serbia", "123456", True)
    john = Passenger("John Smith", "Spain", 987656, True)
    jane = Passenger("Jane Smith", "Italy", "987659")
    mike = Passenger.covid_free_Aussie_passenger("Mike Brown", "123654")

    for p in [bob, john, jane, mike]:
        lh1411.add_passenger(p)

    print("\nTRYING TO ADD A PASSENGER WHO IS ALREADY IN THE PASSENGERS LIST")
    lh1411.add_passenger(Passenger("J Smith", "Spain", "987656", True))
    print()

    print(f"\nFLIGHTS DATA AFTER ADDING PASSENGERS TO THE FLIGHT {lh1411.flight_num}:\n")
    print(lh1411)

    print()

    days, hours, mins = lh1411.time_till_departure()
    print(f"Time till departure of the flight {lh1411.flight_num}: {days} days, {hours} hours, and {mins} minutes")

    print()
    print("\nPASSENGERS ON FLIGHT LH1411 (iter / next):")
    passengers_iter = iter(lh1411)
    try:
        while True:
            print(next(passengers_iter))
    except StopIteration:
        print("No more passengers")

    print()
    print("\nPASSENGERS ON FLIGHT LH1411 (FOR loop):")
    for p in iter(lh1411):
        print(p)



# Activity class 

from datetime import date, timedelta

ACTIVITY_ATTRIBUTES = ['number', 'label', 'description',
                       'prerequisites', 'dependants', 'child', 'parent']

TIME_ATTRIBUTES = ['start_date', 'end_date', 'duration']

# VALID_ACTIVITY_ATTRIBUTES = #Join all attribute lists

class Duration:
    fill_missing = True

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        #Check temporal attributes all exist
        # if fill_missing:
        self.comp_missing()

    def is_valid(self):
        for v in VALID_ACTIVITY_ATTRIBUTES:
            if not self._check_(name)[0]:
                return False

    def comp_missing(self):
        if not all([hasattr(self, k) for k in TIME_ATTRIBUTES]):
            if hasattr(self, 'start_date') and hasattr(self, 'end_date'):
                setattr(self, 'duration', self.end_date - self.start_date)
            elif hasattr(self, 'duration') and hasattr(self, 'end_date'):
                setattr(self, 'start_date', self.end_date - self.duration)
            elif hasattr(self, 'duration') and hasattr(self, 'start_date'):
                setattr(self, 'end_date', self.start_date + self.duration)
            else:
                print('WARNING: Missing temporal attributes necessary for computation!')

    def __add__(self, other):
        if isinstance(other, int):
            other = timedelta(days=other)

        if isinstance(other, timedelta):
            # Assumes you want to add some number of days to the duration of the activity
            duration = other + self.duration
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)

        elif other.__class__.__name__ == 'timedelta':
            duration = other + self.duration
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)

        elif other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            # Assumes you are adding the second activity to the first
            duration = self.duration + other.duration
            end_date = self.end_date + other.duration
            return return_new(self.start_date, end_date, duration)

        else:
            print('Sorry! I dont know how to deal with that object yet!')
            return None

    def __sub__(self, other):
        if isinstance(other, int):
            other = timedelta(days=other)
        if isinstance(other, timedelta):
            # Assumes you want to add some number of days to the duration of the activity
            duration = self.duration - other
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)

        elif other.__class__.__name__ == 'timedelta':
            duration = self.duration - other
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)

        elif other.__class__.__name__ == 'Duration':
            # Assumes you are adding the second activity to the first
            duration = self.duration - other.duration
            self.end_date = self.end_date - other.duration
            return return_new(self.start_date, end_date, duration)

        else:
            print('Sorry! I dont know how to deal with that object yet')
            return None

    def __mul__(self, other):
        if isinstance(other, int):
            duration = self.duration * other
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)
        else:
            print('Sorry! I dont know how to deal with that object yet!')
            return None

    def __truediv__(self, other):
        if isinstance(other, int):
            duration = self.duration / other
            end_date = self.start_date + self.duration
            return return_new(self.start_date, end_date, duration)
        else:
            print('Sorry! I dont know how to deal with that object yet!')
            return None

    def __lt__(self, other):
        # <
        if other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            return self.end_date < other.start_date
        elif isinstance(other, date):
            return self.end_date < date

    def __eq__(self, other):
        """ we will use equal to mean some overlap """
        # =
        if other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            A = (other.end_date <=
                 self.end_date and other.start_date >= self.start_date)
            B = (other.end_date >=
                 self.end_date and other.start_date <= self.start_date)
            C = (other.end_date <=
                 self.end_date and other.end_date >= self.start_date)
            D = (other.start_date <=
                 self.end_date and other.start_date >= self.start_date)
            return any([A, B, C, D])

        elif isinstance(other, date):
            return self.end_date <= date and self.start_date >= date

    def __gt__(self, other):
        #>
        if other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            return self.end_date > other.start_date
        elif isinstance(other, date):
            return self.end_date > date

    def __ne__(self, other):
        """ Assumes you are checking there is no overlap"""
        # !=
        if isinstance(other, date):
            return not self.__eq__(other)
        elif other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            return not self.__eq__(other)
            #return self.start_date > other.end_date or self.end_date < other.end_date

    def __le__(self, other):
        """ Assumes you are checking if the end date comes after some date!"""
        # <=
        if other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            return self.end_date <= other.end_date
        elif isinstance(other, date):
            return self.end_date <= date

    def __ge__(self, other):
        """ Assumes you are checking if the start date comes after some date!"""
        # >=
        if other.__class__.__name__ == 'Duration' or other.__class__.__name__ == 'Activity':
            return self.start_date >= other.end_date
        elif isinstance(other, date):
            return self.start_date >= date

    def move(self, other):
        if isinstance(other, int):
            other = timedelta(days=other)

        if isinstance(other, timedelta):
            start_date = self.start_date + other
            end_date = start_date + self.duration
            return return_new(start_date, end_date, self.duration)
        else:
            print('Sorry! I dont know how to deal with that object yet!')
            return None

    # def __getattr__(self, name):
    #     try:
    #         return getattr(self, name)
    #     except AttributeError:
    #         raise AttributeError(
    #                 "Activity' object has no attribute '%s'" % name)

    def _check_(self, name):
        if hasattr(self, name):
            return True, getattr(self, name)
        else:
            return False, None


class Activity(Duration):
    parent = []
    child = []
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.__check_duration_info__()

    def __check_duration_info__(self):
        c = 0
        for k in TIME_ATTRIBUTES:
            if hasattr(self, k):
                c+=1
        if c > 1:
            super(Duration, self).__init__()
            self.comp_missing()
    
    def after(self, other, offset=0):
        """Changes the start and end date of the input activity to make it before this"""
        date_delta = other.end_date - self.start_date
        date_delta = date_delta + timedelta(offset)
        return self.move(date_delta)
        
    def before(self, other, offset=0):
        """Changes the start and end date of the input activity to make it after this"""
        date_delta = other.start_date - self.end_date
        date_delta = date_delta + timedelta(offset)
        return self.move(date_delta)

    def parallel(self, other, offset=0):
        """Changes the start and end date of the input activity to make it at the same time as this.
        You can also give and offset, assuming positive is later, negative is earlier"""
        date_delta = other.start_date - self.start_date
        date_delta = date_delta + timedelta(offset)
        return self.move(date_delta)

    def isbefore(self, other):
        """Assumes you want to check this activity is finished before some other or some date"""
        return self.__le__(other)

    def isafter(self, other):
        """Assumes you want to check this activity starts after some other or some date"""
        return self.__ge__(other)

    def isduring(self, other):
        """Assumes you want to check any overlap"""
        return self.__eq__(other)

    def setparent(self, other):
        self.parent.append(other)

    def setchild(self, other):
        self.child.append(other)



def return_new(S, E, D):
    return Activity(start_date=S, end_date=E, duration=D)


if __name__ == '__main__':

    A0 = Activity(start_date = date.today(), duration = timedelta(10))
    A1 = A0
    A1 = A1.move(30)
    
    A0.start_date
    A1.start_date

    A0 = A0.before(A1)
    A1.isbefore(A0)
    A1.isafter(A0)
    A2 = A0.move(-3)
    A0.isduring(A2)
    A1.isduring(A2)
    A2.isduring(A0)

    A0.start_date
    A1.end_date

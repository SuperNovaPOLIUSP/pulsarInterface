from Course import *

class TimePeriod(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idTimePeriod  (public)

     Defines if the Time Period range is a semester or a quarter.

    lengh  (public)

     Defines the year on wich the Time Period takes place.

    year  (public)

     Defines the order of the term lengh on the year, if it's the first or second
     semester or the first, second, third or fourth quarter.

    session  (public)

    """

    def __init__(self, length, year, session):
        """
         Constructor Method

        @param int length : Defines if the Time Period range is a semester or a quarter.
        @param int year : Defines the year on wich the Time Period takes place.
        @param int session : Defines the session of the term lengh on the year, if it's the first or second semester or the first, second, third or fourth quarter.
        @return  :
        @author
        """
        self.length = length
        self.year = year
        self.session = session
        
        
    def __str__(self):
        """
         Returns a string description of the TimePeriod. Eg: "First semester of 2013".

        @return string :
        @author
        """
        length_str = ("semester", "quarter")
        session_str = ("First", "Second", "Third", "Fourth")
        str_timePeriod = session_str[self.session -1] + length_str[self.length -1] + "of" + str(self.year)
        return str_timePeriod
        
        
    def pickById(self, idTimePeriod):
        """
         Returns a TimePeriod object once given its idTimePeriod.

        @param int idTimePeriod : Associated data base key.
        @return TimePeriod :
        @author
        """
        pass

    def remove(self):
        """
         Removes the time period's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        pass

    def store(self):
        """
         Creates or changes the time period's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        pass




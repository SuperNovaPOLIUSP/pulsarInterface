from tools.MySQLConnection import *

class TimePeriod(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idTimePeriod  (public)

     Defines if the Time Period range is a semester or a quarter.

    length  (public)

     Defines the year when the time period takes place.

    year  (public)

     Defines the order of the term length in the year, if it is the first or second
     semester or the first, second or third quarter.

    order  (public)

    """

    def __init__(self, length, year, session):
        """
         Constructor Method.

        @param int length : Defines if the Time Period range is a semester or a quarter.
        @param int year : Defines the year on wich the Time Period takes place.
        @param int order : Defines the order of the term lengh on the year, if it's the first or second semester or the first, second, third or fourth quarter.
        @return  :
        @author
        """
        self.length = length
        self.year = year
        self.session = session
        self.idTimePeriod = None
        

    def __str__(self):
        """
         Returns a string description of the TimePeriod. E.g. "First semester of 2013".

        @return string :
        @author
        """
        length_str = ("semester ", "quarter ")
        session_str = ("First ", "Second ", "Third ", "Fourth ")
        str_timePeriod = session_str[self.session -1] + length_str[self.length -1] + "of " + str(self.year)
        return str_timePeriod

    def __eq__(self, other):
        if not isinstance(other, TimePeriod):
            return False
        return self.__dict__ == other.__dict__


    @staticmethod
    def pickById(idTimePeriod):
        """
         Returns a TimePeriod object once given its idTimePeriod.

        @param int idTimePeriod : Associated data base key.
        @return TimePeriod :
        @author
        """
        cursor = MySQLConnection()
        query = 'SELECT * FROM timePeriod WHERE idTimePeriod = ' + str(idTimePeriod)
        try:
            timePeriod_sql = cursor.execute(query)[0]
        except:
            return None
        timePeriod = TimePeriod(timePeriod_sql[1], timePeriod_sql[2], timePeriod_sql[3])
        timePeriod.idTimePeriod = idTimePeriod
        return timePeriod

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing offers in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idTimePeriod
         > length
         > year
         > order
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. TimePeriod.find(length = 1, year = 2013, order = 1)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return TimePeriod[] :
        @author
        """
        cursor = MySQLConnection()
        timePeriodsData = cursor.find('SELECT length, year, session, idTimePeriod FROM timePeriod',kwargs)
        timePeriods = []
        for timePeriodData in timePeriodsData:
            timePeriod = TimePeriod(timePeriodData[0], timePeriodData[1], timePeriodData[2])
            timePeriod.idTimePeriod = timePeriodData[3]
            timePeriods.append(timePeriod)
        return timePeriods
        

    def store(self):
        """
         Creates or changes the time period's data in the database.
         
         Return: True if succesful or False otherwise

        @return bool :
        @author
        """
        if (self.length < 1 or self.session < 1):
            print "Lengh and session atributes cannot be lower than 1"
            return False
        cursor = MySQLConnection()
        try:
            values = [self.length, self.year, self.session]
        except:
            print "Values error"
            return False
        if self.idTimePeriod is None:
            possibleIds = self.find(length = self.length, year = self.year, session = self.session)
            if len(possibleIds) > 0:
                self.idTimePeriod = possibleIds[0].idTimePeriod
                return True
            query = "INSERT INTO timePeriod (length, year, session) VALUES " + str(tuple(values))
        else:
            query = "UPDATE timePeriod SET length = " +str(self.length) +", year = " +str(self.year) +", session = " +str(self.session) +" WHERE idTimePeriod = " +str(self.idTimePeriod)
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False

    def delete(self):
        """
         Deletes the time period's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        query = "DELETE FROM timePeriod WHERE idTimePeriod = " + str(self.idTimePeriod) + " AND length = " + str(self.length) + " AND year = " + str(self.year) + " AND session = " + str(self.session)
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False




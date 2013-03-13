from tools.MySQLConnection import MySQLConnection

class TimePeriodError(Exception):
    """
     Exception reporting an error in the execution of a TimePeriod method.

    :version:
    :author:
    """
    pass

class TimePeriod(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idTimePeriod  (private)

     Defines if the Time Period range is a semester or a quarter.

    length  (private)

     Defines the year when the time period takes place.

    year  (private)

     Defines the order of the term length in the year, if it is the first or second
     semester or the first, second or third quarter.

    order  (private)

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
    
        #Parameters verification.
        if length != 1 and length != 2:
            raise TimePeriodError("Parameter length must be: '1' if it is a semester or '2' if it is a quarter.")
        if not isinstance(year, (int, long)):
            raise TimePeriodError('Parameter year must be an int or a long.')
        if session != 1 and session != 2 and session != 3:
            raise TimePeriodError("Parameter session must be: '1' for first, '2' for second or '3' for third.")
        
        #Setting parameters.        
        self.length = length
        self.year = year
        self.session = session
        #Setting None paramenters.
        self.idTimePeriod = None
        
    def __eq__(self, other):
        if not isinstance(other, TimePeriod):
            return False
        return self.__dict__ == other.__dict__

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

    @staticmethod
    def pickById(idTimePeriod):
        """
         Returns a TimePeriod object once given its idTimePeriod.

        @param int idTimePeriod : Associated data base key.
        @return TimePeriod :
        @author
        """
        cursor = MySQLConnection()
        try:
            timePeriodData = cursor.execute('SELECT * FROM timePeriod WHERE idTimePeriod = ' + str(idTimePeriod))[0]
        except:
            return None
        timePeriod = TimePeriod(timePeriodData[1], timePeriodData[2], timePeriodData[3])
        timePeriod.idTimePeriod = timePeriodData[0]
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
        timePeriodsData = cursor.find('SELECT length, year, session, idTimePeriod FROM timePeriod',parameters)
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
       
        cursor = MySQLConnection()
        if self.idTimePeriod == None:
            possibleIds = self.find(length = self.length, year = self.year, session = self.session)
            if len(possibleIds) > 0:
                self.idTimePeriod = possibleIds[0].idTimePeriod
                return
            else:
                #Create this timePeriod.               
                query = "INSERT INTO timePeriod (length, year, session) VALUES " + str(tuple(values))
                cursor.execute(query)
                cursor.commit
                self.idTimePeriod = self.find(length = self.lenght, year = self.year, session = self.session)[0].idTimePeriod
        else:
            #Update timePeriod.
            query = "UPDATE timePeriod SET length = " +str(self.length) +", year = " +str(self.year) +", session = " +str(self.session) +" WHERE idTimePeriod = " +str(self.idTimePeriod)
            cursor.execute(query)
            cursor.commit() 
        return

    def delete(self):
        """
         Deletes the time period's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        if self.idTimePeriod != None:        
            cursor = MySQLConnection()
            query = "DELETE FROM timePeriod WHERE idTimePeriod = " + str(self.idTimePeriod) + " AND length = " + str(self.length) + " AND year = " + str(self.year) + " AND session = " + str(self.session)
            try:
                cursor.execute(query)
                cursor.commit()
            except:
                raise OfferError("Can't delete non saved object.")
        else:
            raise OfferError('No idOffer defined.')




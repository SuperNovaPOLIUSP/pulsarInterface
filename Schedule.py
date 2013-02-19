from tools.MySQLConnection import *
from datetime import timedelta
class Schedule(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associate database key.

    idSchedule  (public)

     The day of the week as it is written in the database's minitableDayOfTheWeek.

    dayOfTheWeek  (public)

     The starting time of the class (e.g. "18:00:00").

    start  (public)

     The ending time of the class (e.g. "03:14:15").

    end  (public)

     Specifies how often the lecture is held at this time (e.g. "weekly", "monthly",
     etc).

    frequency  (public)

    """

    def __init__(self, dayOfTheWeek, end, frequency, start):
        """
         Constructor method.

        @param string dayOfTheWeek : The day of the week as it is written in the database's minitableDayOfTheWeek.
        @param string end : The ending time of the class (e.g. "03:14:15").
        @param string frequency : Specifies how often the lecture is held at this time (e.g. "weekly", "monthly", etc).
        @param string start : The starting time of the class (e.g. "18:00:00").
        @return  :
        @author
        """
        if not isinstance(dayOfTheWeek, str):
            print 'dayOfTheWeek must be a string'
            return None
        if not isinstance(end, str):
            print 'end must be a string'
            return None
        if not isinstance(frequency, str):
            print 'frequency must be a string'
            return None
        if not isinstance(start, str):
            print 'start must be a string'
            return None
        self.dayOfTheWeek = dayOfTheWeek
        self.end = end
        self.frequency = frequency
        self.start = start
        self.idSchedule = None

    def __str__(self):
        """
         Returns the schedule written in a pattern.

        @return string :
        @author
        """
        return self.dayOfTheWeek + ' '+ self.start[:5] + ' - ' + self.end[:5] 
         
    @staticmethod 
    def pickById(idSchedule):
        """
         Returns a Schedule object once given its idSchedule.

        @param int idSchedule : Associated database key.
        @return Schedule :
        @author
        """
        cursor = MySQLConnection()
        query = '''select mtDotW.dayOfTheWeek, sch.end, frequency, sch.start  from schedule as sch
        join minitableDayOfTheWeek as mtDotW on mtDotW.idDayofTheWeek = sch.idDayOfTheWeek
        where sch.idSchedule = ''' + str(idSchedule)
        
        try:
            parameters = cursor.execute(query)
        except:
            return None
        if not parameters:
            return None
        schedule = Schedule(str(parameters[0][0]), str(parameters[0][1]), str(parameters[0][2]), str(parameters[0][3]))
        schedule.idSchedule = idSchedule
        return schedule

    @staticmethod
    def find(self, _kwargs):
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
         > idSchedule
         > dayOfTheWeek_equal or dayOfTheWeek_like
         > start_equal or start_like
         > end_equal or end_like
         > frequency_equal or frequency_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Schedule.find(dayOfTheWeek_equal = "monday", start_like = "09:")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        pass

    def store(self):
        """
         Creates or changes the schedule's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        #the object was not created with pickByID() or find()        
        if not self.idSchedule:
            pass

    def delete(self):
        """
         Deletes the schedule's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        if self.idSchedule != None:
            try:
                cursor = MySQLConnection()
                cursor.execute('DELETE FROM faculty WHERE idFaculty = ' + str(self.idFaculty))
                cursor.commit()
                return True
            except:
                pass
        return False



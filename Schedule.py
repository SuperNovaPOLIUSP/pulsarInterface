from tools.MySQLConnection import *
from tools.timeCheck import *
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
        if not isinstance(dayOfTheWeek, unicode):
            print 'dayOfTheWeek must be unicode'
            return None
        else:
            #check if dayOfTheWeek is in the database
            try:
                cursor = MySQLConnection()              
                if not cursor.execute('select idDayOfTheWeek from minitableDayOfTheWeek where dayOfTheWeek = "' + dayOfTheWeek + '" '):
                #if dayOfTheWeek isn't in the database
                    print "dayOfTheWeek must be in the database"
                    return None
            except:
                return None
        if not isinstance(end, str):
            if not isinstance(end, unicode):
               
                print 'end must be a string or unicode'
                return None
        if not isinstance(frequency, unicode):
            print 'frequency must be unicode'
            return None
        if not isinstance(start, str):
            if not isinstance(start, unicode):
                print 'start must be a string or unicode'
                return None
        
        #check if the parameter 'end' is in the format HH:MM:SS
        if not checkTimeString(end):
            print "Wrong end format"
            return None
        #check if the parameter 'start' is in the format HH:MM:SS
        if not checkTimeString(start):
            print "Wrong start format"
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
        return self.dayOfTheWeek.encode('utf8') + ' '+ self.start[:5] + ' - ' + self.end[:5] 
    
    @staticmethod 
    def pickById(idSchedule):
        """
         Returns a Schedule object once given its idSchedule.

        @param int idSchedule : Associated database key.
        @return Schedule :
        @author
        """
        cursor = MySQLConnection()
        query = '''select mtDotW.dayOfTheWeek, sch.end, sch.frequency, sch.start  from schedule as sch
        join minitableDayOfTheWeek as mtDotW on mtDotW.idDayofTheWeek = sch.idDayOfTheWeek
        where sch.idSchedule = ''' + str(idSchedule)
        
        try:
            values = cursor.execute(query)
        except:
            return None
        if not values:
            return None
        schedule = Schedule(values[0][0], str(values[0][1]), values[0][2], str(values[0][3]))
        schedule.idSchedule = idSchedule
        return schedule

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
        cursor = MySQLConnection()
        query = """SELECT mini.dayOfTheWeek, sch.end, sch.frequency, sch.start, sch.idSchedule FROM schedule AS sch
        JOIN minitableDayOfTheWeek AS mini ON mini.idDayOfTheWeek = sch.idDayOfTheWeek
        """
        schedulesData = cursor.find(query, kwargs)
        schedules = []
        for scheduleData in schedulesData:
            schedule = Schedule(scheduleData[0], str(scheduleData[1]), scheduleData[2], str(scheduleData[3]))
            schedule.idSchedule = scheduleData[4]
            schedules.append(schedule)
        return schedules
        

    def store(self):
        """
         Creates or changes the schedule's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        #check if dayOfTheWeek is in the database
        try:
            query = 'select idDayOfTheWeek from minitableDayOfTheWeek where dayOfTheWeek = "' + self.dayOfTheWeek + '" '
            idDayOfTheWeek = cursor.execute(query)
            if not idDayOfTheWeek:
            #if dayOfTheWeek isn't in the database
                print "dayOfTheWeek must be in the database"
                return False
            idDayOfTheWeek = idDayOfTheWeek[0][0]
        except:
            return False
        #check if end is a value time
        if not checkTimeString(self.end):
            print "Wrong end value"
            return False
        #check if start is a value time
        if not checkTimeString(self.start):
            print "Wrong start value"
            return False
        if self.idSchedule == None:
            #Search for idSchedule
            possibleIds = self.find(dayOfTheWeek_equal = self.dayOfTheWeek, end_equal = self.end, frequency_equal = self.frequency, start_equal = self.start)
            if not possibleIds :
                #If there is no idSchedule, then create row
                try:
                    query = 'INSERT INTO schedule (idDayOfTheWeek, end, frequency, start) VALUES(' + str(idDayOfTheWeek) + ', "' + self.end + '", "' + self.frequency + '", "' + self.start + '")'
                    cursor.execute(query)
                    cursor.commit()
                    self.idSchedule = self.find(dayOfTheWeek_equal = self.dayOfTheWeek, end_equal = self.end, frequency_equal = self.frequency, start_equal = self.start)[0].idSchedule                
                    return True
                except:
                    return False 
            else:
                self.idSchedule = possibleIds[0].idSchedule   #Since all results are the same schedule pick the first one.
                return True
        else:
            #If there is an idFaculty try to update row
            query = 'UPDATE schedule SET idDayOfTheWeek = ' + str(idDayOfTheWeek) + ', end = "' + self.end + '", frequency = "' + self.frequency + '" , start = "' + self.start + '" WHERE idSchedule = ' + str(self.idSchedule)
            try:
                cursor.execute(query)
                cursor.commit()
                return True
            except:
                return False 

    def delete(self):
        """
         Deletes the schedule's data in the database.
         
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        if self.idSchedule != None:
            cursor = MySQLConnection()
            dbobject = self.pickById(self.idSchedule)
            if not dbobject:
                print 'idSchedule must be in the database'
                return False
            if self.dayOfTheWeek != dbobject.dayOfTheWeek or self.end != dbobject.end or self.start != dbobject.start or self.frequency != dbobject.frequency:
                print 'Attributes do not match in the database'
                return False
            try:
                cursor.execute('DELETE FROM schedule WHERE idSchedule = ' + str(self.idSchedule))
                cursor.commit()
                self = None
                return True
            except:
                pass
        print "object has no idSchedule"
        raise MySQLQueryError("")



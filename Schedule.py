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
        if not isinstance(dayOfTheWeek, unicode):
            print 'dayOfTheWeek must be unicode'
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
        split_end = end.split(":")          
        if len(split_end) == 3 and 0 < len(split_end[0]) < 3 and len(split_end[1]) == 2 and len(split_end[2]) == 2:
            #check 'end' hour
            if  int(split_end[0]) <0 or int(split_end[0])> 23:
                print "Wrong format in end, hour must be between 0 and 23"
                return None
            if len(split_end[0]) == 1:
                split_end[0] = "0" + split_end[0]
            #check 'end' minute
            if int(split_end[1]) <0 or int(split_end[1])> 59:
                print "Wrong format in end, minute must be between 0 and 59"
                return None
            #check 'end' minute
            if int(split_end[2]) <0 or int(split_end[2])> 59:
                print "Wrong format in end, second must be between 0 and 59"
                return None
        else:
            print "end must be in format 'HH:MM:SS'"
            return None
        end = split_end[0] + ":" + split_end[1] + ":" + split_end[2]
        #check if the parameter 'start' is in the format HH:MM:SS
        split_start = start.split(":")          
        if len(split_start) == 3 and 0 < len(split_start[0]) < 3 and len(split_start[1]) == 2 and len(split_start[2]) == 2:
            #check 'start' hour
            if  int(split_start[0]) <0 or int(split_start[0])> 23:
                print "Wrong format in start, hour must be between 0 and 23"
                return None
            if len(split_start[0]) == 1:
                split_start[0] = "0" + split_start[0]
            #check 'start' minute
            if int(split_start[1]) <0 or int(split_start[1])> 59:
                print "Wrong format in start, minute must be between 0 and 59"
                return None
            #check 'start' minute
            if int(split_start[2]) <0 or int(split_start[2])> 59:
                print "Wrong format in start, second must be between 0 and 59"
                return None
        else:
            print "start must be in format 'HH:MM:SS'"
            return None
        start = split_start[0] + ":" + split_start[1] + ":" + split_start[2]
        

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
        scheduleData = cursor.find(query, kwargs)
        schedules = []
        for scheduleData in scheduleData:
            schedule = Schedule(scheduleData[0], str(scheduleData[1]), scheduleData[2], str(scheduleData[3]))
            schedule.idschedule = scheduleData[4]
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
                cursor.execute('DELETE FROM schedule WHERE idschedule = ' + str(self.idschedule))
                cursor.commit()
                return True
            except:
                pass
        return False



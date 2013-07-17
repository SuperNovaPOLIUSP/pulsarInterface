# coding: utf-8

from Course import *
from IdealTerm import *
import datetime
from tools.timeCheck import *

class CycleError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass



class Cycle(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idCycle  (public)

     Cycle's name.

    name  (public)

     Date of start of this cycle, in the form year-month-day “xxxx-xx-xx”. Start
     is defined as the start of the cycle in this University.

    startDate  (public)

     Date of the end of this cycle, in the form year-month-day “xxxx-xx-xx”.
     Its value is null if the cycle is not over. Over is defined as the last
     time this cycle was given in this University.

    endDate  (public)

     It represents the type of cycle, (e.g general area, basic cycle ...).

    cycleType  (public)

     Cycle Code (as defined by jupiter)

    cycleCode  (public)

     String representing the time period division ("quarter" or "semester")

    timePeriodType  (public)

     The cycle's faculty.

    faculty  (public)

     List of Idealterm where each one contains a set of mandatory courses of this
     cycle.

    mandatoryIdealTerms  (public)

     List of IdealTerm where each one contains a set of elective courses of this
     cycle.

    electiveIdealTerms  (public)

     Abbreviated cycle's name (e.g. Computing Engineering -> Computing).

    abbreviation  (public)

     Number of vacancies for this cycle.

    vacancyNumber  (public)

     Cycle's daily length (day-time, nigth-time,full-time)

    termLength  (public)

    """

    def __init__(self, name, cycleType, cycleCode, timePeriodType, startDate, termLength):
        """

        @param string name : Cycle's name
        @param string cycleType : It represents the type of cycle, (e.g general area, basic cycle,... ).
        @param string cycleCode : codigo da habilitação (vide jupiter)
        @param string timePeriodType : String representing the period division ("quarter" or "semester").
        @param startDate string : Date of the start of this cycle, in the form year-month-day “xxxx-xx-xx”.Start is defined as the first time this cycle was given in this University. 
        @param string termLength : Cycle's daily length (day-time, nigth-time,full-time)
        @return  :
        @author
        """
        if not isinstance(name, (str, unicode)):
            raise CycleError('Parameter name must be a string or unicode.')
        if not isinstance(cycleType, (str, unicode)):
            raise CycleError('Parameter cycleType must be a string or unicode.')            
        if not isinstance(cycleCode, (int, long)):
            raise CycleError('Parameter cycleCode must be an int or a long.')
        if timePeriodType != None:
            if not isinstance(timePeriodType, (str, unicode)):
                raise CycleError('Parameter timePeriodType must be a string or unicode, or None.')
        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or not checkDateString(startDate):
                raise CycleError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')
        if not isinstance(termLength, (int, long)):
            raise CycleError('Parameter termLength must be an int or a long.')


        self.name = name
        self.cycleType = cycleType
        self.cycleCode = cycleCode
        self.timePeriodType = timePeriodType
        self.startDate = str(startDate) 
        self.abbreviation = name
        self.termLength = termLength
        self.idCycle = None
        self.endDate = None
        self.mandatoryIdealTerms = None
        self.electiveIdealTerms = None
        
    def __eq__(self, other):
        if not isinstance(other, Cycle):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setEndDate(self, endDate):
        """

        @param string endDate : Date of the end of this cycle, in the form year-month-day “xxxx-xx-xx”. It's value is null if the cycle is not over. Over is defined as the last time this cycle was given in this University.
        @return  :
        @author
        """
        if endDate != None:
            if not isinstance(endDate,datetime.date):
                if not isinstance(endDate,(str,unicode)) or not checkDateString(endDate):
                    raise CourseError('Parameter endDate must be a datetime.date format or a string in the format year-month-day')
            self.endDate = str(endDate)
        else:
            self.endDate = endDate

    def setVacancyNumber(self, vacancyNumber):
        """
         

        @param int vancacyNumber : 
        @return  :
        @author
        """

        if not isinstance(vacancyNumber, (int, long)):
            raise CycleError('Parameter vacancyNumber must be a int or a long.')
        self.vacancyNumber = vacancyNumber
       

    def setAbbreviation(self, abbreviation):
        """
         

        @param string abbreviation : 
        @return  :
        @author
        """
        if not isinstance(abbreviation, (str, unicode)):    
            raise CycleError('Parameter abbreviation must be a string or unicode.')
        self.abbreviatio = abbreviation

    def completeMandatoryIdealTerms(self):
        """
         Completes the mandatoryIdealTerms list with the objects idealTerm related to the
         mandatories time period of this cycle.

        @return bool :
        @author
        """
        pass
        #TODO

    def completeElectiveIdealTerms(self):
        """
         Completes the electiveIdealTerms list with the objects idealTerm related to the
         electives time period of this cycle.

        @return bool :
        @author
        """
        pass
        #TODO

    @staticmethod
    def pickById(idCycle):
        """
         Returns a single cycle with the chosen ID.

        @param int idCycle : Associated data base key.
        @return Cycle :
        @author
        """
        cursor = MySQLConnection()  
        try:
            #Here get most of the cycles data
            cycleData = cursor.execute('SELECT curr.name,  mc.name, curr.cycleCode, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM cycle curr JOIN minitableCycleType mc ON curr.idCycleType = mc.idCycleType WHERE curr.idCycle = '+ str(idCycle))[0]
        except:
            return None
        #Now get the timePeriodType
        timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_cycle rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCycle = ' + str(idCycle)  + ' GROUP BY idCycle')
        if len(timePeriodType) > 0:
            timePeriodType = timePeriodType[0][0]
        else:
            timePeriodType = None

        cycle = Cycle(cycleData[0], cycleData[1], cycleData[2], timePeriodType, cycleData[3], cycleData[4])#name, cycleType, cycleCode, timePeriodType, startDate, termLength
        cycle.setVacancyNumber(cycleData[5])
        cycle.setEndDate(cycleData[6])
        cycle.setAbbreviation(cycleData[7])
        cycle.idCycle = idCycle
        return cycle

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
         > idCycle
         > name_equal or name_like
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         > cycleType
         > cycleCode
         > timePeriodType_equal or timePeriodType_like
         > abbreviation_equal or abbreviation_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Cycle.find(timePeriodTime_equal = "night", name_like = "Computer")

        @param dictionary _kwargs : 
        @return Curriculo[] :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        parameters['curr.idCycle'] = []
        for key in kwargs:
            if key.find('cycleType') != -1:
                if key.find('like') != -1:
                    parameters['mc.name_like'] = kwargs[key]
                else:
                    parameters['mc.name_equal'] = kwargs[key]
            elif key.find('timePeriodType') != -1:
                query = 'SELECT rcc.idCycle  FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_cycle rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length '
                if key.find('like') != -1:
                    query = query + 'WHERE ml.length like "%' + kwargs[key]  + '%" GROUP BY rcc.idCycle'
                else:
                    query = query + 'WHERE ml.length = "' + kwargs[key]  + '" GROUP BY rcc.idCycle'
                cyclesData = cursor.execute(query)
                if len(cyclesData) > 0:
                    parameters['curr.idCycle'].append([cycleData[0] for cycleData in cyclesData])

            elif key == 'idCycle':
                if isinstance(kwargs['idCycle'], list):
                    parameters['curr.idCycle'].append(kwargs['idCycle']) 
                else:
                    parameters['curr.idCycle'].append([kwargs['idCycle']])
            else:
                parameters['curr.' + key] = kwargs[key]

        if len(parameters['curr.idCycle']) > 0:
            #Now you join the idsCycle parameters allowing only the ones that belong to all the lists (execute an AND with them)
            finalIdCycleList = []
            for idCycle in parameters['curr.idCycle'][0]:
                belongToAll = True
                for idsCycle in parameters['curr.idCycle'][1:]:
                    if not idCycle in idsCycle:
                        belongToAll = False
                        break
                if belongToAll:
                    finalIdCycleList.append(idCycle)
            parameters['curr.idCycle'] = finalIdCycleList
        else:
            del parameters['curr.idCycle']

        cyclesData = cursor.find('SELECT curr.idCycle, curr.name,  mc.name, curr.cycleCode, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM cycle curr JOIN minitableCycleType mc ON curr.idCycleType = mc.idCycleType',parameters)
        cycles = []
        for cycleData in cyclesData:
            timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_cycle rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCycle = ' + str(cycleData[0])  + ' GROUP BY rcc.idCycle')
            if len(timePeriodType) > 0:
                timePeriodType = timePeriodType[0][0]
            else:
                timePeriodType = None
            
            cycle = Cycle(cycleData[1], cycleData[2], cycleData[3], timePeriodType, cycleData[4], cycleData[5])#name, cycleType, cycleCode, timePeriodType, startDate, termLength
            cycle.setVacancyNumber(cycleData[6])
            cycle.setEndDate(cycleData[7])
            cycle.setAbbreviation(cycleData[8])
            cycle.idCycle = cycleData[0]
            cycles.append(cycle)
        return cycles
        
        
    def store(self):
        """
         Alters the cycle's data in the data base.

        @return bool :
        @author
        """
        pass #I am not ready        
        if self.idCycle == None:
            cycles = Cycle.find(idCycle = self.idCycle, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, cycleType = self.cycleType, cycleCode = self.cycleCode, timePeriodType_equal = self.timePeriodType, abbreviation_equal = self.abbreviation)
            if len(cycles) > 0:
                self.idCycle = cycles[0].idCycle #Any cycle that fit those paramaters is the same as this cycle, so no need to save
                return
            else:
                
                
#         > idCycle
#         > name_equal or name_like
#         > startDate_equal or startDate_like
#         > endDate_equal or endDate_like
#         > cycleType
#         > cycleCode
#         > timePeriodType_equal or timePeriodType_like
#         > abbreviation_equal or abbreviation_like
         
         
                #Create this cycle
                query = "INSERT INTO cycle (name, cycleType, cycleCode" #FALTAM OS OBRIGATORIOS FACULTY(excluido) E TIMEPERIODTYPE
                values = ") VALUES('" +self.name +"', '" +str(self.cycleType) +"', '" +str(self.cycleCode)
                if self.startDate != None:
                    query += ", startDate"
                    values += ", " +self.startDate
                if self.endDate != None:
                    query += ", endDate"
                    values += ", " +self.endDate
                if self.abbreviation != None:
                    query += ", abbreviation"
                    values += ", " +self.endDate
                cursor.execute(query + values +")")
                cursor.commit()
                self.idCycle = Cycle.find(idCycle = self.idCycle, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, cycleType = self.cycleType, cycleCode = self.cycleCode, timePeriodType_equal = self.timePeriodType, abbreviation_equal = self.abbreviation)[0].idCycle 
        
        '''self.name
        self.curriculymType
        self.cycleCode
        self.timePeriodType
        self.idCycle
        self.startDate
        self.endDate
        self.mandatoryIdealTerms
        self.electiveIdealTerms
        self.abbreviation'''

    def delete(self):
        """
         Deletes the cycle's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        
        if self.idCycle != None:
            cursor = MySQLConnection()
            if self == Cycle.pickById(self.idCycle):
                cursor.execute('DELETE FROM cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_course_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_courseCoordination_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_academicProgram_cycle WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_course_cycle_course WHERE idCycle = ' + str(self.idCycle))
                cursor.execute('DELETE FROM rel_cycle_opticalSheet WHERE idCycle = ' + str(self.idCycle))
                cursor.commit()
            else:
                raise CourseError("Can't delete non saved object.")
        else:
            raise CourseError('idCycle not defined.')




# coding: utf-8

from Course import *
from IdealTerm import *
from Faculty import *
from tools.timeCheck import *

class CurriculumError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass



class Curriculum(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idCurriculum  (public)

     Curriculum's name.

    name  (public)

     Date of start of this curriculum, in the form year-month-day “xxxx-xx-xx”. Start
     is defined as the start of the curriculum in this University.

    startDate  (public)

     Date of the end of this curriculum, in the form year-month-day “xxxx-xx-xx”.
     Its value is null if the curriculum is not over. Over is defined as the last
     time this curriculum was given in this University.

    endDate  (public)

     It represents the type of curriculum, (e.g general area, basic cycle ...).

    curriculumType  (public)

     Curriculum Code (as defined by jupiter)

    curriculumCode  (public)

     String representing the time period division ("quarter" or "semester")

    timePeriodType  (public)

     The curriculum's faculty.

    faculty  (public)

     List of Idealterm where each one contains a set of mandatory courses of this
     curriculum.

    mandatoryIdealTerms  (public)

     List of IdealTerm where each one contains a set of elective courses of this
     curriculum.

    electiveIdealTerms  (public)

     Abbreviated curriculum's name (e.g. Computing Engineering -> Computing).

    abbreviation  (public)

     Number of vacancies for this curriculum.

    vacancyNumber  (public)

     Curriculum's daily length (day-time, nigth-time,full-time)

    termLength  (public)

    """

    def __init__(self, name, curriculumType, curriculumCode, timePeriodType, faculty, startDate, termLength):
        """

        @param string name : Curriculum's name
        @param string curriculumType : It represents the type of curriculum, (e.g general area, basic cycle,... ).
        @param string curriculumCode : codigo da habilitação (vide jupiter)
        @param string timePeriodType : String representing the period division ("quarter" or "semester").
        @param Faculty faculty : The curriculum's faculty.
        @param startDate string : Date of the start of this curriculum, in the form year-month-day “xxxx-xx-xx”.Start is defined as the first time this curriculum was given in this University. 
        @param string termLength : Curriculum's daily length (day-time, nigth-time,full-time)
        @return  :
        @author
        """
        if not isinstance(name, (str, unicode)):
            raise CurriculumError('Parameter name must be a string or unicode.')
        if not isinstance(curriculumType, (str, unicode)):
            raise CurriculumError('Parameter curriculumType must be a string or unicode.')            
        if not isinstance(curriculumCode, (int, long)):
            raise CurriculumError('Parameter curriculumCode must be an int or a long.')
        if timePeriodType != None:
            if not isinstance(timePeriodType, (str, unicode)):
                raise CurriculumError('Parameter timePeriodType must be a string or unicode, or None.')
        if faculty != None:
            if not isinstance(faculty, Faculty) or not Faculty.pickById(faculty.idFaculty) == faculty:
                raise CurriculumError('Parameter faculty must be a Faculty object that exists in the database.')
        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or not checkDateString(startDate):
                raise CurriculumError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')
        if not isinstance(termLength, (str, unicode)):
            raise CurriculumError('Parameter termLength must be a string or unicode.')


        self.name = name
        self.curriculumType = curriculumType
        self.curriculumCode = curriculumCode
        self.timePeriodType = timePeriodType
        self.faculty = faculty
        self.startDate = str(startDate) 
        self.abbreviation = name
        self.termLength = termLength
        self.idCurriculum = None
        self.endDate = None
        self.mandatoryIdealTerms = None
        self.electiveIdealTerms = None
        
    def __eq__(self, other):
        if not isinstance(other, Curriculum):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setEndDate(self, endDate):
        """

        @param string endDate : Date of the end of this curriculum, in the form year-month-day “xxxx-xx-xx”. It's value is null if the curriculum is not over. Over is defined as the last time this curriculum was given in this University.
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
            raise CurriculumError('Parameter vacancyNumber must be a int or a long.')
        self.vacancyNumber = vacancyNumber
       

    def setAbbreviation(self, abbreviation):
        """
         

        @param string abbreviation : 
        @return  :
        @author
        """
        if not isinstance(abbreviation, (str, unicode)):    
            raise CurriculumError('Parameter abbreviation must be a string or unicode.')
        self.abbreviatio = abbreviation

    def completeMandatoryIdealTerms(self):
        """
         Completes the mandatoryIdealTerms list with the objects idealTerm related to the
         mandatories time period of this curriculum.

        @return bool :
        @author
        """
        pass
        #TODO

    def completeElectiveIdealTerms(self):
        """
         Completes the electiveIdealTerms list with the objects idealTerm related to the
         electives time period of this curriculum.

        @return bool :
        @author
        """
        pass
        #TODO

    @staticmethod
    def pickById(idCurriculum):
        """
         Returns a single curriculum with the chosen ID.

        @param int idCurriculum : Associated data base key.
        @return Curriculum :
        @author
        """
        cursor = MySQLConnection()  
        try:
            #Here get most of the curricula data
            curriculumData = cursor.execute('SELECT curr.name,  mc.name, curr.curriculumCode, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM curriculum curr JOIN minitableCurriculumType mc ON curr.idCurriculumType = mc.idCurriculumType WHERE curr.idCurriculum = '+ str(idCurriculum))[0]
        except:
            return None
        #Now get the timePeriodType
        timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCurriculum = ' + str(idCurriculum)  + ' GROUP BY idCurriculum')
        if len(timePeriodType) > 0:
            timePeriodType = timePeriodType[0][0]
        else:
            timePeriodType = None
        #Now get the faculty
        facultyData = cursor.execute('SELECT rcf.idFaculty FROM curriculum curr JOIN rel_courseCoordination_curriculum rcc ON curr.idCurriculum = rcc.idCurriculum JOIN rel_courseCoordination_faculty rcf ON rcc.idCourseCoordination = rcf.idCourseCoordination  WHERE curr.idCurriculum = '+ str(idCurriculum))
        if len(facultyData) > 0:
            faculty = Faculty.pickById(facultyData[0][0])
        else:
            faculty = None

        curriculum = Curriculum(curriculumData[0], curriculumData[1], curriculumData[2], timePeriodType, faculty, curriculumData[3], curriculumData[4])#name, curriculumType, curriculumCode, timePeriodType, faculty, startDate, termLength
        curriculum.setVacancyNumber(curriculumData[5])
        curriculum.setEndDate(curriculumData[6])
        curriculum.setAbbreviation(curriculumData[7])
        curriculum.idCurriculum = idCurriculum
        return curriculum

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
         > idCurriculum
         > name_equal or name_like
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         > curriculumType
         > curriculumCode
         > timePeriodType_equal or timePeriodType_like
         > faculty
         > abbreviation_equal or abbreviation_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Curriculum.find(timePeriodTime_equal = "night", name_like = "Computer")

        @param dictionary _kwargs : 
        @return Curriculo[] :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        parameters['curr.idCurriculum'] = []
        for key in kwargs:
            if key.find('curriculumType') != -1:
                if key.find('like') != -1:
                    parameters['mc.name_like'] = kwargs[key]
                else:
                    parameters['mc.name_equal'] = kwargs[key]
            elif key == 'faculty':
                curriculaData = cursor.execute('SELECT curr.idCurriculum FROM curriculum curr JOIN rel_courseCoordination_curriculum rcc ON curr.idCurriculum = rcc.idCurriculum JOIN rel_courseCoordination_faculty rcf ON rcc.idCourseCoordination = rcf.idCourseCoordination WHERE rcf.idFaculty = ' + str(kwargs['faculty'].idFaculty))
                if len(curriculaData) > 0:
                    parameters['curr.idCurriculum'].append([curriculumData[0] for curriculumData in curriculaData])
            
            elif key.find('timePeriodType') != -1:
                query = 'SELECT rcc.idCurriculum  FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length '
                if key.find('like') != -1:
                    query = query + 'WHERE ml.length like "%' + kwargs[key]  + '%" GROUP BY rcc.idCurriculum'
                else:
                    query = query + 'WHERE ml.length = "' + kwargs[key]  + '" GROUP BY rcc.idCurriculum'
                curriculaData = cursor.execute(query)
                if len(curriculaData) > 0:
                    parameters['curr.idCurriculum'].append([curriculumData[0] for curriculumData in curriculaData])

            elif key == 'idCurriculum':
                if isinstance(kwargs['idCurriculum'], list):
                    parameters['curr.idCurriculum'].append(kwargs['idCurriculum']) 
                else:
                    parameters['curr.idCurriculum'].append([kwargs['idCurriculum']])
            else:
                parameters['curr.' + key] = kwargs[key]

        if len(parameters['curr.idCurriculum']) > 0:
            #Now you join the idsCurriculum parameters allowing only the ones that belong to all the lists (execute an AND with them)
            finalIdCurriculumList = []
            for idCurriculum in parameters['curr.idCurriculum'][0]:
                belongToAll = True
                for idsCurriculum in parameters['curr.idCurriculum'][1:]:
                    if not idCurriculum in idsCurriculum:
                        belongToAll = False
                        break
                if belongToAll:
                    finalIdCurriculumList.append(idCurriculum)
            parameters['curr.idCurriculum'] = finalIdCurriculumList
        else:
            del parameters['curr.idCurriculum']

        curriculaData = cursor.find('SELECT curr.idCurriculum, curr.name,  mc.name, curr.curriculumCode, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM curriculum curr JOIN minitableCurriculumType mc ON curr.idCurriculumType = mc.idCurriculumType',parameters)
        curricula = []
        for curriculumData in curriculaData:
            timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCurriculum = ' + str(curriculumData[0])  + ' GROUP BY rcc.idCurriculum')
            if len(timePeriodType) > 0:
                timePeriodType = timePeriodType[0][0]
            else:
                timePeriodType = None
            facultyData = cursor.execute('SELECT rcf.idFaculty FROM curriculum curr JOIN rel_courseCoordination_curriculum rcc ON curr.idCurriculum = rcc.idCurriculum JOIN rel_courseCoordination_faculty rcf ON rcc.idCourseCoordination = rcf.idCourseCoordination  WHERE curr.idCurriculum = '+ str(curriculumData[0]))
            if len(facultyData) > 0:
                faculty = Faculty.pickById(facultyData[0][0])
            else:
                faculty = None

            curriculum = Curriculum(curriculumData[1], curriculumData[2], curriculumData[3], timePeriodType, faculty, curriculumData[4], curriculumData[5])#name, curriculumType, curriculumCode, timePeriodType, faculty, startDate, termLength
            curriculum.setVacancyNumber(curriculumData[6])
            curriculum.setEndDate(curriculumData[7])
            curriculum.setAbbreviation(curriculumData[8])
            curriculum.idCurriculum = curriculumData[0]
            curricula.append(curriculum)
        return curricula
        
        
    def store(self):
        """
         Alters the curriculum's data in the data base.

        @return bool :
        @author
        """
        pass #I am not ready        
        if self.idCurriculum == None:
            curricula = Curriculum.find(idCurriculum = self.idCurriculum, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, curriculumType = self.curriculumType, curriculumCode = self.curriculumCode, timePeriodType_equal = self.timePeriodType, faculty = self.faculty, abbreviation_equal = self.abbreviation)
            if len(curricula) > 0:
                self.idCurriculum = curricula[0].idCurriculum #Any curriculum that fit those paramaters is the same as this curriculum, so no need to save
                return
            else:
                
                
#         > idCurriculum
#         > name_equal or name_like
#         > startDate_equal or startDate_like
#         > endDate_equal or endDate_like
#         > curriculumType
#         > curriculumCode
#         > timePeriodType_equal or timePeriodType_like
#         > faculty
#         > abbreviation_equal or abbreviation_like
         
         
                #Create this curriculum
                query = "INSERT INTO curriculum (name, curriculumType, curriculumCode" #FALTAM OS OBRIGATORIOS FACULTY E TIMEPERIODTYPE
                values = ") VALUES('" +self.name +"', '" +str(self.curriculumType) +"', '" +str(self.curriculumCode)
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
                self.idCurriculum = Curriculum.find(idCurriculum = self.idCurriculum, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, curriculumType = self.curriculumType, curriculumCode = self.curriculumCode, timePeriodType_equal = self.timePeriodType, faculty = self.faculty, abbreviation_equal = self.abbreviation)[0].idCurriculum 
        
        '''self.name
        self.curriculymType
        self.curriculumCode
        self.timePeriodType
        self.faculty
        self.idCurriculum
        self.startDate
        self.endDate
        self.mandatoryIdealTerms
        self.electiveIdealTerms
        self.abbreviation'''

    def delete(self):
        """
         Deletes the curriculum's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        
        if self.idCurriculum != None:
            cursor = MySQLConnection()
            if self == Curriculum.pickById(self.idCurriculum):
                cursor.execute('DELETE FROM curriculum WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.execute('DELETE FROM rel_course_curriculum WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.execute('DELETE FROM rel_courseCoordination_curriculum WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.execute('DELETE FROM rel_academicProgram_curriculum WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.execute('DELETE FROM rel_course_curriculum_course WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.execute('DELETE FROM rel_curriculum_opticalSheet WHERE idCurriculum = ' + str(self.idCurriculum))
                cursor.commit()
            else:
                raise CourseError("Can't delete non saved object.")
        else:
            raise CourseError('idCurriculum not defined.')




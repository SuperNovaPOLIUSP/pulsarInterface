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

     código da habilitação (vide jupiter)

    codHab  (public)

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

    def __init__(self, name, curriculumType, codHab, timePeriodType, faculty, startDate, termLength):
        """

        @param string name : Curriculum's name
        @param string curriculumType : It represents the type of curriculum, (e.g general area, basic cycle,... ).
        @param string codHab : codigo da habilitação (vide jupiter)
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
        if not isinstance(codHab, (int, long)):
            raise CurriculumError('Parameter codHab must be an int or a long.')
        if not isinstance(timePeriodType, (str, unicode)):
            raise CurriculumError('Parameter timePeriodType must be a string or unicode.')
        if not isinstance(faculty, Faculty) or not Faculty.pickById(faculty.idFaculty) == faculty:
            raise CurriculumError('Parameter faculty must be a Faculty object that exists in the database.')
        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or checkDateString(startDate) == None:
                raise CurriculumError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')
        if not isinstance(termLength, (str, unicode)):
            raise CurriculumError('Parameter termLength must be a string or unicode.')


        self.name = name
        self.curriculumType = curriculumType
        self.codHab = codHab
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
        print endDate
        if endDate != None:
            if not isinstance(endDate,datetime.date):
                if not isinstance(endDate,(str,unicode)) or checkDateString(endDate) == None:
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
        self.mandatoryIdealTerms = []
        cursor = MySQLConnection()
        query = "SELECT idCourse FROM rel_course_curriculum JOIN curriculum ON curriculum.idCurriculum = rel_course_curriculum.idCurriculum WHERE "
        query += "rel_course_curriculum.idCurriculum = " +str(self.idCurriculum)
        query += " AND rel_course_curriculum.requisitionType = 1 AND rel_course_curriculum.term = "
        term_searched_for = 0
        courses = ["nada"] #so it enters on the loop below
        for term_searched_for in range(13): #while len(courses) != 0:
            term_searched_for += 1
            courses = cursor.execute(query + str(term_searched_for))
            if len(courses) != 0:
                list_courses = []
                for course in courses:
                    list_courses.append(Course.pickById(course[0]))
                idealTerm = IdealTerm(self.idCurriculum, term_searched_for)
                idealTerm.addCourses(list_courses)
                self.mandatoryIdealTerms.append(idealTerm)
        

    def completeElectiveIdealTerms(self):
        """
         Completes the electiveIdealTerms list with the objects idealTerm related to the
         electives time period of this curriculum.

        @return bool :
        @author
        """
        self.electiveIdealTerms = []
        cursor = MySQLConnection()
        query = "SELECT rel_course_curriculum.idCourse FROM rel_course_curriculum JOIN curriculum ON curriculum.idCurriculum = rel_course_curriculum.idCurriculum WHERE "
        query += "rel_course_curriculum.idCurriculum = " +str(self.idCurriculum)
        query += " AND rel_course_curriculum.requisitionType = 2 AND rel_course_curriculum.term = "
        term_searched_for = 0
        courses = ["nada"] #so it enters on the loop below
        for term_searched_for in range(13): #while len(courses) != 0:
            term_searched_for += 1
            courses = cursor.execute(query + str(term_searched_for))
            if len(courses) != 0:
                list_courses = []
                for course in courses:
                    list_courses.append(Course.pickById(course[0]))
                idealTerm = IdealTerm(self.idCurriculum, term_searched_for)
                idealTerm.addCourses(list_courses)
                self.mandatoryIdealTerms.append(idealTerm)

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
            #All curricula must have a rel_curriculum_faculty relation and at least one offer
            #Here get most of the curricula data
            curriculumData = cursor.execute('SELECT curr.name,  mc.name, curr.curriculumCode, rcf.idFaculty, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM curriculum curr JOIN rel_courseCoordination_curriculum rcc ON curr.idCurriculum = rcc.idCurriculum JOIN rel_courseCoordination_faculty rcf ON rcc.idCourseCoordination = rcf.idCourseCoordination  JOIN minitableCurriculumType mc ON curr.idCurriculumType = mc.idCurriculumType WHERE curr.idCurriculum = '+ str(idCurriculum))[0]
            #Now get the timePeriodType
            timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCurriculum = ' + str(idCurriculum)  + ' GROUP BY idCurriculum')[0][0]
        except:
            return None
        curriculum = Curriculum(curriculumData[0], curriculumData[1], curriculumData[2], timePeriodType, Faculty.pickById(curriculumData[3]), curriculumData[4], curriculumData[5])#name, curriculumType, codHab, timePeriodType, faculty, startDate, termLength
        curriculum.setVacancyNumber(curriculumData[6])
        curriculum.setEndDate(curriculumData[7])
        curriculum.setAbbreviation(curriculumData[8])
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
         > codHab
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
            if key == 'curriculumType':
                parameters['mc.name'] = kwargs['curriculumType']

            elif key == 'faculty':
                parameters['rcf.idFaculty'] = kwargs['faculty'].idFaculty

            elif key.find('timePeriod') != -1:
                query = 'SELECT rcc.idCurriculum  FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length'
                if key.find('like') != -1:
                    query = query + 'WHERE ml.length like ' + kwargs[key]  + ' GROUP BY idCurriculum'
                else:
                    query = query + 'WHERE ml.length = ' + kwargs[key]  + ' GROUP BY rcc.idCurriculum'
                curriculaData = cursor.execute(query)
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

        curriculaData = cursor.find('SELECT curr.idCurriculum, curr.name,  mc.name, curr.curriculumCode, rcf.idFaculty, curr.startDate, curr.termLength, curr.vacancyNumber, curr.endDate, curr.abbreviation  FROM curriculum curr JOIN rel_courseCoordination_curriculum rcc ON curr.idCurriculum = rcc.idCurriculum JOIN rel_courseCoordination_faculty rcf ON rcc.idCourseCoordination = rcf.idCourseCoordination  JOIN minitableCurriculumType mc ON curr.idCurriculumType = mc.idCurriculumType',parameters)
        curricula = []
        for curriculumData in curriculaData:
            timePeriodType = cursor.execute('SELECT ml.length FROM aggr_offer aggr JOIN timePeriod tp ON tp.idTimePeriod = aggr.idTimePeriod JOIN rel_course_curriculum rcc ON rcc.idCourse = aggr.idCourse JOIN minitableLength ml ON ml.idLength = tp.length WHERE rcc.idCurriculum = ' + str(curriculumData[0])  + ' GROUP BY rcc.idCurriculum')[0][0]
            curriculum = Curriculum(curriculumData[1], curriculumData[2], curriculumData[3], timePeriodType, Faculty.pickById(curriculumData[4]), curriculumData[5], curriculumData[6])#name, curriculumType, codHab, timePeriodType, faculty, startDate, termLength
            curriculum.setVacancyNumber(curriculumData[7])
            curriculum.setEndDate(curriculumData[8])
            curriculum.setAbbreviation(curriculumData[9])
            curriculum.idCurriculum = curriculumData[0]
            curricula.append(curriculum)
        return curricula
        
        
    def store(self):
        """
         Alters the curriculum's data in the data base.

        @return bool :
        @author
        """
        
        if self.idCurriculum == None:
            curricula = Curriculum.find(idCurriculum = self.idCurriculum, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, curriculumType = self.curriculumType, codHab = self.codHab, timePeriodType_equal = self.timePeriodType, faculty = self.faculty, abbreviation_equal = self.abbreviation)
            if len(curricula) > 0:
                self.idCurriculum = curricula[0].idCurriculum #Any curriculum that fit those paramaters is the same as this curriculum, so no need to save
                return
                
#         > idCurriculum
#         > name_equal or name_like
#         > startDate_equal or startDate_like
#         > endDate_equal or endDate_like
#         > curriculumType
#         > codHab
#         > timePeriodType_equal or timePeriodType_like
#         > faculty
#         > abbreviation_equal or abbreviation_like
         
        else: 
                #Create this curriculum
                query = "INSERT INTO curriculum (name, curriculumType, curriculumCode" #FALTAM OS OBRIGATORIOS FACULTY E TIMEPERIODTYPE
                values = ") VALUES('" +self.name +"', '" +str(self.curriculumType) +"', '" +str(self.codHab)
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
                self.idCurriculum = Curriculum.find(idCurriculum = self.idCurriculum, name_equal = self.name, startDate_equal = self.startDate, endDate_equal = self.endDate, curriculumType = self.curriculumType, codHab = self.codHab, timePeriodType_equal = self.timePeriodType, faculty = self.faculty, abbreviation_equal = self.abbreviation)[0].idCurriculum 
        
        '''self.name
        self.curriculymType
        self.codHab
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




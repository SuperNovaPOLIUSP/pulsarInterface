from Course import *
from IdealTerm import *
from AcademicProgram import *
from Faculty import *
from Dictionary import *
from tools.timeCheck import *

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
     It's value is null if the curriculum is not over. Over is defined as the last
     time this curriculum was given in this University.

    endDate  (public)

     It represents the type of curriculum, (e.g general area, basic cycle ...).

    curriculumType  (public)

     código da habilitação (vide júpiter)

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

    abbreviation  (private)

    """

    def __init__(self, name, curriculumType, codHab, timePeriodType, faculty):
        """
         

        @param string name : Curriculum's name
        @param string curriculumType : It represents the type of curriculum, (e.g general area, basic cycle,... ).
        @param string codHab : codigo da habilitação (vide jupiter)
        @param string timePeriodType : String representing the period division ("quarter" or "semester").
        @param Faculty faculty : The curriculum's faculty. 
        @return  :
        @author
        """
        self.name = name
        self.curriculymType = curriculymType
        self.codHab = codHab
        self.timePeriodType = timePeriodType
        self.faculty = faculty
        self.idCurriculum = None
        self.startDate = None
        self.endDate = None
        self.mandatoryIdealTerms = None
        self.electiveIdealTerms = None
        self.abbreviation = None
        
    def __eq__(self, other):
        if not isinstance(other, Curriculum):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setStartDate(self, startDate):
        """
         

        @param string startDate : Date of the start of this curriculum, in the form year-month-day “xxxx-xx-xx”.Start is defined as the first time this curriculum was given in this University.
        @return  :
        @author
        """
        if checkDateString(startDate) is not None
            self.startDate = startDate
            return True
        return False

    def setEndDate(self, endDate):
        """
         

        @param string endDate : Date of the end of this curriculum, in the form year-month-day “xxxx-xx-xx”. It's value is null if the curriculum is not over. Over is defined as the last time this curriculum was given in this University.
        @return  :
        @author
        """
        if checkDateString(endDate) is not None
            self.endDate = endDate
            return True
        return False

    def completeMandatoryIdealTerms(self):
        """
         Completes the mandatoryIdealTerms list with the objects idealTerm related to the
         mandatories time period of this curriculum.

        @return bool :
        @author
        """
        pass

    def completeElectiveIdealTerms(self):
        """
         Completes the electiveIdealTerms list with the objects idealTerm related to the
         electives time period of this curriculum.

        @return bool :
        @author
        """
        pass

    @staticmethod
    def pickById(idCurriculum):
        """
         Returns a single curriculum with the chosen ID.

        @param int idCurriculum : Associated data base key.
        @return Curriculum :
        @author
        """
        cursor = MySQLConnection()
        query = 'SELECT name, curriculumType, codHab, timePeriodType, faculty, idCurriculum, startDate, endDate, mandatoryIdealTerms, electiveIdealTerms, abbreviation FROM curriculum WHERE idCurriculum = ' + str(idCurriculum)
        try:
            curriculum_sql = cursor.execute(query)[0]
        except:
            return None
        curriculum = Curriculum(curriculum_sql[0], curriculum_sql[1], curriculum_sql[2], curriculum_sql[3], curriculum_sql[4])
        curriculum.idCurriculum = idCurriculum
        curriculum.startDate = curriculum_sql[6]
        curriculum.endDate = curriculum_sql[7]
        curriculum.mandatoryIdealTerms = curriculum_sql[8]
        curriculum.electiveIdealTerms = curriculum_sql[9]
        curriculum.abbreviation = curriculum_sql[10]
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
         > campus_equal or campus_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Curriculum.find(timePeriodTime_equal = "night", name_like = "Computer")

        @param dictionary _kwargs : 
        @return Curriculo[] :
        @author
        """
        cursor = MySQLConnection()
        curriculaData = cursor.find('SELECT name, curriculumType, codHab, timePeriodType, faculty, idCurriculum, startDate, endDate, mandatoryIdealTerms, electiveIdealTerms, abbreviation FROM curriculum',kwargs)
        curricula = []
        for curriculumData in curriculaData:
            curriculum = Curriculum(curriculaData[0], curriculaData[1], curriculaData[2], curriculaData[3], curriculaData[4])
            curriculum.idCurriculum = curriculaData[5]
            curriculum.startDate = curriculaData[6]
            curriculum.endDate = curriculaData[7]
            curriculum.mandatoryIdealTerms = curriculaData[8]
            curriculum.electiveIdealTerms = curriculaData[9]
            curriculum.abbreviation = curriculaData[10]
            curricula.append(curriculum)
        return curricula
        
        
    def store(self):
        """
         Alters the curriculum's data in the data base.

        @return bool :
        @author
        """
        pass

    def delete(self):
        """
         Deletes the curriculum's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        pass




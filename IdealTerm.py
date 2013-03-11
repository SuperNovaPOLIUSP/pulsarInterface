from Course import Course
from tools.MySQLConnection import *


class IdealTerm(object):

    """
     It is the group of disciplines that belongs to a curriculum's term.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCurriculum  (private)

     The term (number of the curriculum's semester or  quadmester) of the relation.

    term  (private)

     List of courses that belong to this relation.

    courses  (private)

     It says if the course is mandatory, elective or free elective.

    requisitionType  (private)


    startDate  (private)


    endDate  (private)

    """

    def __init__(self, idCurriculum, term):
        """
         Constructor method.

        @param int idCurriculum : Associated data base key.
        @param int term : Term of the ideal term.
        @return  :
        @author
        """
        cursor = MySQLConnection()              
        
        if not cursor.execute('SELECT idCurriculum FROM curriculum  WHERE idCurriculum = ' + str(idCurriculum)):   
            raise IdealTermError('idCurriculum must be in the database')
        self.idCurriculum = idCurriculum
        self.term = term
        self.courses = None
        self.requisitionType = None
        self.startDate = None
        self.endDate = None
	
    def addCourse(self, course):
        """
             Adds courses to a relation.
             Return: True if successful or False, otherwise
    
             @param Course[] course : Disciplines's list to be added to the relation.
             @return bool :
             @author
        """
        
        cursor = MySQLConnection()
        
        try:
            for course_data in course:
                if not isinstance(course_data, Course) or not Course.pickById(course.idCourse) == course:
                    raise IdealTermError('The parameter course must be a list of course objects present in the database')
        except:
            raise IdealTermError('The parameter course must be a list.')

        if not self.courses:
            self.courses = course
            return False

        for course_data in course:
            if not course_data in self.courses:
                self.courses.append(course_data)
        
        return True

    def removeCourse(self, course):
        """
         Removes a course from its list.
         Return: True if successful or False, otherwise

        @param Course course : Course to be removed.

        @return bool :
        @author
        """

        try:
            self.courses.remove(course)
        except:
            return False

        return True

    def fillCourses(self):
        """
         Fill the list of courses from the ideal term.

        @return bool :
        @author
        """
        courses = []
        cursor = MySQLConnection()

        query = 'SELECT idCourse from rel_course_curriculum WHERE idCurriculum = ' + str(self.idCurriculum)
        courses_data = cursor.execute(query)

        for course_data in courses_data:
            courses.append(Course.pickById(course_data)[0])

        self.addCourse(courses)
        return True
        
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
         > term
         > course
         > requisitionType
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E.g. IdealTerm.find(course = courseObject, term = 3, startDate_equal =
         "2008-10-20", endDate_like = "2010")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return idealTerm[] :
        @author
        """
        cursor = MySQLConnection()
        ideal_terms_data = cursor.find('SELECT idCurriculum, term, idCourse, requisitionType, startDate, endDate FROM rel_course_curriculum',kwargs)
        ideal_terms = []
        for ideal_term_data in ideal_terms_data:
            ideal_term = IdealTerm(ideal_term_data[0], ideal_term_data[1])
            ideal_term.fillCourses()
            ideal_terms.append(ideal_term)

        return ideal_terms

    def store(self):
        """
         Creates or alters rel_course_curriculum in the database and returns True if it
         works, and False if it does not work.

        @return bool :
        @author
        """
        if self.startDate == None:
            startDate = 'CURRENT_DATE'
        else:
            startDate = str(self.startDate)
    
        if self.endDate == None:
            endDate = '0000-00-00'
        else:
            endDate = str(self.endDate)

        if self.requisitionType == None:
            requisitionType = 1
        else:
            requisitionType = self.requisitionType



        cursor = MySQLConnection()
        try:
            for course in self.courses:
                #Search for idIdealTerm
                possibleIdealTerms = self.find(idCurriculum = self.idCurriculum, course = course, term = self.term)
                if len(possibleIdealTerms) > 0:
                    if not self.startDate == possibleIdealTerms[0].startDate or not self.endDate == possibleIdealTerms[0].endDate:
                        query = 'UPDATE rel_course_curriculum SET startDate = ' + startDate + ', endDate = ' + endDate + ' WHERE idCourse = ' + str(course.idCourse) + ' AND idCurriculum = ' + str(self.idCurriculum)
                        cursor.execute(query)
                        cursor.commit()

                else:
                    #If there is no idIdealTerm create row
                    query = 'INSERT INTO rel_course_curriculum (idCourse, idCurriculum, startDate, endDate, term, requisitionType) VALUES(' + str(course.idCourse) + ', ' + str(self.idCurriculum) + ', ' + startDate + ', ' + endDate + ', ' + str(self.term)+ ', ' + str(requisitionType) + ')'
                    cursor.execute(query)
                    cursor.commit()
                    return True
        except:
            raise IdealTermError('')

    def delete(self):
        """
         Deletes the ideal term's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        pass




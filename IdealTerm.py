from Course import Course
from tools.MySQLConnection import *
import sys
import time
from datetime import *

class IdealTermError(Exception):
    """
     Exception reporting an error in the execution of a Faculty method.

    :version:
    :author:
    """
    pass

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

    def __init__(self, idCurriculum, term, startDate):
        """
         Constructor method.

        @param int idCurriculum : Associated data base key.
        @param int term : Term of the ideal term.
        @param string startDate : Starting date of this ideal term.
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
        self.startDate = startDate
        self.endDate = '0000-00-00'

    def setEndDate(self, endDate):
        """
         Set the endDate of this IdealTerm.

        @param string endDate : String representing this IdealTerm's end date .
        @author
        """
        self.endDate = endDate
	
    def addCourses(self, courses):
        """
             Adds courses to a relation.
             Return:
    
             @param Course[] courses : Disciplines's list to be added to the relation.
             @return bool :
             @author
        """
        
        cursor = MySQLConnection()
        
        try:
            for course_data in courses:
                # if the object in the list 'courses' is not an object neither is in the database, the parameter 'courses' must not be added to the idealTerm object
                if not isinstance(course_data, Course):
                        if not Course.pickById(course.idCourse) == course:
                                raise CourseError('Course not in the database')
        except:
            raise IdealTermError("The parameter 'courses' must be a list of 'Course' objects.")

        if not self.courses:
            self.courses = []
            for course in courses:
                self.courses.append(course)
        else:
            for course_data in courses:
                if not course_data in self.courses:
                    self.courses.append(course_data)

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

        query = 'SELECT idCourse from rel_course_curriculum WHERE idCurriculum = ' + str(self.idCurriculum) + ' AND term = ' + str(self.term)
        courses_data = cursor.execute(query)

        for course_data in courses_data:
            courses.append(Course.pickById(course_data[0]))

        self.addCourses(courses)
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
         > courses
         > requisitionType
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E.g. IdealTerm.find(course = courseObject, term = 3, startDate_equal =
         "2008-10-20", endDate_like = "2010")

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return idealTerm[] :
        @author
        """
        cursor = MySQLConnection()
        new_kwargs = {}
        for key in kwargs:
           if not key == "courses":
               new_kwargs[key] = kwargs[key]
        query = 'SELECT DISTINCT idCurriculum, term, startDate, endDate, requisitionType'
        if kwargs.has_key('requisitionType'): 
            query += ', requisitionType'
        if kwargs.has_key('startDate'): 
            query += ', startDate'
        if kwargs.has_key('endDate'):
            query += ', endDate'
        if kwargs.has_key('courses'): 
            new_courses = []
            for course in kwargs['courses']:
                new_courses.append(course.idCourse)
            new_kwargs["idCourse"] = new_courses
            query += ', idCourse'
        query += ' FROM rel_course_curriculum'
        objects_to_create = []
        complements = []
        number_objects = 0
        idealTerms = []
        query_result = cursor.find(query, new_kwargs)
        if len(query_result) > 0:
            for idealTerms_data in query_result:
                #if it's the first time that query_result is being read; or 
                #if the idCurriculum of the current object is different from the current line in the query_result; or
                #if the term of the current object is different from the current line in the query_result; then
                #another object must be created        
                if number_objects == 0 or objects_to_create[number_objects-1][0] != idealTerms_data[0] or objects_to_create[number_objects-1][1] != idealTerms_data[1]:
                    objects_to_create.append(list(idealTerms_data))
                    number_objects += 1
            for idealTerm_data in objects_to_create:
                idealTerm = IdealTerm(idealTerm_data[0], idealTerm_data[1], idealTerm_data[2].isoformat())
                idealTerm.fillCourses()
                if idealTerm_data[3] != None:
                    endDate = idealTerm_data[3].isoformat()
                    idealTerm.setEndDate(endDate)
                idealTerm.requisitionType = idealTerm_data[4]
                idealTerms.append(idealTerm)
        return idealTerms

    def store(self):
        """
         Creates or alters rel_course_curriculum in the database and returns True if it
         works, and False if it does not work.

        @return bool :
        @author
        """

        if self.requisitionType == None:
            requisitionType = 1
            self.requisitionType = requisitionType
        else:
            requisitionType = self.requisitionType

        cursor = MySQLConnection()

        try:
            for course in self.courses:
                #Search for idIdealTerm
                possibleIdealTerms = self.find(idCurriculum = self.idCurriculum, courses = [course], term = self.term, startDate_equal = self.startDate)
                if len(possibleIdealTerms) > 0:
                    if not self.startDate == possibleIdealTerms[0].startDate or not self.endDate == possibleIdealTerms[0].endDate:
                        query = "UPDATE rel_course_curriculum SET startDate = '" + self.startDate + "', endDate = '" + self.endDate + "' WHERE idCourse = " + str(course.idCourse) + ' AND idCurriculum = ' + str(self.idCurriculum)
                        cursor.execute(query)
                        cursor.commit()

                else:
                    #If there is no idIdealTerm create row
                    query = 'INSERT INTO rel_course_curriculum (idCourse, idCurriculum, startDate, endDate, term, requisitionType) VALUES(' + str(course.idCourse) + ', ' + str(self.idCurriculum) + ", '" + self.startDate + "', '" + self.endDate + "', " + str(self.term)+ ', ' + str(requisitionType) + ')'
                    cursor.execute(query)
                    cursor.commit()
        except:
            raise IdealTermError('Error adding or updating IdealTerm')

    def __eq__(self, other):
        if not isinstance(other, IdealTerm):
            return False
        return self.__dict__ == other.__dict__

    def delete(self):
        """
         Deletes the ideal term's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if not self.courses:
            raise IdealTermError('No courses in this IdealTerm')
        for course in self.courses:
            query = 'delete from rel_course_curriculum where idCurriculum = ' + str(self.idCurriculum) + ' and term = ' + str(self.term) + " and startDate = '" + self.startDate + "' and endDate = '" + self.endDate + "' and idCourse = " + str(course.idCourse)
            if self.requisitionType:
                query += ' and requisitionType = ' + str(self.requisitionType)
            try:
                cursor.execute(query)
                cursor.commit()
            except:
                raise IdealTermError('Error on deleting IdealTerm')

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
     It is the group of disciplines that belongs to a cycle's term.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCycle  (private)

     The term (number of the cycle's semester or  quadmester) of the relation.

    term  (private)

     List of courses that belong to this relation.

    courses  (private)

     It says if the course is mandatory, elective or free elective.

    requisitionType  (private)

    startDate  (private)

    endDate  (private)

    """

    def __init__(self, idCycle, term, startDate, requisitionType, course):
        """
         Constructor method.

        @param int idCycle : Associated data base key.
        @param int term : Term of the ideal term.
        @param string startDate : Starting date of this ideal term.
        @return  :
        @author
        """
        cursor = MySQLConnection()              
        
        if not cursor.execute('SELECT idCycle FROM cycle WHERE idCycle = ' + str(idCycle)):   
            raise IdealTermError('idCycle must be in the database')
        if not startDate or not isinstance(startDate, (str,unicode)) or not checkDateString(startDate):
            raise IdealTermError('Must provide a valid start date string in unicode')
        if not requisitionType or not isinstance(requisitionType, (int, long)):
            raise IdealTermError('Must provide a valid requisition type integer')
        if not isinstance(course, Course) or Course.pickById(course.idCourse) != course:
            raise IdealTermError('Must provide a valid course from the database')
        self.idCycle = idCycle
        self.term = term
        self.course = course
        self.requisitionType = requisitionType
        self.startDate = startDate
        self.setEndDate('0000-00-00')

    def setEndDate(self, endDate):
        """
         Set the endDate of this IdealTerm.

        @param string endDate : String representing this IdealTerm's end date .
        @author
        """
        if not isinstance(endDate, (str,unicode)) or not checkDateString(endDate):
            raise IdealTermError('endDate parameter must be a valid string representing a date')
        self.endDate = endDate
	
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
        searchData = cursor.find('SELECT idCourse, idCycle, startDate, endDate, term, requisitionType FROM rel_course_cycle ', kwargs)
        idealTerms = []
        for idealTermData in searchData:
            newIdealTerm = IdealTerm(idealTermData[1], idealTermData[4], idealTermData[2].isoformat(), idealTermData[5], Course.pickById(idealTermData[0]))
            newIdealTerm.setEndDate(idealTermData[3].isoformat())
            idealTerms.append(newIdealTerm)
        return idealTerms

    def store(self):
        """
         Creates or alters rel_course_cycle in the database and returns True if it
         works, and False if it does not work.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if not self.idCycle or not self.idCourse or not self.endDate or not self.startDate or not self.term:
            return False
        idCycle = str(self.idCycle)
        idCourse = str(self.idCourse)
        term = str(self.term)
        if self.requisitionType:
            requisitionType = str(self.requisitionType)
        else:
            requisitionType = 'NULL'
        querySelect = 'SELECT idCourse, idCycle, endDate FROM rel_course_cycle WHERE idCourse = ' + idCourse + ' and idCycle = ' + idCycle + ' and endDate = ' + self.endDate
        queryInsert = 'INSERT INTO rel_course_cycle (idCourse, idCycle, startDate, endDate, term, requisitionType) values (' + idCourse + ', ' + idCycle + ', ' + self.startDate + ', ' + self.endDate + ', ' + term + ', ' + requisitionType + ')'
        queryUpdate = 'UPDATE rel_course_cycle SET startDate = ' + self.startDate + ', term = ' + term + ', requisitionType = ' + requisitionType + ' WHERE idCourse = ' + idCourse + ' and idCycle = ' + idCycle + ' and endDate = ' + self.endDate
        try:
            searchData = cursor.execute(querySelect)
            if not searchData:
                cursor.execute(queryInsert)
                cursor.commit()
            else:
                cursor.execute(queryUpdate)
                cursor.commit()
        except:
            return False
        return True
    

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
        if not self.idCourse or not self.idCycle or not self.endDate:
            raise IdealTermError("Can't uniquely identify object, can't delete database tuple")
            return False
        query = 'DELETE FROM rel_course_cycle WHERE idCourse = ' + str(self.idCourse) + ' and idCycle = ' + str(self.idCycle) + ' and endDate = ' + self.endDate
        try:
            cursor.execute(query)
            cursor.commit()
        except:
            raise IdealTermError("Couldn't delete object")
            return False
        return True


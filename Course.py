from tools.MySQLConnection import *
from tools.timeCheck import *
import datetime

class CourseError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass

class Course(object):

    """
     Representation of a course in the database.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idCourse  (public)

     7 character code that represents the course.

    courseCode  (public)

     Abbreviation of the course's name.

    abbreviation  (public)

     Complete name of a course

    name  (public)

     List of offers associated with this course.

    offers  (public)

     Date of start of this course, in the form year-month-day "xxxx-xx-xx". Start is
     defined as the start of the course in general, not only in this year, but the
     first time it was in this University.

    startDate  (public)

     Date of the end of this course, in the form year-month-day "xxxx-xx-xx". It's
     value is null if the course is not over. Over is defined as the last time this
     discipline is given was this University

    endDate  (public)

    """

    def __init__(self, courseCode, name, startDate):
        """
         A course is defined by a name and a 7 character code.

        @param string courseCode : A 7 character code that represents the course.
        @param string name : Complete name of a discipline.
        @return  :
        @author
        """
        if not isinstance(courseCode,(str,unicode)):
            raise CourseError('Parameter courseCode must be a string or an unicode')
        if not isinstance(name,(str,unicode)):
            raise CourseError('Parameter name must be a string or an unicode')

        if not isinstance(startDate,datetime.date):
            if not isinstance(startDate,(str,unicode)) or checkDateString(startDate) == None:
                raise CourseError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')

        self.startDate = startDate
        self.courseCode = courseCode
        self.name = name
        self.idCourse = None
        self.abbreviation = None
        self.offers = []
        self.startDate = None
        self.endDate = None

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other) 

    def setAbbreviation(self, abbreviation):
        """
         Set the abbreviation of this course.

        @param string abbreviation : Abbreviation of the course's name.
        @return string :
        @author
        """
        if not isinstance(abbreviation,(str,unicode)):
            raise CourseError("Parameter abbreviation must be str or unicode")
        self.abbreviation = abbreviation

    def setEndDate(self, endDate):
        """
         Set the endDate of this course .

        @param string endDate : String difining the end  date of this course, in the form year-month-day "xxxx-xx-xx".
        @return string :
        @author
        """
        if endDate != None:
            if not isinstance(startDate,datetime.date):
                if not isinstance(startDate,(str,unicode)) or checkDateString(startDate) == None:
                    raise CourseError('Parameter startDate must be a datetime.date format or a string in the format year-month-day')
        self.endDate = endDate

    @staticmethod
    def pickById(idCourse):
        """
         Returns a single course with the chosen ID.

        @param int idCourse : Associated data base key.
        @return int :
        @author
        """
        cursor = MySQLConnection()
        try:
            courseData = cursor.execute('SELECT idCourse, courseCode, abbreviation, name, startDate, endDate FROM course WHERE idCourse = ' + str(idCourse))[0]
        except:
            return None

        course = Course(courseData[1],courseData[3],courseData[4])
        course.idCourse = courseData[0]
        course.setAbbreviation(courseData[2])
        course.setEndDate(courseData[5]) 
        return course        

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
         > idCourse
         > courseCode_equal or courseCode_like
         > abbreviation_equal or abbreviation_like
         > name_equal or name_like
         > startDate_equal or startDate_like
         > endDate_equal or endDate_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Course.find(name_like = "Computer", courseCode_equal = "MAC2166")

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return course[] : 
        @author
        """
        cursor = MySQLConnection()
        coursesData = cursor.find('SELECT idCourse, courseCode, abbreviation, name, startDate, endDate FROM course',kwargs)
        courses = []
        for courseData in coursesData:
            course = Course(courseData[1],courseData[3],courseData[4])
            course.idCourse = courseData[0]
            course.setAbbreviation(courseData[2])
            course.setEndDate(courseData[5]) 
            courses.append(course)
        return courses

    def store(self):
        """
         Creates or alters a course in the database, returns True if it is successful. If
         the offers list is not empty, alters it in the database.

        @return bool :
        @author
        """
        pass

    def delete(self):
        """
         Deletes the course's data in the database.
         
         Return: True if succesful or False otherwise

        @return bool :
        @author
        """
        pass




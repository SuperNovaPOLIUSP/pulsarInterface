#import header
from Offer import Offer
from tools.MySQLConnection import *

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

    def __init__(self, courseCode, name):
        """
         A course is defined by a name and a 7 character code.

        @param string courseCode : A 7 character code that represents the course.
        @param string name : Complete name of a discipline.
        @return  :
        @author
        """
        self.courseCode = courseCode
        self.name = name
        self.idCourse = None
        self.abbreviation = None
        self.offers = []
        self.startDate = None
        self.endDate = None

    def setAbbreviation(self, abbreviation):
        """
         Set the abbreviation of this course.

        @param string abbreviation : Abbreviation of the course's name.
        @return string :
        @author
        """
        self.abbreviation = abbreviation

    def setStartDate(self, startDate):
        """
         Set the startDate of this course .

        @param string startDate : String defining the criation date of this course, in the form year-month-day "xxxx-xx-xx".
        @return  :
        @author
        """
        self.startDate = startDate

    def setEndDate(self, endDate):
        """
         Set the endDate of this course .

        @param string endDate : String difining the end  date of this course, in the form year-month-day "xxxx-xx-xx".
        @return string :
        @author
        """
        self.endDate = endDate

    def addOffers(self, offers):
        """
         Adds a set of offers to this course.

        @param Offer[] offers : List of offers to be associated to this course.
        @return bool :
        @author
        """
        for offer in offers:
            self.offers.append(offer)

    def removeOfferById(self, idOffer):
        """
         Removes an offer with the chosen ID from the list offers.

        @param int idOffer : The id of the offer chosen to be removed from this course.
        @return  :
        @author
        """
        self.offers = [offer for offer in self.offers if offer.idOffer != idOffer ]    

    @staticmethod
    def specifyCourse(offers):
        """
         Receives a list of offers and returns the name associated with this set.
         E.g. Physics (P)[professor's name].

        @param Offer[] offers : List of offers
        @return string :
        @author
        """
        #Check if the course, the professor and the practical is the same.
        idCourse = offers[0].idCourse
        idTimePeriod = offers[0].timePeriod.idTimePeriod
        idProfessor = offers[0].professor.idProfessor
        practical = offers[0].practical
        for offer in offers[1:]:
            if offer.timePeriod.idTimePeriod != idTimePeriod:
                return None #if the timePeriod is diferent there is no name for this set of offers.
            if offer.idCourse != idCourse:
                return None #if the course is diferent there is no name for this set of offers.
            if idProfessor != offer.professor.idProfessor:
                idProfessor = None
            if practical != offer.practical:
                practical = None
        courseName = offers[0].getCourse().name
        #Now checks if there are other offers in this course that have diferent professors and practical from this set
        otherOffers = Offer.find(idCourse = idCourse, timePeriod = offers[0].timePeriod)
        otherProfessor = False
        otherPractical = False
        for otherOffer in otherOffers:
            if idProfessor != None:
                if otherOffer.professor.idProfessor != idProfessor:
                    otherProfessor = True                    
            if practical != None:
                if otherOffer.practical != practical:
                    otherPractical = True
        #Now creats the name
        if otherProfessor:
            courseName = courseName + '[' + offers[0].professor.name + ']'
        if otherPractical:
            if practical == 1:
                courseName = courseName + '(P)'
            else:
                courseName = courseName + '(T)'
        return courseName

    def possibleNames(self):
        """
         Returns a list of dicts in the form {name:specifyCourse(offers),offers:Offer[]},
         where the offers is a subset of this courses offers, and the name is the name of
         this subset. The list must contain all possible names for that course.
    
        @return [] :
        @author
        """
        pass


    def fillOffers(self, **kwargs):
        """
         Fills the object's list of offers, the parameters passed to kwargs may be:
         >practical
         >professor
         >timePeriod
         >classNumber

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        if self.idCourse != None:
            kwargs['idCourse'] = self.idCourse
            self.offers = Offer.find(**kwargs)
        

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
            courseData = cursor.execute('SELECT courseCode, name FROM course WHERE idCourse = ' + str(idCourse))[0]
        except:
            return None
        course = Course(courseData[0],courseData[1])
        course.idCourse = idCourse
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
            course = Course(courseData[1],courseData[3])
            course.setAbbreviation(courseData[2])
            course.setStartDate(courseData[4])
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




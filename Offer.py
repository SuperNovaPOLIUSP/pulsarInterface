from TimePeriod import TimePeriod
from Professor import Professor
from Course import Course
from Schedule import Schedule
from toolsDev.tools.MySQLConnection import MySQLConnection 

class OfferError(Exception):
    """
     Exception reporting an error in the execution of a Offer method.

    :version:
    :author:
    """
    pass

class Offer(object):

    """
     COMPLETAR!!!!!!!!!!!!!!!

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key of this offer.

    idOffer  (private)

     The database ID of the course related to this offer.

    idCourse  (private)

     The professor responsible for this offer.

    professor  (private)

     The time period related to this offer.

    timePeriod  (private)

     The college class's number of this offer.

    classNumber  (private)

     It is True if this offer is a practical class, and False if it is a theoretical
     class.

    practical  (private)

     The number of max students allowed in this offer.

    numberOfRegistrationis  (private)

     List of schedules when the lectures related to this offer are held.

    schedules  (private)

    """

    def __init__(self, timePeriod, course, classNumber, practical, professor):
        """
         Creates an Offer object if all the parameters needed are specified, except by
         the numberOfRegistration, which is not necessarily needed.

        @param TimePeriod timePeriod : The offer's time period.
        @param int idCourse : The offer's course associated database key.
        @param int classNumber : The college class's number of the offer.
        @param bool pratica : It's true if the offer is a practical class, and false if it is a theoretical class.
        @param Professor professor : The professor responsible for this offer.
        @param int numberOfRegistrations : The maximum number of students allowed in this offer.
        @return  :
        @author
        """
        #Parameters verification.
        if not isinstance(timePeriod, TimePeriod) or not TimePeriod.pickById(timePeriod.idTimePeriod) == timePeriod:
            raise OfferError('Parameter timePerid must be a TimePeriod object that exists in the database.')
        if not isinstance(course, Course) or not Course.pickById(course.idCourse) == course:
            raise OfferError('Parameter course must be a Course object.')            
        if not isinstance(classNumber, (int, long)):
            raise OfferError('Parameter classNumber must be an int or a long.')
        if not isinstance(practical, int):
            raise OfferError('Parameter practical must be a bool.')

        #Setting parameters that have set function
        self.setProfessor(professor)
        #Setting other parameters
        self.timePeriod = timePeriod
        self.course = course
        self.classNumber = classNumber
        self.practical = practical
        #Setting None parameters
        self.numberOfRegistrations = None
        self.schedules = []
        self.idOffer = None

    def __eq__(self, other):
        if not isinstance(other, Offer):
            return False
        return self.__dict__ == other.__dict__

    def setProfessor(self, professor):
        """
         Associate a new professor with the offer.

        @param Professor professor : The new professorresponsable for this offer
        @return  :
        @author
        """
        if not isinstance(professor, Professor) or not Professor.pickById(professor.idProfessor) == professor:
            raise OfferError('Parameter professor must be a Professor object that exists in the database.')
        self.professor = professor

    def setNumberOfRegistrations(self, numberOfRegistrations):
        """
         Associate a numberOfRegistrations with the offer.

        @param int numberOfRegistrations : The number of registrations of this offer
        @return  :
        @author
        """
        if not isinstance(numberOfRegistrations, (int, long, type(None))) :
            raise OfferError('Parameter numberOfRegistrations must be an int or a long or None')

        self.numberOfRegistrations = numberOfRegistrations

    def setSchedules(self, schedules):
        """
         Associate a schedule list with the offer.

        @param Schedule schedules : The list of Schedule objects of this offer
        @return  :
        @author
        """
        for schedule in schedules:
            if not isinstance(schedule, Schedule):
                raise OfferError('Parameter schedules must be a list of Schedule objects')
        self.schedules = schedules

    def fillSchedules(self):
        """
         Finds the schedules associated to this offer through a query in the database.

        @param  :
        @return  :
        @author
        """
        if self.idOffer != None:
            cursor = MySQLConnection()
            schedulesData = cursor.execute('SELECT idSchedule FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
            self.schedules = [Schedule.pickById(scheduleData[0]) for scheduleData in schedulesData]
        else:
            raise OfferError('idOffer is not defined')

    @staticmethod
    def offersName(offers):
        """
         Receives a list of offers and returns the name associated with this set.
         E.g. Physics (P)[professor's name].

        @param Offer[] offers : List of offers
        @return string :
        @author
        """
        #Check if offers is a list of offer
        for offer in offers:
            if not isinstance(offer, Offer):
                print "offers must be a list of Offer objects"
                return None
        #Check if the course, the professor and the practical is the same.
        course = offers[0].course
        timePeriod = offers[0].timePeriod
        professor = offers[0].professor
        practical = offers[0].practical
        for offer in offers[1:]:
            if not offer.timePeriod == timePeriod:
                return None #if the timePeriod is diferent there is no name for this set of offers.
            if not offer.course == course:
                return None #if the course is diferent there is no name for this set of offers.
            if not professor == offer.professor:
                professor = None
            if practical != offer.practical:
                practical = None
        courseName = offers[0].course.name
        #Now checks if there are other offers in this course that have diferent professors and practical from this set
        otherOffers = Offer.find(course = course, timePeriod = timePeriod)
        otherProfessor = False
        otherPractical = False
        for otherOffer in otherOffers:
            if professor != None:
                if not otherOffer.professor == professor:
                    otherProfessor = True                    
            if practical != None:
                if otherOffer.practical != practical:
                    otherPractical = True
        #Now creats the name
        if otherProfessor:
            courseName = courseName + '[' + professor.name + ']'
        if otherPractical:
            if practical == 1:
                courseName = courseName + '(P)'
            else:
                courseName = courseName + '(T)'
        return courseName 


    @staticmethod
    def pickById(idOffer):
        """
         Searches for an offer with the same id as the value of the parameter idOffer.
         
         Return: one object of the class Offer, if successful, or none, if unsuccessful.

        @param int idOffer : Associated database key of the offer you are searching for.

        @return Offer :
        @author
        """
        cursor = MySQLConnection()
        try:
            offerData = cursor.execute('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer WHERE idOffer = ' + str(idOffer))[0]
        except:
            return None
        offer = Offer(TimePeriod.pickById(offerData[1]), Course.pickById(offerData[2]), offerData[3], offerData[4], Professor.pickById(offerData[5]))
        offer.setNumberOfRegistrations(offerData[6])
        offer.idOffer = offerData[0]
        offer.fillSchedules()
        return offer

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
         > idOffer
         > idCourse
         > professor
         > timePeriod
         > classNumber
         > practical
         > numberOfRegistration
         > schedule
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Offer.find(classNumber = 3, practical = True)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  Offer[]:
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        parameters = {}
        for key in kwargs:
            if key == 'course':
                parameters['idCourse'] = kwargs['course'].idCourse
            if key == 'professor':
                parameters['idProfessor'] = kwargs['professor'].idProfessor
            elif key == 'timePeriod':
                parameters['idTimePeriod'] = kwargs['timePeriod'].idTimePeriod
            elif key == 'schedule':
                parameters['idSchedule'] = kwargs['schedule'].idSchedule
            else:
                parameters[key] = kwargs[key]
        offersData = cursor.find('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer',parameters)
        offers = []
        for offerData in offersData:
            offer = Offer(TimePeriod.pickById(offerData[1]), Course.pickById(offerData[2]), offerData[3], offerData[4], Professor.pickById(offerData[5]))
            offer.setNumberOfRegistrations(offerData[6])
            offer.idOffer = offerData[0]
            offer.fillSchedules()
            offers.append(offer)
        return offers

    def store(self):
        """
         Creates or alters the professor's data in the database.
         
         Return: true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if False:
            if self.numberOfRegistrations == None:
                mySQLNumberOfRegistrations = 'NULL'  #in MySQL is NULL
            else:
                mySQLNumberofRegistrations = self.numberOfRegistrations
            if self.idOffer == None:
                offers = self.find(course = self.course, professor = self.professor, timePeriod = self.timePeriod, classNumber = self.classNumber, practical = self.practical, mySQLNumberOfRegistrations = self.numberOfRegistrations) #Schedule does not define the offer 
                if len(offers) > 0:
                    self.idOffer = offers[0].idOffer #Any offer that fit those paramaters is the same as this offer
                    return
                else: 
                    #Create this offer
                    query = 'INSERT INTO aggr_offer (idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations) VALUES(' + str(self.timePeriod.idTimePeriod) + ', ' + str(self.course.idCourse) + ', ' + str(self.classNumber) + ', ' + str(self.practical) + ', ' + str(self.professor.idProfessor) + ', ' + str(mySQLNumberOfRegistrations) + ')'
                    cursor.execute(query)
                    cursor.commit()
                    self.idOffer = self.find(course = self.course, professor = self.professor, timePeriod = self.timePeriod, classNumber = self.classNumber, practical = self.practical, mySQLNumberOfRegistrations = self.numberOfRegistrations)[0].idOffer
            else:
                #Update offer
                oldOffer = self.pickById(self.idOffer)
                query = 'UPDATE aggr_offer SET idTimePeriod = ' + str(self.timePeriod.idTimePeriod) + ', idCourse = ' + str(self.course.idCourse) + ', classNumber = ' + str(self.classNumber) + ', practical = ' + str(self.practical) + ', idProfessor = ' + str(self.professor.idProfessor) + ', numberOfRegistrations = ' + str(mySQLNumberOfRegistrations) + ' WHERE idOffer = ' + str(self.idOffer)
                cursor.execute(query)
                cursor.commit() 
        #Create the rel_offer_schedule
        idsScheduleOld = cursor.execute('SELECT idSchedule FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
        #First delete all the old relations
        for idScheduleOld in idsScheduleOld:
            cursor.execute('DELETE FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer) + ' AND idSchedule = ' + str(idScheduleOld[0]))
        #Now creates all the new relations
        for schedule in self.schedules:
            cursor.execute('INSERT INTO rel_offer_schedule (idOffer, idSchedule) VALUES (' + str(self.idOffer) + ', ' + str(schedule.idSchedule) + ')')
        cursor.commit() 
        
        return

    def delete(self):
        """
         Deletes the professor's data in the database.
         
         Return:  true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        if self.idOffer != None:
            cursor = MySQLConnection()
            if self == Offer.pickById(self.idOffer):
                cursor.execute('DELETE FROM rel_offer_schedule WHERE idOffer = ' + str(self.idOffer))
                cursor.execute('DELETE FROM aggr_offer WHERE idOffer = ' + str(self.idOffer))
                cursor.commit()
            else:
                raise OfferError("Can't delete non saved object.")
        else:
            raise OfferError('No idOffer defined.')



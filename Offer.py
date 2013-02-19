from TimePeriod import *
from Professor import *
from tools.MySQLConnection import *

class Offer(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key of this offer.

    idOffer  (public)

     The database ID of the course related to this offer.

    idCourse  (public)

     The professor responsible for this offer.

    professor  (public)

     The time period related to this offer.

    timePeriod  (public)

     The college class's number of this offer.

    classNumber  (public)

     It is True if this offer is a practical class, and False if it is a theoretical
     class.

    practical  (public)

     The number of max students allowed in this offer.

    numberOfRegistration  (public)

     List of schedules when the lectures related to this offer are held.

    schedules  (public)

    """

    def __init__(self, timePeriod, course, classNumber, practical, professor, numberOfRegistration):
        """
         Creates an Offer object if all the parameters needed are specified, except by
         the numberOfRegistration, which is not necessarily needed.

        @param TimePeriod timePeriod : The offer's time period.
        @param int idCourse : The offer's course associated database key.
        @param int classNumber : The college class's number of the offer.
        @param bool pratica : It's true if the offer is a practical class, and false if it is a theoretical class.
        @param Professor professor : The professor responsible for this offer.
        @param int numberOfRegistration : The maximum number of students allowed in this offer.
        @return  :
        @author
        """
        self.timePeriod = timePeriod
        #self.idCourse = course.idCourse #ainda nao esta implementado
        self.idCourse = course #temporary
        self.classNumber = classNumber
        self.practical = practical
        self.professor = professor
        self.numberOfRegistration = numberOfRegistration
        self.schedules = []
        self.idOffer = None

    def setProfessor(self, professor):
        """
         Associate a new professor with the offer.

        @param Professor professor : The new professorresponsable for this offer
        @return  :
        @author
        """
        self.professor = professor

    def getCourse(self):
        """
         Returns the Course object associated with the idCourse of this object.

        @return Course :
        @author
        """
        #return Course.pickById(self.idCourse)
        pass

    @staticmethod
    def pickById(idOffer):
        """
         Search an offer with the same id as the value of the parameter idOffer.
         
         Return: one object of the class Offer, if successful, or none, if unsuccessful.

        @param int idOffer : Associated database key of the offer you are searching for.

        @return Offer :
        @author
        """
        cursor = MySQLConnection()
        if isinstance(idOffer,int) or isinstance(idOffer,float):
            try:
                offerData = cursor.execute('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer WHERE idOffer = ' + str(idOffer))[0]
            except:
                return None
            schedulesData = cursor.execute('SELECT idSchedule FROM rel_offer_schedule WHERE idOffer = ' + str(idOffer))
            schedules = []
            for scheduleData in schedulesData:
                schedules.append(scheduleData[0])
            #                                                 temporary
            offer = Offer(TimePeriod.pickById(offerData[1]), offerData[2],   offerData[3], offerData[4], Professor.pickById(offerData[5]), offerData[6])
            if len(schedules)>0:
                offer.schedules = schedules
            offer.idOffer = offerData[0]
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

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        paramaters = {}
        for key in kwargs:
            if key == 'professor':
                paramaters['idProfessor'] = kwargs['professor'].idProfessor
            elif key == 'timePeriod':
                paramaters['idTimePeriod'] = kwargs['timePeriod'].idTimePeriod
            elif key == 'schedule':
                pass
            else:
                paramaters[key] = kwargs[key]

        offersData = cursor.find('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer',paramaters)
        offers = []
        for offerData in offersData:
            offer = Offer(TimePeriod.pickById(offerData[1]), offerData[2],   offerData[3], offerData[4], Professor.pickById(offerData[5]), offerData[6])
            offer.idOffer = offerData[0]
            offers.append(offer)
            
        return offers
    def store(self):
        """
         Creates or alters the professor's data in the data base.
         
         Return: true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        pass         

    def delete(self):
        """
         Deletes the professor's data in the data base.
         
         Return:  true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        pass




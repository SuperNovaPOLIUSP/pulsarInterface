from TimePeriod import TimePeriod
from Professor import Professor
import Course #To avoid cyclical import
from tools.MySQLConnection import MySQLConnection 

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

    numberOfRegistrationis  (public)

     List of schedules when the lectures related to this offer are held.

    schedules  (public)

    """

    def __init__(self, timePeriod, course, classNumber, practical, professor, numberOfRegistrations):
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
        self.timePeriod = timePeriod
        self.idCourse = course.idCourse
        self.classNumber = classNumber
        self.practical = practical
        self.professor = professor
        self.numberOfRegistrations = numberOfRegistrations
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
        return Course.Course.pickById(self.idCourse)

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
        try:
            offerData = cursor.execute('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer WHERE idOffer = ' + str(idOffer))[0]
        except:
            return None
        offer = Offer(TimePeriod.pickById(offerData[1]), Course.Course.pickById(offerData[2]),   offerData[3], offerData[4], Professor.pickById(offerData[5]), offerData[6])
        #offer.schedule = Schedule.find(idOffer = offerData[0]) #Not implemented
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

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  Offer[]:
        @author
        """
        cursor = MySQLConnection()
        #first prepare the kwargs for the MySQLConnection.find function
        parameters = {}
        for key in kwargs:
            if key == 'professor':
                parameters['idProfessor'] = kwargs['professor'].idProfessor
            elif key == 'timePeriod':
                parameters['idTimePeriod'] = kwargs['timePeriod'].idTimePeriod
            elif key == 'schedule': #COMPLETAR!!!!
                pass
            else:
                parameters[key] = kwargs[key]

        offersData = cursor.find('SELECT idOffer, idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations FROM aggr_offer',parameters)
        offers = []
        for offerData in offersData:
            offer = Offer(TimePeriod.pickById(offerData[1]), Course.Course.pickById(offerData[2]),   offerData[3], offerData[4], Professor.pickById(offerData[5]), offerData[6])
            offer.idOffer = offerData[0]
            #offer.schedule = Schedule.find(idOffer = self.idOffer) #Not implemented
            offers.append(offer)
        return offers

    def store(self):
        """
         Creates or alters the professor's data in the data base.
         
         Return: true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        if self.numberOfRegistrations == None:
            numberOfRegistrations = 'NULL'  #in MySQL is NULL
        else:
            numberofRegistrations = self.numberOfRegistrations
        if self.idOffer == None:
            offers = self.find(idCourse = self.idCourse, professor = self.professor, timePeriod = self.timePeriod, classNumber = self.classNumber, practical = self.practical, numberOfRegistrations = self.numberOfRegistrations) #schedule doesnt define the offer 
            if len(offers)>0:
                self.idOffer = offers[0].idOffer #Any offer that fit those paramaters is the same as this offer
            else: 
                #create this offer
                cursor = MySQLConnection()
                cursor.execute('INSERT INTO aggr_offer (idTimePeriod, idCourse, classNumber, practical, idProfessor, numberOfRegistrations) VALUES('+str(self.timePeriod.idTimePeriod)+', '+str(self.idCourse)+', '+str(self.classNumber)+', '+str(self.practical)+', '+str(self.professor.idProfessor)+', '+str(numberOfRegistrations)+')')
                cursor.commit()
                return True
        else:
            oldOffer = self.pickById(self.idOffer)
            query = 'UPDATE aggr_offer SET idTimePeriod = ' + str(self.timePeriod.idTimePeriod) + ', idCourse = ' + str(self.idCourse) + ', classNumber = ' + str(self.classNumber) + ', practical = ' + str(self.practical) + ', idProfessor = ' + str(self.professor.idProfessor) + ', numberOfRegistrations = ' + str(numberOfRegistrations) + ' WHERE idOffer = ' + str(self.idOffer)
            #Need to set the schedule offer relation
            cursor = MySQLConnection()
            print query
            try:
                cursor.execute(query)
                cursor.commit() 
                return True
            except:
                return False

    def delete(self):
        """
         Deletes the professor's data in the data base.
         
         Return:  true if successful or false if unsuccessful.

        @return bool :
        @author
        """
        if self.idOffer != None:
            try:
                cursor=MySQLConnection()
                self.idOffer = Offer.find(timePeriod = self.timePeriod, idCourse = self.idCourse, classNumber = self.classNumber, practical = self.practical, professor = self.professor, numberOfRegistrations = self.numberOfRegistrations, idOffer = self.idOffer)[0].idOffer
                cursor.execute('DELETE FROM aggr_offer WHERE idOffer = ' + str(self.idOffer))
                cursor.commit()
                return True
            except:
                return False
        else:
            return False



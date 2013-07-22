#coding: utf8
from Survey import *
from OpticalSheetField import *
from Cycle import *

class OpticalSheetError(Exception):
    """
     Exception reporting an error in the execution of a OpticalSheetColumn method.

    :version:
    :author:
    """
    pass



class OpticalSheet (object):

    """
     Contains the information of an Optical Sheet from the Data Base. It also makes
     and saves alterations.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idOpticalSheet  (public)

    A string specifying the type of survey that will be used as is defined by minitableSurveyType.

    surveyType  (public)

    Id related to surveyType, as defined in the minitableSurveyType.

    idSurveyType  (public)

     List of dictionaries in the form [{"term" : termOfTheCycle, "cycle" :
     cycleObject },{...].

    cycles  (public)

     List of surveys associated to this Optical Sheet.

    surveys  (public)

     A list of OpticalSheetField objects.

    fields  (public)

    """

    def __init__(self, surveyType):
        """
         

        @param string surveyType : A string specifying the type of survey that will be used as is defined by minitableSurveyType.
        @return  :
        @author
        """
        if not isinstance(surveyType, (str, unicode)):
            raise OpticalSheetError('Parameter surveyType must be a string')
        else:
            cursor = MySQLConnection()
            try:
                idSurveyType = cursor.execute('SELECT idSurveyType FROM minitableSurveyType WHERE typeName = "' + surveyType + '"')[0]
            except:
                raise OpticalSheetError('Parameter surveyType must be a defined in the minitableSurveyType')

        self.idSurveyType = idSurveyType
        self.surveyType = surveyType
        self.idOpticalSheet = None
        self.cycles = []
        self.surveys = []
        self.fields = []

    def addSurvey(self, questionnaire, assessmentNumber):
        """
         Creates and adds a survey to the surveys list with the parameters passed. In
         case there is already a servey belonging to the same assessment, or if it is not
         possible to add the survey for any other reason, returns False.

        @param undef questionnaire : Questionnaire to be associated to this Optical Sheet.
        @param undef assessmentNumber : if it is the first, the second, etc. assessment process made in this time period.
        @return  :
        @author
        """
        if self.idOpticalSheet == None:
            raise OpticalSheetError('idOpticalSheet parameter must be defined in order to add surveys')
        if not isinstance(questionnaire, Questionnaire) or not Questionnaire.pickById(questionnaire.idQuestionnaire) == questionnaire:
            raise OpticalSheetError('Parameter questionnaire must be a Questionnaire objects that exists in the database.')
        for survey in self.surveys:
            if survey.assessmentNumber == assessmentNumber:
                raise OpticalSheetError("There can't be more than one survey with the same assessment number in one opticalSheet.")
        self.surveys.append(Survey(self.idOpticalSheet, questionnaire, assessmentNumber))
        

    def removeSurvey(self, assessmentNumber):
        """
         Removes the survey from the list (surveys) with this assessmentNumber and
         returns False if it does not work.

        @param undef assessmentNumber : if it is the first, the second, etc. assessment process made in this time period.
        @return undef :
        @author
        """
        if not isinstance(assessmentNumber,(int, long)):
            raise OpticalSheetError("Parameter assessmentNumber must be int or long")
        self.surveys = [survey for survey in surveys if survey.assessmentNumber != assessmentNumber]

    def addOpticalSheetField(self, offers, index, encoded):
        """
         Adds an OpticalSheetField relating the set of offers to the code or courseIndex
         in this opticalSheet.

        @param Offer[] offers : List of offers to be appended to this Optical Sheet.
        @param int index : Index/code of the offers to be appended.
        @param bool encoded : List of offers to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if self.idOpticalSheet == None:
            raise OpticalSheetError('idOpticalSheet parameter must be defined in order to add offers')
        for offer in offers:
            #Check if is a valid Offer object
            if not isinstance(offer,Offer) or not Offer.pickById(offer.idOffer) == offer:
                raise OpticalSheetError('Parameter offers must be a list of Offer object that exists in the database.')
            #Create an OpticalSheetColumn for this offer and this index
            opticalSheetField = OpticalSheetColumn(self.idOpticalSheet, offer)
            if encoded:
                opticalSheetField.setCode(index)
            else:
                opticalSheetField.setCourseIndex(index)
            self.fields.append(opticalSheetField)


    def removeOpticalSheetField(self, index):
        """
         Removes an OpticalSheetField with the selected index in this opticalSheet.

        @param int index : Index/code of the offers to be removed.
        @return  :
        @author
        """
        if not isinstance(index,(int, long)):
            raise OpticalSheetError("Parameter index must be int or long")
        self.fields = [field for field in fields if field.code != index and field.courseIndex != index]

    def addCycle_Term(self, cycle, term):
        """
         Adds a cycle's term to the Optical  Sheet.

        @param Curriculo cycle : Cycle to be associated to this Optical Sheet
        @param int term : Term of the cycle to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(cycle,Cycle) or not cycle == Cycle.pickById(cycle.idCycle):
            raise OpticalSheetError('Parameter cycle must be a Cycle object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        cycles.append({'cycle':cycle, 'term':term})

    def removeCycle_Term(self, cycle, term):
        """
         Removes a cycle's term from this Optical Sheet.

        @param Curriculo cycle : Cycle to be associated to this Optical Sheet
        @param int term : Term of the cycle to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(cycle,Cycle) or not cycle == Cycle.pickById(cycle.idCycle):
            raise OpticalSheetError('Parameter cycle must be a Cycle object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        cycle.remove({'cycle':cycle,'term':term}) 


    def fillCycles(self):
        cursor = MySQLConnection()
        cyclesData = cursor.execute('SELECT idCycle, term FROM rel_cycle_opticalSheet WHERE idOPticalSheet = ' + str(self.idOpticalSheet))
        for cycleData in cyclesData:
            self.cycles.append({'cycle':Cycle.pickById(cycleData[0]), 'term':cycleData[1]})

    def fillOpticalSheetFields(self):
        cursor = MySQLConnection()
        fieldsData = cursor.execute('SELECT idOpticalSheetField FROM aggr_opticalSheetField WHERE idOpticalSheet = ' + str(self.idOpticalSheet))
        for fieldData in fieldsData:
            self.fields.append(OpticalSheetField.pickById(fieldData[0]))

    def fillSurveys(self):
        cursor = MySQLConnection()
        surveysData = cursor.execute('SELECT idSurvey FROM aggr_survey WHERE aggr_survey.idOpticalSheet = ' + str(self.idOpticalSheet))
        assessmentNumbers = []
        for surveyData in surveysData:
            survey = Survey.pickById(surveyData[0])
            if survey.assessmentNumber in assessmentNumbers:
                raise OpticalSheetError("There can't be more than one survey with the same assessment number in one opticalSheet.")
            assessmentNumbers.append(survey.assessmentNumber)
            self.surveys.append(survey)

    @staticmethod
    def pickById(idOpticalSheet):
        """
         Returns one complete Optical Sheet object where its ID is equal to the chosen.

        @param int idOpticalSheet : Associated data base key.
        @return OpticalSheet :
        @author
        """
        cursor = MySQLConnection()
        opticalSheetData = cursor.execute('SELECT minitableSurveyType.typeName FROM opticalSheet JOIN minitableSurveyType ON minitableSurveyType.idSurveyType = opticalSheet.idSurveyType WHERE opticalSheet.idOpticalSheet = ' + str(idOpticalSheet))
        if len(opticalSheetData) == 0:
            return None
        else:
            opticalSheetData = opticalSheetData[0]
        opticalSheet = OpticalSheet(opticalSheetData[0])
        opticalSheet.idOpticalSheet = idOpticalSheet
        opticalSheet.fillSurveys()
        opticalSheet.fillCycles()
        #opticalSheet.fillOpticalSheetFields() #it takes a long to do it
        return opticalSheet
        

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
         > idOpticalSheet
         > surveyType
         > cycles
         > term
         > questionnaires
         > offers
         > timePeriod
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. OpticalSheet.find(surveyType_like = "n", cycles = listOfCycleObjects, timePeriod = TimePeriodObject)

        @param undef _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        parameters = {}
        complement = ''
        for key in kwargs:
            if key == 'surveyType_equal':
                parameters['minitableSurveyType.typeName_equal'] = kwargs[key]
            elif key == 'surveyType_like':
                parameters['minitableSurveyType.typeName_like'] = kwargs[key]
            elif key == 'term':
                complement = ' JOIN rel_cycle_opticalSheet ON rel_cycle_opticalSheet.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['rel_cycle_opticalSheet.term'] = kwargs[key]
            elif key == 'cycles':
                complement = ' JOIN rel_cycle_opticalSheet ON rel_cycle_opticalSheet.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['rel_cycle_opticalSheet.idCycle'] = [cycle.idCycle for cycle in kwargs[key]]
            elif key == 'questionnaires':
                complement = ' JOIN aggr_survey ON aggr_survey.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['aggr_survey.idQuestionnaire'] = [questionnaire.idQuestionnaire for questionnaire in kwargs[key]]
            elif key == 'offers':
                complement = ' JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheet = opticalSheet.idOpticalSheet'
                parameters['aggr_opticalSheetField.idOffer'] = [offer.idOffer for offer in kwargs[key]]
            elif key == 'timePeriod':
                complement = ' JOIN aggr_opticalSheetField ON aggr_opticalSheetField.idOpticalSheet = opticalSheet.idOpticalSheet JOIN aggr_offer ON aggr_offer.idOffer = aggr_opticalSheetField.idOffer'
                parameters['aggr_offer.idTimePeriod'] = kwargs[key].idTimePeriod
            else:
                parameters['opticalSheet.' + key] = kwargs[key]
        opticalSheetsData = cursor.find('SELECT opticalSheet.idOpticalSheet, minitableSurveyType.typeName FROM opticalSheet JOIN minitableSurveyType ON minitableSurveyType.idSurveyType = opticalSheet.idSurveyType' + complement, parameters, ' GROUP BY opticalSheet.idOpticalSheet')
        opticalSheets = []
        for opticalSheetData in opticalSheetsData:
            opticalSheet = OpticalSheet(opticalSheetData[1])
            opticalSheet.idOpticalSheet = opticalSheetData[0]
            opticalSheet.fillSurveys()
            opticalSheet.fillCycles()
            opticalSheets.append(opticalSheet)
        return opticalSheets
           

    def store(self):
        """
         Saves the information in the database.

        @return  :
        @author
        """
        if self.idOpticalSheet == None:
            if len(self.fields) != 0 and len(self.cycles) != 0:  #In order to find out if this opticalSheet is already stored cycles and fields are needed
                opticalSheets = []
                for cycle in cycles:
                    opticalSheets = opticalSheets + OpticalSheet.find()
                
                

    def delete(self):
        """
         Deletes the information in the database.

        @return  :
        @author
        """
        pass




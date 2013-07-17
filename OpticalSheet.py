#coding: utf8
#from Questionario import *
from OpticalSheetColumn import *
#from Curriculum import *

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

     A string specifying the type of survey that will be used:
     e = Encoded
     n = not encoded

    surveyType  (public)

     List of dictionaries in the form [{"term" : termOfTheCurriculum, "curriculum" :
     curriculumObject },{...].

    curricula  (public)

     List of questionnaires associated to this Optical Sheet.

    questionnaires  (public)

     A list of OpticalSheetColumn objects.

    columns  (public)

    """

    def __init__(self, surveyType):
        """
         

        @param string surveyType : A string specifying the type of survey that will be used:
e = Encoded
n = not encoded
        @return  :
        @author
        """
        if surveyType != 'e' and surveyType != 'n':
            raise OpticalSheetError('Parameter surveyType must be "e" or "n"')
        self.surveyType = surveyType
        self.idOpticalSheet = None
        self.curricula = []
        self.questionnaires = []
        self.columns = [] 

    def addQuestionnaire(self, questionnaire):
        """
         Add a questionnaire to the questionnaires list. In case there is already a
         questionnaire belonging to the same assessment, or if it is not possible to add
         the questionnaire for any other reason, returns False.

        @param Questionario questionnaire : Questionnaire to be associated to this Optical Sheet.
        @return  :
        @author
        """
        pass

    def removeQuestionnaire(self, questionnaire):
        """
         Removes the questionnaire from the list (questionnaires) and returns False if it
         does not work.

        @param Questionario questionnaire : 
        @return bool :
        @author
        """
        pass

    def addOpticalSheetColumn(self, offers, index):
        """
         Adds an OpticalSheetColumn relating the set of offers to the code or courseIndex
         in this opticalSheet.

        @param Oferecimento[] offers : List of offers to be appended to this Optical Sheet.
        @param int index : Index/code of the offers to be appended.
        @return  :
        @author
        """
        #first check if all offers are ok
        for offer in offers:
            if not isinstance(offer,Offer) or not Offer.pickById(offer.idOffer) == offer:
                raise OpticalSheetError('Parameter offers must be a list of Offer object that exists in the database.')
            opticalSheetColumn = OpticalSheetColumn(offer)
            if self.surveyType == "e":
                opticalSheetColumn.setCode(index)
            else:
                opticalSheetColumn.setCourseIndex(index)
            self.columns.append(opticalSheetColumn)

    def removeOpticalSheetColumn(self, index):
        """
         Removes an OpticalSheetColumn with the selected index in this opticalSheet.

        @param int index : Index/code of the offers to be removed.
        @return  :
        @author
        """
        if not isinstance(index,(int, long)):
            raise OpticalSheetError("Parameter index must be int or long")
        columns = [column for column in columns if column.code != index and column.courseIndex != index]

    def addCurriculum_Term(self, curriculum, term):
        """
         Adds a curriculum's term to the Optical  Sheet.

        @param Curriculo curriculum : Curriculum to be associated to this Optical Sheet
        @param int term : Term of the curriculum to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(curriculum,Curriculum) or not curriculum == Curriculum.pickById(curriculum.idCurriculum):
            raise OpticalSheetError('Parameter curriculum must be a Curriculum object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        curricula.append({'curriculum':curriculum, 'term':term})

    def removeCurriculum_Term(self, curriculum, term):
        """
         Removes a curriculum's term from this Optical Sheet.

        @param Curriculo curriculum : Curriculum to be associated to this Optical Sheet
        @param int term : Term of the curriculum to be appended to this Optical Sheet.
        @return  :
        @author
        """
        if not isinstance(curriculum,Curriculum) or not curriculum == Curriculum.pickById(curriculum.idCurriculum):
            raise OpticalSheetError('Parameter curriculum must be a Curriculum object that exists in the database.')
        if not isinstance(term,(int,long)):
            raise OpticalSheetError('Parameter term must be a long or an int')
        curricula.remove({'curriculum':curriculum,'term':term}) 

    def pickById(self, idOpticalSheet):
        """
         Returns one complete Optical Sheet object where its ID is equal to the chosen.

        @param int idOpticalSheet : Associated data base key.
        @return OpticalSheet :
        @author
        """
        pass

    def store(self):
        """
         Saves the information in the database. Returns True if it is successful.

        @return bool :
        @author
        """
        pass

    def delete(self):
        """
         Deletes the information in the database. Returns True if it is successful.

        @return bool :
        @author
        """
        pass

    def find(self, _kwargs):
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
         > curricula
         > questionnaires
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. OpticalSheet.find(surveyType_like = "n", curricula =
         listOfCurriculumObjects)

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        pass




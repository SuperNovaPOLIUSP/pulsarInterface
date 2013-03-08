#from Questionario import *
#from Curriculum import *
#from Period import *

class OpticalSheet (object):

  """
   Contains the information of an Optical Sheet from the Data Base. It also makes
   and saves alterations.

  :version:
  :author:
  """

  """ ATTRIBUTES

   Associated data base key.

  idOpticalSheet  (public)

   e = Encoded
   n = not encoded

  ApplicationType  (public)

   List of dictionaries in the form [{"term":term of the curriculum,
   "curriculum":name of the curriculum },{...].

  curricula  (public)

   List of questionnaires associated to this Optical Sheet.

  questionnaires  (public)

   A dictionary in the format {index/code : Offer[],...} that describes the offers
   of each index or code.

  columns  (public)

  """

  def pickById(self, idOpticalSheet):
    """
     Returns one complete Optical Sheet object where its ID is equal to the chosen.

    @param int idOpticalSheet : Associated data base key.
    @return OpticalSheet :
    @author
    """
    pass

  def filterCurriculum_Term_Period(self, curriculum, Term, period):
    """
     Returns a list of Optical Sheets that have the curriculum, the term and the
     period chosen.

    @param Curriculum curriculum : 
    @param int Term : Term of the desired curriculum.
    @param Period period : The period associated to this Optical Sheet.
    @return  :
    @author
    """
    pass

  def addQuestionnaire(self, questionnaire):
    """
     Add a questionnaire to the questionnaires. In case there is already a
     questionnaire belonging to the same assessment, or it cannot add the
     questionnaire for any other reason, returns False.

    @param Questionario questionnaire : Questionnaire to be associated to this Optical Sheet.
    @return  :
    @author
    """
    pass

  def setColumn(self, offers, index):
    """
     Replace an index or a code of the dictionary (offers) by the list of offers
     given to this function. If the list is empty, the index or the code will be
     linked to nothing.

    @param Oferecimento[] offers : List of offers to be appended to this Optical Sheet.
    @param int index : Index/code of the offers to be appended.
    @return  :
    @author
    """
    pass

  def store(self):
    """
     Saves the information in the data base. Returns True if it is successful.

    @return bool :
    @author
    """
    pass

  def addCurriculum_Term(self, curriculum, term):
    """
     Adds a curriculum's term to the Optical  Sheet.

    @param Curriculo curriculum : Curriculum to be associated to this Optical Sheet
    @param int term : Term of the curriculum to be appended to this Optical Sheet.
    @return  :
    @author
    """
    pass

  def removeCurriculum_Term(self, curriculum, term):
    """
     Removes a curriculum's term from this Optical Sheet.

    @param Curriculo curriculum : Curriculum to be associated to this Optical Sheet
    @param int term : Term of the curriculum to be appended to this Optical Sheet.
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




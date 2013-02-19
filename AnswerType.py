#coding: utf8

from tools.MySQLConnection import MySQLConnection

class AnswerType(object):
  
    """
     Class that represents a category of multiple choice answers that a question can
     be related to (e. g. the category "hours" may refer to different ammounts of
     hours specified by alternatives A to E).
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     Associated database key.
  
    idAnswerType  (public)
  
     A dictionary containing the meaning of the answers alternative choices in the
     form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
  
    alternativeMeaning  (public)
  
     The name of  the AnswerType category (e.g. hours, frequency).
  
    category  (public)
  
    """
  
    def __init__(self, category, alternativeMeaning):
        """
         Constructor method.
         Name and meaning are the necessary data to create an AnswerType.
  
        @param string category : The name of  the AnswerType category (e.g. hours, frequency).
        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        # verifies if category is a proper parameter
        if isinstance(category, unicode):
            self.category = category
            # verifies if alternativeMeaning is a proper parameter
            if isinstance(alternativeMeaning, dict):
                if len(alternativeMeaning) is 5:
                    if 'A' and 'B' and 'C' and 'D' and 'E' in alternativeMeaning.keys():
                        self.alternativeMeaning = alternativeMeaning

    @staticmethod
    def pickById(idAnswerType):
        """
         Returns an AnswerType object given an idAnswerType.
         
  
        @param int idAnswerType : Associated database key.
        @return AnswerType :
        @author
        """

        databaseConnection = MySQLConnection() # gets connection with the mysql database

        category = databaseConnection.execute("SELECT name FROM answerType WHERE idAnswerType = " + str(idAnswerType))[0][0]

        alternativeMeaning = databaseConnection.execute("SELECT alternative, meaning FROM alternativeMeaning WHERE idAnswerType = " + str(idAnswerType))
        alternativeMeaning = {alternative : meaning for (alternative, meaning) in alternativeMeaning}

        pickedAnswerType = AnswerType(category, alternativeMeaning)
        pickedAnswerType.idAnswerType = idAnswerType

        return pickedAnswerType
  
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
         > idAnswerType
         > category_equal or category_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E.g. AnswerType.find(category_equal = "time", campus_like = "Main")
  
        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return AnswerType[] :
        @author
        """
        pass
  
    def store(self):
        """
         Changes object on table or adds it to database if an object is absent. Returns
         True if object is stored and False if it fails.
  
        @return bool :
        @author
        """
        pass
  
    def delete(self):
        """
         Deletes object from the database. Returns True if the object was successfully
         deleted and False if it fails.
  
        @return bool :
        @author
        """
        pass

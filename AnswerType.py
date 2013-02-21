#coding: utf8

from tools.MySQLConnection import MySQLConnection

class AnswerType(object):
  
    """
     Class that represents a category of multiple choice answers that a question can
     be related to (e. g. the answer type "hours" may refer to different ammounts of
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
  
     The name of the AnswerType related to a category of answers (e.g. hours, frequency).
  
    name  (public)
  
    """
  
    def __init__(self, name, alternativeMeaning):
        """
         Constructor method.
         Name and meaning are the necessary data to create an AnswerType.
  
        @param string name : The name of  the AnswerType related to a category of answers (e.g. hours, frequency).
        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        # verifies if name is a proper parameter
        if isinstance(name, unicode):
            self.name = name
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

        # gets connection with the mysql database
        databaseConnection = MySQLConnection() 

        # finds the name of the answer type through the answerType table
        name = databaseConnection.execute("SELECT name FROM answerType WHERE idAnswerType = " + str(idAnswerType))[0][0]

        # finds the meaning of each alternative associated to the answer type through the alternativeMeaning table
        alternativeMeaning = databaseConnection.execute("SELECT alternative, meaning FROM alternativeMeaning WHERE idAnswerType = " + str(idAnswerType))
        # turns de result found into a dictionary
        alternativeMeaning = {alternative : meaning for (alternative, meaning) in alternativeMeaning}

        # creates the AnswerType object to be returned
        pickedAnswerType = AnswerType(name, alternativeMeaning)
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
         > name_equal or name_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E.g. AnswerType.find(name_equal = "time")
  
        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return AnswerType[] :
        @author
        """

        # gets connection with the mysql database
        databaseConnection = MySQLConnection()

        # finds the database IDs of the answer types that need to be found
        foundAnswerTypeIds = databaseConnection.find("SELECT idAnswerType FROM answerType", kwargs)

        # for each id found, creates an AnswerType object using the 'pickById' method
        foundAnswerTypes = []
        for Id in foundAnswerTypeIds:
            foundAnswerTypes.append(AnswerType.pickById(Id[0]))

        return foundAnswerTypes        
  
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

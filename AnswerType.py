#coding: utf8

from tools.MySQLConnection import MySQLConnection

class AnswerTypeError(Exception):
    """
     Exception that reports errors during the execution of AnswerType class methods
  
    :version:
    :author:
    """
    pass

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

    idAnswerType  (private)

     A dictionary containing the meaning of the answers alternative choices in the
     form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}

    alternativeMeaning  (private)

     The name of the AnswerType related to a category of answers (e.g. hours, frequency).

    name  (private)

    """

    def __init__(self, name, alternativeMeaning):
        """
         Constructor method.
         Name and meaning are the necessary data to create an AnswerType.

        @param string name : The name of the AnswerType related to a category of answers (e.g. hours, frequency).
        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        self.setName(name)
        self.setAlternativeMeaning(alternativeMeaning)

    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         equal.

        @param AnswerType other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        if not isinstance(other, AnswerType):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         not equal.

        @param AnswerType other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    def setName(self, name):
        """
         Changes the name of the category related to the answer type.

        @param string name : The name of the AnswerType related to a category of answers (e.g. hours, frequency).
        @return  :
        @author
        """
        # verifies if name is a proper parameter
        if isinstance(name, (unicode, str)):
            self.name = name
        else:
            raise AnswerTypeError("Invalid name parameter. It must be of type str or unicode.")

    def setAlternativeMeaning(self, alternativeMeaning):
        """
         Changes the set of alternative meanings of the answer type.

        @param string{} alternativeMeaning : A dictionary containing the meaning of the answers alternative choices in the form { 'A':'meaningA' , 'B':'meaningB' , ..., 'E':'meaningE'}
        @return  :
        @author
        """
        # verifies if alternativeMeaning is a proper parameter
        if isinstance(alternativeMeaning, dict):
            if len(alternativeMeaning) is 5:
                if 'A' and 'B' and 'C' and 'D' and 'E' in alternativeMeaning.keys():
                    for meaning in alternativeMeaning.values():
                        if not isinstance(meaning, unicode) and not isinstance(meaning, str):
                            raise AnswerTypeError("Invalid meaning found.")
                    self.alternativeMeaning = alternativeMeaning
                else:
                    raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")
            else:
                raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")
        else:                    
            raise AnswerTypeError("Invalid set of alternatives. The parameter alternativeMeaning must be a dictionary with five keys, each key being a leter from A to E.")

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
         > meaning_equal or meaning_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.

         In this method: the parameter meaning_like refers to a list of words that must 
         be all present in the alternatives of the object that needs to be found; and 
         the parameter meaning_equal refers to a dictionary containing the exact 
         alternatives of the object that needs to be found.

         E. g. AnswerType.find(name_equal = "time", meaning_like = ["very", "interesting", "good", "less", "bad", "issue"])

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        # gets connection with the mysql database
        databaseConnection = MySQLConnection()

        # finds the database IDs of the answer types that need to be found
        foundAnswerTypeIdsByMeaning = []

        if "meaning_like" in kwargs:
            # finds the IDs of the database objects that contains all the meanings in the list that was passed
            query = "SELECT idAnswerType FROM alternativeMeaning WHERE meaning LIKE '%" + "%' AND meaning LIKE '%".join(kwargs['meaning']) + "%'"
            foundAnswerTypeIdsByMeaning = databaseConnection.execute(query)

            # changes the resoult found to a list, instead of a tuple of tuples
            foundAnswerTypeIdsByMeaning = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIdsByMeaning]

            # removes the 'meaning_like' key from kwargs in order to call the MySQLConnection find method
            del kwargs['meaning_like']

        elif "meaning_equal" in kwargs:
            # finds the IDS of the database objects that contains the dictionary of meanings passed
            for alternative, meaning in kwargs['meaning_equal'].items():
                # find the IDs for a specific alternative and its meaning
                foundAnswerTypeIdsByAlternativeAndMeaning = databaseConnection.execute("SELECT idAnswerType FROM alternativeMeaning WHERE alternative = '" + alternative + "' AND meaning = '" + meaning + "'")
                foundAnswerTypeIdsByAlternativeAndMeaning = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIdsByAlternativeAndMeaning]
                # adds the IDs found for this specific alternative to the list of all IDs found
                foundAnswerTypeIdsByMeaning += foundAnswerTypeIdsByAlternativeAndMeaning

            # excludes duplicate IDs from the list by turning it to a set and back again to a list
            foundAnswerTypeIdsByMeaning = list(set(foundAnswerTypeIdsByMeaning))

            # removes the 'meaning_equal' key from kwargs in order to call the MySQLConnection find method
            del kwargs['meaning_equal']

        # gets the intersection of the previously found IDs with those which will be found when searching for the names of the answer types, but only if necessary
        if len(foundAnswerTypeIdsByMeaning) > 0:
            # finds the IDs of the database objects that contain the name or the idAnswerType specified in kwargs
            foundAnswerTypeIds = databaseConnection.find("SELECT idAnswerType FROM answerType", kwargs)
            foundAnswerTypeIds = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIds]

            # gets the intersection between the two sets of IDs that were found
            foundAnswerTypeIds = list(set(foundAnswerTypeIds).intersection(foundAnswerTypeIdsByMeaning))

        else:
            foundAnswerTypeIds = databaseConnection.find("SELECT idAnswerType FROM answerType", kwargs)
            foundAnswerTypeIds = [int(foundAnswerTypeId[0]) for foundAnswerTypeId in foundAnswerTypeIds]

        # for each ID found, creates an AnswerType object using the 'pickById' method
        foundAnswerTypes = []
        for Id in foundAnswerTypeIds:
            foundAnswerTypes.append(AnswerType.pickById(Id))

        return foundAnswerTypes

    def store(self):
        """
         Changes object on table or adds it to database if an object is absent.

        @return  :
        @author
        """
        # gets connection with the mysql database
        databaseConnection = MySQLConnection()
        
        # verifies if the database already has an object like the one to be stored
        exists = False
        '''
        try:
            # se alternativa existe e nome não existe ou se alternativa não existe e nome existe, altera
            if 
            # se alternativa exite e nome existe, havendo mais de um id, apaga todos os ids e cria um novo
            # se alternativa existe e nome existe, havendo apenas um id, pega o id se necessário
            # se alternativa não existe e nome não existe, cria um novo
            if len(AnswerType.find(name_equal = self.name)) > 0:
                pass
        '''
                


        '''
        # verifies if the database already has an object like the one to be stored
        try:
            # verifies if the database possesses instances of the object
            if len(databaseConnection.execute("SELECT * FROM answerType WHERE idAnswerType = " + str(self.idAnswerType))) > 0:
                # updates the database instance of the object
                databaseConnection.execute("UPDATE answerType SET name = " + self.name + " WHERE idAnswerType = " + str(self.idAnswerType))
                databaseConnection.execute("UPDATE answerType SET alternative = " + alternative + ", meaning = " + meaning + " WHERE idAnswerType = " + str(self.idAnswerType))

                # validates the updates made in the database
                # databaseConnection.commit()
                return True

            else: 
                # if the query was successful and no result was returned, the object has an invalid database ID
                raise MySQLQueryError("Invalid AnswerType database ID")
        except:
            # creates new instance, for this object, in the database
            databaseConnection.execute("INSERT INTO answerType (name) VALUES (" + self.name)
        '''

    def delete(self):
        """
         Deletes object from the database.

        @return  :
        @author
        """
        pass

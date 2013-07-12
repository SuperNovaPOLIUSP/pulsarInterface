from Answer import *
from Answer[] import *
from {} import *

class Datafile(object):

    """
     Class representing a file which contains several answers read from several
     optical sheets.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idDatafile  (public)

     The file name of the datafile (e.g. "ae_poli_20101_1cb_1_n.dat").

    fileName  (public)

     List of answers that the datafile keeps.

    answers  (public)

    """

    def __init__(self, fileName):
        """
         Constructor method.

        @param string fileName : The file name of the datafile (e.g. "ae_poli_20101_1cb_1_n.dat").
        @return  :
        @author
        """
        pass

    def setAnswers(self, answers):
        """
         Sets the object's list containing the answers kept by the datafile.

        @param Answer[] answers : List of answers that the datafile keeps.
        @return  :
        @author
        """
        pass

    def pickById(self, idDataFile):
        """
         Returns one complete Datafile object where its ID is equal to the chosen.

        @param int idDataFile : Object's associated database key.
        @return Datafile :
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
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idDatafile
         > fileName_like
         > fileName_equal
         > answers
         
         E. g. Datafile.find(fileName_like = "1cb")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        pass

    def store(self):
        """
         Stores the information in the database.

        @return  :
        @author
        """
        pass

    def delete(self):
        """
         Deletes the information from the database.

        @return  :
        @author
        """
        pass




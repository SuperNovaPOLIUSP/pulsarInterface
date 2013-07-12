from Answer import *
from Answer[] import *
from {} import *

class DatafileError(Exception):
    """
    Exception reporting an error in the execution of a Datafile method.

    :version:
    :author:
    """
    pass

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
        #Parameters verification:
        if not isinstance(fileName, (str, unicode))
            raise DatafileError('Parameter filename must be a string or unicode.')

        # Setting parameters
        self.fileName = fileName
        #Setting None parameters
        self.idDatafile = None
        self.answers = []

    def __eq__(self,other):
        if not isinstance(other, Datafile):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self,other):
        return not self.__eq__(other)

    def setAnswers(self, answers):
        """
         Sets the object's list containing the answers kept by the datafile.

        @param Answer[] answers : List of answers that the datafile keeps.
        @return  :
        @author
        """
        if not isinstance (answers, list):
            raise DatafileError('Parameter answers must be a list of answers')
        for answer in answers:
            if not isinstance (answer, Answer):
                raise DatafileError('Each item on list must be an Answer object')
        self.answers = answers

    def getAnswers(self):
        answers = []
        answerData = cursor.execute('SELECT idAnswer FROM answer WHERE idDatafile = ' + str(self.idDatafile))
        if answerData:
            for idAnswer in answerData:
                answers.append(Answer.pickById(idAnswer[0]))
        return answers

    def pickById(self, idDataFile):
        """
         Returns one complete Datafile object where its ID is equal to the chosen.

        @param int idDataFile : Object's associated database key.
        @return Datafile :
        @author
        """
        cursor = MySQLConnection()
        try:
            datafileData = cursor.execute('SELECT idDatafile, fileName FROM datafile where idDatafile = ' + str(idDatafile))[0]
        except:
            return None
        datafile = Datafile(datafileData[1])
        datafile.idDatafile = datafileData[0]
        datafile.setAnswers(datafile.getAnswers())
        return datafile

    def find(self, **kwargs):
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
         
         E. g. Datafile.find(fileName_like = "1cb")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        datafiles = []
        datafileData = cursor.find('SELECT idDatafile, fileName FROM datafile', kwargs)
        try:
            for objectData in datafileData:
                datafile = Datafile(objectData[1])
                datafile.idDatafile = objectData[0]
                datafile.setAnswers(datafile.getAnswers())
                datafiles.append(datafile)
        except:
            return []
        return datafiles

    def store(self):
        """
         Stores the information in the database.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if Datafile.find(fileName = self.fileName):
            cursor.execute('UPDATE datafile SET fileName = '+ self.fileName + ' WHERE idDatafile = '+ str(self.idDatafile))
        else: 
            cursor.execute('INSERT INTO datafile (fileName) VALUES (' + self.fileName + ')')
            self.idDatafile = Datafile.find(fileName = self.fileName)[0].idDatafile
        cursor.commit()

    def delete(self):
        """
         Deletes the information from the database.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        cursor.execute('DELETE FROM datafile WHERE idDatafile = ' + str(self.idDatafile))
        cursor.commit()


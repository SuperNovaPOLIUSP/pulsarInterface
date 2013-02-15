#encoding: utf8
from tools.MySQLConnection import MySQLConnection

class Professor(object):

    """
     A professor

    :version:
    :author:
    """

    """ ATTRIBUTES

     The professor's name.

    name  (public)

     Associated data base key.

    idProfessor  (public)

    """

    def __init__(self, name):
        """
         Professor's name is the basic attribute for creating a professor in your data
         base.

        @param string name : The professor's name.
        @return  :
        @author
        """
        self.name = name
        self.idProfessor = None

    @staticmethod
    def pickById(idProfessor):
        """
         Returns a single professor with the chosen ID.

        @param int idProfessor : Associated data base key.
        @return Professor :
        @author
        """
        
        cursor = MySQLConnection()
        query = '''SELECT * FROM professor
        WHERE idProfessor = 
        ''' + str(idProfessor)
        name = cursor.execute(query)[0][2]
        professor = Professor(name)
        professor.idProfessor = idProfessor
        return professor        

    @staticmethod
    def pickByName(name):
        """
         Returns a single professor with the chosen name.

        @param string name : The professor's name
        @return Professor :
        @author
        """
        cursor = MySQLConnection()
        query = '''SELECT * FROM professor
        WHERE name = 
        ''' + '"'+ name +'"'
        professor = Professor(name)
        professor.idProfessor = cursor.execute(query)[0][0]
        return professor

    @staticmethod
    def findName(name):
        """
         Returns a list of professors with the name that contains the chosen one.

        @param string name : The professor's name.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = '''SELECT * FROM professor
        WHERE name LIKE 
        ''' + '"%'+ name +'%"'
        professorTargets = []
        professorData = cursor.execute(query)
        for professorDatum in professorData:
            professorTarget = Professor(professorDatum[2])
            professorTarget.idProfessor = professorDatum[0]
            professorTargets.append(professorTarget)
        return professorTargets

    def store(self):
        """
         Creates or alters the professor's data in the data base.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        column = [memberId, name]
        values = []
        try:
            self.memberID
        except:
            self.memberID = 0
        values.append(self.memberID)
        values.append(self.name)
        try:
            self.office
            column.append(office)
            values.append(self.office)
        except:
            print "'office' column set as null"
        try:
            self.email
            column.append(email)
            values.append(self.email)
        except:
            print "'email' column set as null"
        try:
            self.phoneNumber
            column.append(phoneNumber)
            values.append(self.phoneNumber)
        except:
            print "'phoneNumber' column set as null"
        try:
            self.cellphoneNumber
            column.append(cellphoneNumber)
            values.append(self.cellphoneNumber)
        except:
            print "'cellphoneNumber' column set as null"
        query = "INSERT INTO professor " + str(tuple(column)) + " VALUES " + str(tuple(values))
        #returns 0 if insertion is ok, returns 1 if error
        try:
            cursor.execute(query)
            return 0
        except:
            return False

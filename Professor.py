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
        pass




#encoding: utf8
from ae2012.models import *

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
        name = docente.objects.filter(id = idProfessor).values('nome')[0]['nome']
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
        professor = Professor(name)
        professor.idProfessor = docente.objects.filter(nome = name).values('id')[0]['id']
        return professor

    @staticmethod
    def findName(name):
        """
         Returns a list of professors with the name that contains the chosen one.

        @param string name : The professor's name.
        @return  :
        @author
        """
        professorData = docente.objects.filter(nome__contains = name).values('nome','id')
        professorTargets = []
        for professorDatum in professorData:
            professorTarget = Professor(professorDatum['nome'])
            professorTarget.idProfessor = professorDatum['id']
            professorTargets.append(professorTarget)
        return professorTargets

    def store(self):
        """
         Creates or alters the professor's data in the data base.

        @return  :
        @author
        """
        pass




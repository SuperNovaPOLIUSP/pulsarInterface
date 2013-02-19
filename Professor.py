#encoding: utf8
from tools.MySQLConnection import MySQLConnection
from Department import *

class Professor(object):

    """
     Representation of a professor in the data base.

    :version:
    :author:
    """

    """ ATTRIBUTES

     The professor's name.

    name  (public)

     Associated data base key.

    idProfessor  (public)

     Associated database key of the professor's department.

    idDepartment  (private)

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
        self.office = None
        self.email = None
        self.phoneNumber = None
        self.cellphoneNumber = None

    @staticmethod
    def pickById(idProfessor):
        """
         Returns a single professor with the chosen ID.

        @param int idProfessor : Associated data base key.
        @return Professor :
        @author
        """
        if not (isinstance(idProfessor,int) or isinstance(idProfessor,float)):
            return None
        cursor = MySQLConnection()
        query = 'SELECT * FROM professor WHERE idProfessor =  '+ str(idProfessor)
        name = cursor.execute(query)[0][2]
        professor = Professor(name)
        professor.idProfessor = idProfessor
        return professor

    def store(self):
        """
         Creates or alters the professor's data in the data base.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        column = [memberId, name]
        values = []
        if self.memberID is None:
            self.memberID = 0
        values.append(self.memberID)
        values.append(self.name)
        if self.office is not None:
            column.append(office)
            values.append(self.office)
        if self.email is not None:
            column.append(email)
            values.append(self.email)
        if self.phoneNumber is not None:
            column.append(phoneNumber)
            values.append(self.phoneNumber)
        if self.cellphoneNumber is not None:
            column.append(cellphoneNumber)
            values.append(self.cellphoneNumber)
        query = "INSERT INTO professor " + str(tuple(column)) + " VALUES " + str(tuple(values))
        #returns True if insertion is ok, returns False if error
        try:
            cursor.execute(query)
            return True
        except:
            return False

    def delete(self):
        """
         Deletes the professor's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        query = "DELETE FROM professor WHERE idProfessor = " + str(self.idProfessor) + " AND name = " + str(self.name)
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False

    def setDepartment(self, department):
        """
         With the Department objects given set the idDepartment.

        @param Department department : 
        @return  :
        @author
        """
        cursor = MySQLConnection()
        #Checking if professor is already related to a department
        if len(cursor.execute("SELECT idProfessor FROM rel_department_professor WHERE idProfessor = " +str(self.idProfessor))) > 0:
            query = "UPDATE rel_department_professor SET idDepartment=" +str(department.idDepartment) +"WHERE idProfessor=" +str(self.idProfessor)
        else:
            values = (self.idProfessor, department.idDepartment)
            query = "INSERT INTO rel_department_professor (idProfessor, idDepartment) VALUES " +str(values)
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False

    def getDepartment(self):
        """
         Returns the Department object associated with the idDepartment of this object.

        @return Department :
        @author
        """
        cursor = MySQLConnection()
        query = '''SELECT idDepartment, name, departmentCode FROM rel_department_professor JOIN department
ON rel_department_professor.idDepartment = department.idDepartment
WHERE idProfessor = ''' + str(self.idProfessor)
        try:
            professor_sql = cursor.execute(query)
        except:
            return None
        department = Department(professor_sql[0][1], professor_sql[0][2])
        department.idDepartment = department_sql[0][0]
        return department

    def find(self, _kwargs):
        """
         Searches the database to find one or more objects that fit the description
         sepcified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing offers in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idProfessor
         > name_equal or name_like
         > department
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Professor.find(name_like = "Some Na", department = departmentObject)

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        pass




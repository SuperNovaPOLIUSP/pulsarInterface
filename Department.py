from tools.MySQLConnection import MySQLConnection

class Department(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idDepartment  (public)

     Department name.

    name  (public)

     A string code that represents the department

    departmentCode  (public)

    """
    
    def __init__(self, name, departmentCode):
        """
         

        @param string name : Department name
        @param string departmentCode : 
        @return  :
        @author
        """
        self.name = name
        self.departmentCode = departmentCode


    @staticmethod
    def pickById(idDepartment):
        """
         Returns a Department object with the chosen idDepartment.

        @param int idDepartment : Associated database key.
        @return Department :
        @author
        """
        if not isinstance(idDepartment,int):
            return None
        cursor = MySQLConnection()
        query = 'SELECT * FROM department WHERE idDepartment = ' + str(idDepartment)
        department_sql = cursor.execute(query)
        department = Department(department_sql[0][1], department_sql[0][2])
        department.idDepartment = idDepartment
        return department

    def find(self, **kwargs):
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
         > idDepartment
         > name_equal or name_like
         > departmentCode_equal or departmentCode_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Department.find(name_equal = "Department of Computer Science",
         departmentCode_like = "MAC")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        pass

    def store(self):
        """
         Creates or changes the department's data in the database.
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        column = [name, departmentCode]
        try:
            values = [self.name, self.departmentCode]
        except:
            print "Values error"
            return 1        
        query = "INSERT INTO department " + str(tuple(column)) + " VALUES " + str(tuple(values))
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False

    def delete(self):
        """
         Deletes the department's data in the database.
         Return: True if succesful or False otherwise.

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        query = "DELETE FROM department WHERE idDepartment = " + str(self.idDepartment) + " AND name = " + str(self.name) + " AND departmentCode = " + str(self.departmentCode)
        try:
            cursor.execute(query)
            cursor.commit()
            return True
        except:
            return False




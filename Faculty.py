from tools.MySQLConnection import *
class Faculty(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated data base key.

    idFaculty  (public)

     Faculty's name

    name  (public)

     The faculty's abbreviation.

    abbreviation  (public)

     Faculty's campus.

    campus  (public)

     Faculty's city.

    city  (private)

    """

    def __init__(self, name, abbreviation, campus, city):
        """
         Only the name ad the abbreviation are needed, the other 2 can be None.

        @param string name : Faculty's name
        @param string abbreviation : Faculty's abbreviation.
        @param string campus : Faculty's campus, it can be None
        @param string city : Faculty's campus, it can be None.
        @return  :
        @author
        """
        self.name = name
        self.abbreviation = abbreviation
        self.campus = campus
        self.city = city
        self.idFaculty = None
    
    @staticmethod
    def pickById(idFaculty):
        """
         Returns a single complete Faculty with the chosen ID.

        @param int idFaculty : Associated data base key.
        @return Faculty :
        @author
        """
        cursor = MySQLConnection()
        if isinstance(idFaculty,int):
            try:
                facultyData = cursor.execute('SELECT name,abbreviation,campus,city,idFaculty FROM faculty WHERE idFaculty = ' + str(idFaculty))[0]
            except:
                return None
            faculty = Faculty(facultyData[0], facultyData[1], facultyData[2], facultyData[3])
            faculty.idFaculty = facultyData[4]
            return faculty
        else:
            return None 
    
    def delete(self):
        """
         Deletes the faculty's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        if self.idFaculty != None:
            cursor = MySQLConnection()
            try:
                cursor.execute('DELETE FROM faculty WHERE idFaculty = ' + str(self.idFaculty))
                cursor.commit()
                return True
            except:
                pass
        return False

    def store(self):
        """
         Creates or changes the faculty's data in the data base.
         
         Return: true if succesful or false otherwise

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        if self.idFaculty == None:
            #Search for idFaculty
            possibleIdsQuery = 'SELECT idFaculty FROM faculty WHERE name = "'+self.name+'"'
            if self.campus != None:
                possibleIdsQuery = possibleIdsQuery + ' AND campus = "' + self.campus + '"'
            if self.city != None:
                possibleIdsQuery = possibleIdsQuery + ' AND city = "' + self.city + '"' 
            possibleIds = cursor.execute(possibleIdsQuery)
            if len(possibleIds) > 0:
                self.idFaculty = possibleIds[0][0]   #Since all results are the same faculty pick the first one.

            else:
                #If there is no idFaculty create row
                try:
                    cursor.execute('INSERT INTO faculty (name, abbreviation, campus, city) VALUES("'+self.name+'", "'+self.abbreviation+'", "'+self.campus+'", "'+self.city+'")')
                    cursor.commit()
                    self.idFaculty = cursor.execute('SELECT idFaculty FROM faculty WHERE name = "'+self.name+'" AND abbreviation = "'+self.abbreviation+'" AND campus = "'+self.campus+'" AND city = "'+self.city+'"')[0][0]
                    return True
                except:
                   return False
 
        #If there is an idFaculty try to update row
        oldData = cursor.execute('SELECT name, abbreviation, city, campus FROM faculty WHERE idFaculty = ' + str(self.idFaculty))[0] #in a search for id there is only one row
        query = 'UPDATE faculty SET '
        #Find the complements to be added to the query
        complements = []
        if oldData[0] != self.name:
            complements.append('name = "' + self.name + '"') 
        if oldData[1] != self.abbreviation:
            complements.append('abbreviation = "' + self.abbreviation + '"')
        if oldData[2] != self.city:
            complements.append('city = "' + self.city + '"')
        if oldData[3] != self.campus:
            complements.append('campus = "' + self.campus + '"')
        #Now join the complements with the query
        if len(complements)>0:
            query = query + ', '.join(complements)
            query = query + ' WHERE idFaculty = ' + str(self.idFaculty)
            print query
            #Execute the changes
            try:
                cursor.execute(query)
                cursor.commit()
                return True
            except:
                pass
        else:
            #Nothing to change
            return True
        return False

    @staticmethod
    def find(**kwargs):
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
         > idFaculty
         > name_equal or name_like
         > abbreviation_equal or abbreviation_like
         > campus_equal or campus_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. faculty.find(name_equal = "Faculty of Enginieering", campus_like = "Main")

        @param dictionary _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        facultiesData = cursor.find('SELECT name, abbreviation, campus, city, idFaculty FROM faculty',kwargs)
        faculties = []
        for facultyData in facultiesData:
            faculties.append(Faculty(facultyData[0], facultyData[1], facultyData[2], facultyData[3]))
        return faculties


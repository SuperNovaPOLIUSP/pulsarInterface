from Offer import *

class OpticalSheetColumnError(Exception):
    """
     Exception reporting an error in the execution of a OpticalSheetColumn method.

    :version:
    :author:
    """
    pass


class OpticalSheetColumn(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idOpticalSheetColumn  (public)

     Associated database key of the related opticaSheet.

    idOpticalSheet  (public)

     The Offer Object of this relation.

    offer  (public)

     The code of this relation, is None if the opticalSheet is not coded.

    code  (public)

     The position (column) where this offer is in the opticalSheet, more than one
     OpticalSheetColumn have the same courseIndex, is None if the opticalSheet is
     coded.

    courseIndex  (public)

    """

    def __init__(self, offer):
        """
         Constructur method.

        @param int idOpticalSheet : Associated database key of the related opticaSheet
        @param Offer offer : The Offer Object of this relation.
        @return  :
        @author
        """
        if not isinstance(offer,Offer) or not Offer.pickById(offer.idOffer) == offer:
            raise OpticalSheetColumnError('Parameter offer must be an Offer object that exists in the database.')

        self.offer = offer
        self.idOpticalSheet = None 
        self.code = None
        self.courseIndex = None 
        self.idOpticalSheetColumn = None
    
    def __eq__(self, other):
        if not isinstance(other, OpticalSheetColumn):
            return False
        return self.__dict__ == other.__dict__
  
    def __ne__(self,other):
        return not self.__eq__(other)

    def setCode(self, code):
        """
         Set the code of this relation, it should only be used if the OpticalSheet is
         coded.

        @param int code : The code of this relation.
        @return  :
        @author
        """
        if not isinstance(code,(int,long)):
            raise OpticalSheetColumnError('code must be and int or long')
        self.code = code

    def setIdOpticalSheet(self, idOpticalSheet):

        if not isinstance(idOpticalSheet,(int,long)):
            raise OpticalSheetColumnError('idOpticalSheet must be and int or long')
        self.idOpticalSheet = idOpticalSheet

    def setCourseIndex(self, courseIndex):
        """
         Set the courseIndex of this relation, it should only be used if the OpticalSheet
         is not coded.

        @param int courseIndex : The position (column) where this offer is in the opticalSheet, more than one OpticalSheetColumn have the same courseIndex.
        @return  :
        @author
        """
        if not isinstance(courseIndex,(int,long)):
            raise OpticalSheetColumnError('courseIndex must be and int or long')
        self.courseIndex = courseIndex

    @staticmethod
    def pickById(idOpticalSheetColumn):
        """
         Returns one complete OpticalSheetColumn object where its ID is equal to the
         chosen.

        @param int idOpticalSheetColumn : Associated database key.
        @return OpticalSheetColumn :
        @author
        """
        cursor = MySQLConnection()
        opticalSheetColumnData = cursor.execute('SELECT idOpticalSheetColumn, idOpticalSheet, idOffer, code, courseIndex FROM rel_offer_opticalSheet WHERE idOpticalSheetColumn = ' + str(idOpticalSheetColumn))[0]
        opticalSheetColumn = OpticalSheetColumn(Offer.pickById(opticalSheetColumnData[2]))
        opticalSheetColumn.setIdOpticalSheet(opticalSheetColumnData[1])
        opticalSheetColumn.idOpticalSheetColumn = opticalSheetColumnData[0]
        if opticalSheetColumnData[3] != None:
            opticalSheetColumn.setCode(opticalSheetColumnData[3])
        elif opticalSheetColumnData[4] != None:
            opticalSheetColumn.setCourseIndex(opticalSheetColumnData[4])
        return opticalSheetColumn
    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idOpticalSheet
         > idOpticalSheetColumn
         > offer
         > code
         >courseIndex
         
         E. g. OpticalSheetColumn.find(idOpticalSheet = 314, offer = Offer, code = 21)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """

        cursor = MySQLConnection()
        parameters = {}
        for key in kwargs:
            if key == "offer":
                parameters['idOffer'] = kwargs['offer'].idOffer
            else:
                parameters[key] = kwargs[key]
        oscsData = cursor.find('SELECT idOpticalSheetColumn, idOpticalSheet, idOffer, code, courseIndex FROM rel_offer_opticalSheet', parameters)
        oscs = []
        for oscData in oscsData:
            osc = OpticalSheetColumn(Offer.pickById(oscData[2]))
            osc.setIdOpticalSheet(oscData[1])
            osc.idOpticalSheetColumn = oscData[0]
            if oscData[3] != None:
                osc.setCode(oscData[3])
            elif oscData[4] != None:
                osc.setCourseIndex(oscData[4])
            oscs.append(osc)
        return oscs

    def store(self):
        """
         Stores the information in the database only if either code or courseIndex is not
         None.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        if self.idOpticalSheet == None:
            raise OpticalSheetColumnError("idOpticalSheet is not defined")    
        if self.code == None and self.courseIndex == None:
            raise OpticalSheetColumnError("code or courseIndex must be defined")
        if self.code != None and self.courseIndex != None:
            raise OpticalSheetColumnError("code or courseIndex must be undefined")

        if self.code == None:
            mySQLCode = 'NULL'  #in MySQL is NULL
        else:
            mySQLCode = self.code
        if self.courseIndex == None:
            mySQLCourseIndex = 'NULL'
        else:
            mySQLCourseIndex = self.courseIndex
        if self.idOpticalSheetColumn == None:
            opticalSheetColumns = self.find(offer = self.offer, idOpticalSheet = self.idOpticalSheet, code = self.code, courseIndex = self.courseIndex)
            if len(opticalSheetColumns) > 0:
                self.idOpticalSheetColumn = opticalSheetColumns[0].idOpticalSheetColumn #Any osc that fit those paramaters is the same as this osc
                return
            else: 
                #Create this osc
                query = 'INSERT INTO rel_offer_opticalSheet (idOffer, idOpticalSheet, code, courseIndex) VALUES(' + str(self.offer.idOffer) + ', ' + str(self.idOpticalSheet) + ', ' + str(mySQLCode) + ', ' + str(mySQLCourseIndex) + ')'
                cursor.execute(query)
                cursor.commit()
                self.idOpticalSheetColumn = self.find(offer = self.offer, idOpticalSheet = self.idOpticalSheet, code = self.code, courseIndex = self.courseIndex)[0].idOpticalSheetColumn
        else:
            #Update opticalSheetColumn
            query = 'UPDATE rel_offer_opticalSheet SET idOffer = ' + str(self.offer.idOffer) + ', idOpticalSheet = ' + str(self.idOpticalSheet) + ', code = ' + str(mySQLCode) + ', courseIndex = ' + str(mySQLCourseIndex) + ' WHERE idOpticalSheetColumn = ' + str(self.idOpticalSheetColumn)
            cursor.execute(query)
            cursor.commit() 


    def delete(self):
        """
         Deletes the information in the database.

        @return  :
        @author
        """
        if self.idOpticalSheetColumn != None:
            cursor = MySQLConnection()
            if self == OpticalSheetColumn.pickById(self.idOpticalSheetColumn):
                cursor.execute('DELETE FROM rel_offer_opticalSheet WHERE idOpticalSheetColumn = ' + str(self.idOpticalSheetColumn))
                cursor.commit()
            else:
                raise OpticalSheetColumnError("Can't delete non saved object.")
        else:
            raise OpticalSheetColumnError('No idOpticalSheetColumn defined.')




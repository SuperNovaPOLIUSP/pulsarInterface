from pulsarInterface.Question import *

class AnswerError(Exception):
    """
     Exception reporting an error in the execution of an Answer method.

    :version:
    :author:
    """
    pass


class Answer(object):

    """
     Class representing an answer to a question related to a course.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idAnswer  (public)

     Question to which the answer has been given.

    question  (public)

     Associated database key of the related datafile.

    idDatafile  (public)

     The alternative corresponding to a multiple choice question answer. Its values
     must be:
     'A', 'B', 'C', 'D', 'E' or 'X'.

    alternative  (public)

     Identification of an optical sheet, relating it to a line of a datafile.

    identifier  (public)

     The position (column) in the optical sheet.

    courseIndex  (public)

     Represents the code refering to the offer of a course OR a class number in case
     of a non-encoded optical sheet.

    code  (public)

    """

    def __init__(self, question, alternative, identifier):
        """
        @param Question question : Question to which the answer has been given.
        @param char alternative : The alternative corresponding to a multiple choice question answer. Its values must be:
'A', 'B', 'C', 'D', 'E' or 'X'.
        @param int identifier : Identification of an optical sheet, relating it to a line of a datafile.
        @return  :
        @author
        """
        validAlternatives = ['A', 'B', 'C', 'D', 'E', 'X']
        if not question or not isinstance(question, Question):
            raise AnswerError('Must provide a valid question')
        if not alternative or not isinstance(alternative, (str, unicode)) or alternative not in validAlternatives:
            raise AnswerError('Must provide a valid alternative')
        if not identifier or not isinstance(identifier, (int, long)):
            raise AnswerError('Must provide a valid identifier')
        self.question = question
        self.alternative = alternative
        self.identifier = identifier
        self.idAnswer = None
        self.idDatafile = None
        self.courseIndex = None
        self.code = None

    def setIdDatafile(self, idDatafile):
        """
         Sets the datafile from which the answer comes from through its idDatafile. It
         should only be used by the Datafile class in order to register its answers.

        @param int idDatafile : Associated database key of the related datafile.
        @return  :
        @author
        """
        if not idDatafile or not isinstance(idDatafile, (int, long)):
            raise AnswerError('Must provide a valid idDatafile')
        self.idDatafile = idDatafile

    def setCode(self):
        """
         Set the code for the course assessed, it should only be used if the OpticalSheet
         is coded.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = 'select code from answer a, rel_answer_opticalSheetField_survey ra, aggr_opticalSheetField ao where a.idAnswer = ra.idAnswer and ra.idOpticalSheetField = ao.idOpticalSheetField and a.idAnswer = ' + str(self.idAnswer)
        codeData = cursor.execute(query)
        if codeData:
            self.code = codeData[0][0]
        else:
            raise AnswerError("Couldn't find a code to this Answer")

    def setCourseIndex(self):
        """
         Set the courseIndex for the course assessed, it should only be used if the
         OpticalSheet is not coded.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = 'select courseIndex from answer a, rel_answer_opticalSheetField_survey ra, aggr_opticalSheetField ao where a.idAnswer = ra.idAnswer and ra.idOpticalSheetField = ao.idOpticalSheetField and a.idAnswer = ' + str(self.idAnswer)
        indexData = cursor.execute(query)
        if indexData:
            self.curseIndex = indexData[0][0]
        else:
            raise AnswerError("Couldn't find a course index to this Answer")
        
    @staticmethod
    def countAnswers(**kwargs):
        """
         Searches the database and counts the ocurrences of answers matching the
         description specified through the method's parameters.
         
         Returns:
         A dictionary in the format {'A' : 13, 'B' : '27', 'C' : 30, 'D' : 48, 'E' : 5,
         'X' : 62}, which displays the number of answers counted according to the
         alternative.
         
         The parameters admitted to specify the description of the answers to be counted
         are the following:
         > question
         > timePeriod
         > cycle
         > course
         > offer_byClass
         > offer_byProfessor
         
         E. g. Answer.countAnswers(question = questionObject, timePeriod =
         timePeriodObject, course = courseObject)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return {} :
        @author
        """
        cursor = MySQLConnection()
        query = 'select a.alternative, count(a.alternative) from answer a'
        queryComplement = ' where '
        linkComplements = set([])
        complements = set([])
        offerBranchFlag = False
        linkOffer = 'aggr_offer o'
        joinOpticalSheetOpticalSheetField = 'os.idOpticalSheet = osf.idOpticalSheet'
        joinOfferOpticalSheet = 'rco.idOpticalSheet = os.idOpticalSheet'
        joinOfferOpticalSheetField = 'o.idOffer = osf.idOffer'
        joinOpticalSheetFieldRel = 'osf.idOpticalSheetField = r.idOpticalSheetField'
        joinRelAnswer = 'r.idAnswer = a.idAnswer'
        if 'question' in kwargs:
            linkComplements.add('question q')
            complements.add(' a.idQuestion = q.idQuestion and q.idQuestion = ' + str(kwargs['question'].idQuestion))
        if 'timePeriod' in kwargs:
            linkComplements.add('timePeriod tp')
            linkComplements.add(linkOffer)
            complements.add(' tp.idTimePeriod = o.idTimePeriod and tp.idTimePeriod = ' + str(kwargs['timePeriod'].idTimePeriod))
            offerBranchFlag = True
        if 'cycle' in kwargs:
            linkComplements.add('cycle c')
            linkComplements.add('rel_cycle_opticalSheet rco')
            linkComplements.add('opticalSheet os')
            linkComplements.add('rel_answer_opticalSheetField_survey r')
            linkComplements.add('aggr_opticalSheetField osf')
            complements.add(' c.idCycle = rco.idCycle and c.idCycle = ' + str(kwargs['cycle'].idCycle))
            complements.add(joinOfferOpticalSheet)
            complements.add(joinOpticalSheetOpticalSheetField)
            complements.add(joinOpticalSheetFieldRel)
            complements.add(joinRelAnswer)
        if 'course' in kwargs:
            linkComplements.add('course co')
            linkComplements.add(linkOffer)
            complements.add(' co.idCourse = o.idCourse and co.idCourse = ' + str(kwargs['course'].idCourse))
            offerBranchFlag = True
        if 'offer_byClass' in kwargs:
            linkComplements.add(linkOffer)
            complements.add(' o.classNumber = ' + str(kwargs['offer_byClass']))
            offerBranchFlag = True
        if 'offer_byProfessor' in kwargs:
            linkComplements.add(linkOffer)
            complements.add(' o.idProfessor = ' + str(kwargs['offer_byProfessor']))
            offerBranchFlag = True
        if offerBranchFlag:
            linkComplements.add('aggr_opticalSheetField osf')
            linkComplements.add('rel_answer_opticalSheetField_survey r')
            complements.add(joinOfferOpticalSheetField)
            complements.add(joinOpticalSheetFieldRel)
            complements.add(joinRelAnswer)
        for linkComplement in linkComplements:
            query += ', '
            query += linkComplement
        for complement in complements:
            queryComplement += complement
            queryComplement += ' and '
        queryComplement = queryComplement[:-5]
        query += queryComplement + ' group by a.alternative'
        print query
        answers = {}
        searchData = cursor.execute(query)
        if searchData:
            for data in searchData:
                answers[data[0]] = data[1]
        return answers

    @staticmethod
    def pickById(idAnswer):
        """
         Returns one complete Answer object where its ID is equal to the chosen.

        @param int idAnswer : Associated database key.
        @return Answer :
        @author
        """
        cursor = MySQLConnection()
        query = 'select idQuestion, idDatafile, alternative, identifier from answer where idAnswer = ' + str(idAnswer)
        searchData = cursor.execute(query)
        if searchData:
            question = Question.pickById(searchData[0][0])
            idDatafile = searchData[0][1]
            alternative = searchData[0][2]
            identifier = searchData[0][3]
            answer = Answer(question, alternative, identifier)
            answer.idAnswer = idAnswer
            answer.setIdDatafile(idDatafile)
            answer.setCode()
            answer.setCourseIndex()
            return answer
        raise AnswerError('Answer not found')

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
         > idAnswer
         > question
         > idDataFile
         > alternative
         > identifier
         
         E. g. Answer.find(question = questionObject, identifier = 21, idDataFile = 413)

        @param {} **kwargs : Dictionary of arguments to be used as parameters for the search.
        @return Answer[] :
        @author
        """
        cursor = MySQLConnection()
        answers = []
        if 'question' in kwargs:
            kwargs['idQuestion'] = kwargs['question'].idQuestion
            del(kwargs['question'])
        if 'alternative' in kwargs:
            alt = kwargs['alternative']
            del(kwargs['alternative'])
            kwargs['alternative_equal'] = alt
        query = 'select idAnswer, idQuestion, idDatafile, alternative, identifier from answer '
        searchData = cursor.find(query, kwargs)
        if searchData:
            for answerData in searchData:
                question = Question.pickById(answerData[1])
                alternative = answerData[3]
                identifier = answerData[4]
                idDatafile = answerData[2]
                answer = Answer(question, alternative, identifier)
                answer.idAnswer = answerData[0]
                answer.setIdDatafile(idDatafile)
                answer.setCode()
                answer.setCourseIndex()
                answers.append(answer)
        return answers

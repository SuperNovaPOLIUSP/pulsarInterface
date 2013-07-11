# -*- coding: utf8 -*-
from AnswerType import *
from tools.MySQLConnection import MySQLConnection

class QuestionError(Exception):
    """
     Exception that reports errors during the execution of Question class methods
  
    :version:
    :author:
    """
    pass

class Question(object):

    """
     Class that represents a question used in an assessment.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.

    idQuestion  (public)

     Question's written statement.

    questionWording  (public)

     The type of the question, that relates it to five possible choice answers.

    answerType  (public)

    """

    def __init__(self, questionWording, answerType):
        """
         Constructor method.

        @param string questionWording : The question's written questionWording.
        @param AnswerType answerType : The type of the question, that relates it to five possible choice answers.
        @return  :
        @author
        """
	#Parameter verification
	if not isinstance(answerType,AnswerType) or not AnswerType.pickById(answerType.idAnswerType) == answerType:
	    raise QuestionError('Parameter answerType must be a AnswerType object that exists in the database.')
	#Setting parameters that have set function
        self.setQuestionWording(questionWording)
	#Setting other parameters
        self.answerType = answerType
	#Setting None parameters
        self.idQuestion = None
        
    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class Question are
         equal.

        @param Question other : Other object of the class Question to be compared with a present object.
        @return bool :
        @author
        """
        if not isinstance(other, Question):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         not equal.

        @param Question other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    @staticmethod
    def pickById(idQuestion):
        """
         Returns a Question object specified by its database ID.

        @param int idQuestion : Database ID.
        @return Question :
        @author
        """
        #Checked, is OK        
        cursor = MySQLConnection()
        try:
            questionData = cursor.execute("""SELECT idQuestion, questionWording, idAnswerType FROM question WHERE idQuestion = """ + str(idQuestion))[0]
        except:
            return None
        question = Question(questionData[1], AnswerType.pickById(questionData[2]))
        question.idQuestion = questionData[0]
        return question

    def setQuestionWording(self, newQuestionWording):
        """
         Changes the question questionWording.

        @param string questionWording : New questionWording for the question.
        @return  :
        @author
        """
        #Checked, is OK
        if not isinstance(newQuestionWording,(unicode,str)):
            raise QuestionError('Parameter newQuestionWording must be unicode or string.')
        self.questionWording = newQuestionWording

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator).
         
         Returns:
         All the objects that are related to existing questions in the database, if there
         are not any parameters passed.
         
         A list of objects that match the specifications made by one (or more) of the
         folowing parameters:
         > idQuestion
         > questionWording_equal or questionWording_like
         > category_equal or category_like
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Question.find(questionWording_like = "How many", category_equal = "Hour")

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        questionsData = cursor.find("""SELECT idQuestion, questionWording, idAnswerType FROM question""",kwargs)
        questions = []
        for questionData in questionsData:
            question = Question(questionData[1], AnswerType.pickById(questionData[2]))
            question.idQuestion = questionData[0]
            questions.append(question)
        return questions

    def store(self):
        """
         Adds object to database if it does not exist on the table or changes it if it
         does.

        @return  :
        @author
        """
        cursor = MySQLConnection()
        #Question already exists in database?
        if self.idQuestion:
            #Yes, the question exists
            #We will update its data
            query = """UPDATE question SET idAnswerType = """ +str(self.idAnswerType) +""", questionWording = '""" +self.questionWording + """'"""
            query += """ WHERE idQuestion = """ +str(self.idQuestion)
        else:
            #No, the question does not exist
            #Is there one just like it?
            possibleQuestions = Question.find(questionWording_equal = self.questionWording, answerType = self.answerType)
            if len(possibleQuestions) > 0:
                #There's one just like it!
                self.idQuestion = possibleQuestions[0].idQuestion
                return None
	    else:
                #No, let's create it
                query = "INSERT INTO question (idAnswerType, questionWording) VALUES ( "
                query += str(self.answerType.idAnswerType) + ",'" + str(self.questionWording) + "')"
        #Execute query
        cursor.execute(query)
        cursor.commit()
        return None

    def delete(self):
        """
         Deletes a question from the database.

        @return  :
        @author
        """
        
        if self.idQuestion != None:
            cursor = MySQLConnection()
            if self == Curriculum.pickById(self.idQuestion):
                cursor.execute("""DELETE FROM question WHERE idQuestion = """ + str(self.idQuestion))
                cursor.execute("""DELETE FROM rel_question_questionnaire WHERE idQuestion = """ + str(self.idQuestion))
                cursor.commit()
            else:
                raise QuestionError("Can't delete non saved question.")
        else:
            raise QuestionError('idQuestion not defined.')




#coding: utf8
#from AnswerType import *
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
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Question's written statement
     
     o enunciado da pergunta

    statement  (private)

     

    idQuestion  (private)

     

    answerType  (private)

    """

    def __init__(self, statement, answerType):
        """
         

        @param string statement : 
        @param AnswerType answerType : 
        @return  :
        @author
        """
        if not isinstance(statement, (str, unicode)):
            raise QuestionError("'statement' must be a string or unicode type")
        if not isinstance(answerType, (str, unicode)):
            raise QuestionError("'statement' must be a string or unicode type")
        self.statement = statement
        self.answerType = answerType
        self.idQuestion = None
        
    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class Question are
         equal.

        @param AnswerType other : Other object of the class Question to be compared with a present object.
        @return bool :
        @author
        """
        if not isinstance(other, Question):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class Question are
         not equal.

        @param AnswerType other : Other object of the class Question to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    @staticmethod
    def pickById(idQuestion):
        """
         returns a Question object once given an idQuestion
         
         retorna um objeto Pergunta a partir do idPergunta

        @param int idQuestion : 
        @return Question :
        @author
        """
        #Checked, is OK        
        cursor = MySQLConnection()
        questionData = cursor.execute("""SELECT idQuestion, questionWording, idAnswerType FROM question WHERE idQuestion = """ + str(idQuestion))[0]
        question = Question(questionData[1], AnswerType.pickById(questionData[2]))
        question.idQuestion = questionData[0]
        return question

    def setStatement(self, newStatement):
        """
         

        @param string newStatement : novo enunciado para a pergunta
        @return  :
        @author
        """
        #Checked, is OK   
        if not isinstance(newStatement, (str, unicode)):
            raise QuestionError("'statement' must be a string or unicode type")
        self.statement = newStatement
        return

    @staticmethod
    def find(**kwargs):
        """
         Searches the database to find one or more objects that fit the description
         specified by the method's parameters. It is possible to perform two kinds of
         search when passing a string as a parameter: a search for the exact string
         (EQUAL operator) and a search for at least part of the string (LIKE operator). 

        Returns:
        All the objects that are related to existing offers in the database, if there
        are not any parameters passed.

        A list of objects that match the specifications made by one (or more) of the
        folowing parameters:
        > idQuestion
        > statement_equal or statement_like
        > category_equal or category_like
        The parameters must be identified by their names when the method is called, and
        those which are strings must be followed by "_like" or by "_equal", in order to
        determine the kind of search to be done.
        E. g. Question.find(statement_like = "How many", category_equal = "Hour")
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
         adds object to database if it does not exist on the table or changes it if it
         does. Returns "true" if object is stored and "false" if it isn't.
         
         insere no banco caso o objeto não exista na tabela ou altera, caso contrário.
         Retorna true caso o objeto tenha sido armazenado ou false, caso contrário

        @return bool :
        @author
        """
        cursor = MySQLConnection()
        #Question already exists in database?
        if self.idQuestion:
            #Yes, the question exists
            #We will update its data
            query = """UPDATE question SET idAnswerType = """ +str(self.answerType.idAnswerType) +""", questionWording = '""" +self.statement + """'"""
            query += """ WHERE idQuestion = """ +str(self.idQuestion)
            #Doesn't save changes in AnswerType parameter
        else:
            #No, the question does not exist
            #Is there one just like it?
            possibleQuestions = Question.find(statement_equal = self.statement, category_equal = self.answerType.name)
            if len(possibleQuestions) > 0:
                #There's one just like it!
                self.idQuestion = possibleQuestions[0].idQuestion
                return
                #No, let's create it
                query = """INSERT INTO question (idAnswerType, questionWording) VALUES ("""
                query += str(self.answerType.idAnswerType), """'"""+self.statement+"""')"""
        #Execute query
        cursor.execute(query)
        cursor.commit()
        return
        

    def remove(self):
        """
         removes object from database. Returns "true" if succeeds
         
         remove o objeto do banco de dados e retorna True se conseguir, caso contrario
         retorna False

        @return bool :
        @author
        """
        
        if self.idQuestion != None:
            cursor = MySQLConnection()
            if self == Question.pickById(self.idQuestion):
                cursor.execute("""DELETE FROM question WHERE idQuestion = """ + str(self.idQuestion))
                cursor.execute("""DELETE FROM rel_question_questionnaire WHERE idQuestion = """ + str(self.idQuestion))
                cursor.commit()
            else:
                raise QuestionError("Can't delete non saved object.")
        else:
            raise QuestionError('idQuestion not defined.')




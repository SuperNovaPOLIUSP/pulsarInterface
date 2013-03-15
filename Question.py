from AnswerType import *

class Question(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

     Question's written statement
     
     o enunciado da pergunta

    statement  (public)

     

    idQuestion  (public)

     

    answerType  (public)

    """

    def __init__(self, statement, answerType):
        """
         

        @param string statement : 
        @param AnswerType answerType : 
        @return  :
        @author
        """
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
        cursor = MySQLConnection()
        try:
            questionData = cursor.execute('SELECT idQuestion, questionWording, idAnswerType FROM question WHERE idQuestion = ' + str(idQuestion))[0]
        except:
            return None
        question = Question(questionData[1], questionData[2])
        question.idQuestion = questionData[0]
        return question

    def setStatement(self, newStatement):
        """
         

        @param string newStatement : novo enunciado para a pergunta
        @return  :
        @author
        """
        if not isinstance(newStatement, str):
            return False
        self.statement = newStatement

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
        questionsData = cursor.find('SELECT idQuestion, questionWording, idAnswerType FROM question',kwargs)
        questions = []
        for questionData in questionsData:
            question = Question(questionData[1], questionData[2])
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
        if self.idQuestion == None:
            possibleIds = self.find(statement_equal = self.statement,  category_equal = self.category)
            if len(possibleIds) > 0:
                self.idQuestion = possibleIds[0].idQuestion
                return
            else:
                #Create this question.
                #Getting idAnswerType
                idAnswerType_sql = cursor.execute('SELECT idAnswerType FROM answerType WHERE name = ' + self.category
                if len(idAnswerType) = 0
                    raise Error('AnswerType not found')
                query = 'INSERT INTO question (questionWording, idAnswerType) VALUES ' + str((self.statement, idAnswerType_sql[0]))
                cursor.execute(query)
                cursor.commit()
                self.idQuestion = self.find(statement_equal = self.statement,  category_equal = self.category)[0].idQuestion
        else:
            #Update timePeriod.
            idAnswerType_sql = cursor.execute('SELECT idAnswerType FROM answerType WHERE name = ' + self.category
            if len(idAnswerType) = 0
                raise Error('AnswerType not found')
            query = "UPDATE question SET questionWording = " +str(self.statement) +", idAnswerType = " +str(idAnswerType_sql[0]) +" WHERE idQuestion = " +str(self.idQuestion)
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
        pass




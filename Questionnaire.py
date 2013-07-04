from Question import *
import time
from date import *

class Questionnaire(object):

    """
     Class representing a set of questions in an assessment.

    :version:
    :author:
    """

    """ ATTRIBUTES

     Associated database key.
    idQuestionnaire  (private)

     Dictionary of Question objects, in which each key is the question's index in the
     questionnaire and the value is a Question object.
    questions  (private)

     Indicates who or what the questionnaire refers to (usually to a curriculum's
     term).
    description  (private)

     Date on which the questionnaire was created.
    creationDate  (private)

     Number that indicates which assessment the questionnaire refers to.
    assessmentNumber  (private)
    """

    def __init__(self, questionDictionary, description, assessmentNumber):
        """
         Constructor method. When creating a questionary, this method sets its date to
         the the same as the date of the object's creation.

        @param Question{} questionDictionary : Dictionary of Questions objects, in which each key is the question's index in the questionnaire and the value is a Question object.
        @param string description : Indicates who or what the questionnaire refers to (usually to a curriculum's term).
        @param int assessmentNumber : Number that indicates which assessment the questionnaire refers to.
        @return Questionnaire :
        @author
        """
        if not isEmpty questionDictionary:
            for index in questionDictionary:
                if not isinstance(questionDictionary[index], Question):
                    raise QuestionnaireError('One or more of the entries in questionDictionary is not a question')
        self.questions = questionDictionary
        self.description = description
        self.creationDate = date.today().isoformat()
        self.assessmentNumber = assessmentNumber

    def __iter__(self):
        """
         Iterator that returns each question of the questionnaire's questions attribute.
        @return Question :
        @author
        """
        pass

    def __eq__(self, other):
        """
         Comparison method that returns True if two objects of the class Questionnaire
         are equal.
        @param Questionnaire other : Other object of the class Questionnaire to be compared with a present object.
        @author
        """
        if not isinstance(other, Questionnaire):
            return False
        return self.__dict__ == other.__dict__


    def __ne__(self, other):
        """
         Comparison method that returns True if two objects of the class AnswerType are
         not equal.

        @param Questionnaire other : Other object of the class AnswerType to be compared with a present object.
        @return bool :
        @author
        """
        return not self.__eq__(other)

    def addQuestion(self, question, index):
        """
         Adds a question to the questionnaire's dictionary of questions at the position
         specified by the index parameter. Returns a boolean that confirms if the
         question was successfully added.
        @param Question question : A Question object to be added to the dictionay of questions in the questionnaire.
        @param int index : The index of the question to be inserted in the questionnaire.
        @return bool :
        @author
        """
        try:
            all_keys = self.questions.keys()
            if index in all_keys:
                return false #Adding a second question to the same index
            self.questions[index] = question
            return True
        except:
            return False

    def removeQuestionByIndex(self, index):
        """
         Removes a question, specified by its index, from the questions attribute.
         Returns a boolean that confirms if the question was successfully removed.
        @param int index : Question's index in the questionnaire.
        @return bool :
        @author
        """
        try:
            all_keys = self.questions.keys()
            if index not in all_keys:
                return false #Key not in dict
            del self.questions[index]
            return True
        except:
            return False

    def removeQuestionById(self, idQuestion):
        """
         Removes a question, specified by its database ID, from the questions attribute.
         Returns a boolean that confirms if the question was successfully removed.
        @param int idQuestion : Database ID of the question to be removed from the questionnaire.
        @return bool :
        @author
        """
        question = Question.pickById(idQuestion)
        associations = self.questions.items()
        try:
            for association in associations:
                if association[1] == question:
                    self.removeQuestionByIndex(association[0])
            return True
        except:
            return False

    @staticmethod
    def buildQuestionsQuestionnaire(self, idOffer):
        """
         Method that returns a list with all the questions from questionnaires that refer to a specific offer.
        @param int idOffer : Database ID of the discipline's offer.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = 'select idQuestionnaire from questionnaire q, 
            rel_opticalSheet_questionnaire roq, 
            rel_offer_opticalSheet roo, 
            aggr_offer o 
        where q.idQuestionnaire = roq.idQuestionnaire
            and roq.idOpticalSheet = roo.idOpticalSheet
            and roo.idOffer = o.idOffer
            and o.idOffer = ' + str(idOffer)
        questionnaire_list = []
        question_list = []
        try:
            results = cursor.execute(query)
            for result in results:
                questionnaire_list.append(Questionnaire.pickById(result[0]))
            for questionnaire in questionnaire_list
                question_list.extend(questionnaire.questions)
            return question_list
        except:
            raise QuestionnaireError('Error joining offer with optical ')

    @staticmethod
    def getQuestionsById(self, idQuestionnaire):
        """
            Returns a dictionary containing the questions related to a questionnaire's
            id passed as argument

            @param int idQuestionnaire : Database ID of the questionnaire
        """
        cursor = MySqlConnection()
        questions = {}
        query_questions = 'select idQuestion, questionIndex from rel_question_questionnaire where idQuestionnnaire = ' + str(idQuestionnnaire)
        try:
            search_for_questions = cursor.execute(query_questions)
            for question_data in search_for_questions:
                questions{question_data[question_data[1]] = Question.pickById(question_data[0])}
            return questions
        except:
            raise QuestionnaireError('Error on linking questionnaire to questions')

    @staticmethod
    def pickById(self, idQuestionnaire):
        """
         Returns a Questionnaire object specified by its database ID.

        @param int idQuestionnaire : Database ID of the questionnaire to be found.
        @return Questionnaire :
        @author
        """
        cursor = MySQLConnection()
        query = 'select description, creationDate from questionnaire where idQuestionnaire = ' + str(idQuestionnaire)
        try:
            result = cursor.execute(query)
            return Questionnaire(questions, result[0][0], result[0][1])
        except:
            raise QuestionnaireError('Error on creating new Questionnnaire object')
            

    @staticmethod
    def find(self, _kwargs):
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
         > idQuestionnaire
         > description_equal or description_like
         > creationDate_equal or creationDate_like
         > assessmentNumber
         The parameters must be identified by their names when the method is called, and
         those which are strings must be followed by "_like" or by "_equal", in order to
         determine the kind of search to be done.
         E. g. Questionnaire.find(description_like = "3rdYear", creationDate_equal =
         "2013-01-01", assessmentNumber = 1)

        @param {} _kwargs : Dictionary of arguments to be used as parameters for the search.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        query = 'select * from questionnaire '
        questionnaire_list = []
        try:
            results = cursor.find(query, _kwargs)
            for data in results:
                questionnaire = Questionnaire(getQuestions(data[0]), data[1], data[2].isoformat())
                questionnaire_list.append(questionnaire)
            return questionnaire_list
        except:
            raise QuestionnaireError('Error searching for a questionnaire')

    def store(self):
        """
         Stores the data of the Questionnaire object on the database.
        @return  :
        @author
        """
        cursor = MySQLConnection()
        main_query = 'insert into questionnaire values ('
        rel_query = 'insert into rel_question_questionnaire values (' + self.idQuestionnaire + ', '
        main_query += self.description + ', ' + self.creationDate + ')'
        try: 
            cursor.execute(main_query)
        except:
            raise QuestionnaireError('Error trying to insert a new questionnaire')
        try:
            for question_index in self.questions:
                rel_query_to_execute = rel_query + str(self.questions[question_index]) + ', ' + str(question_index) + ')'
                cursor.execute(rel_query_to_execute)
        except:
            raise QuestionnaireError('Error trying to add questionnaire-question relation')

    def delete(self):
        """
         Deletes the data of the Questionnaire object on the database.
        @return  :
        @author
        """
        cursor = MySQLConnection
        query = 'delete from questionnaire where idQuestionnaire = ' + str(self.idQuestionnaire)
        query_rel = 'delete from rel_question_questionnaire where idQuestionnaire = ' + str(self.idQuestionnaire)
        cursor.execute(query)
        cursor.execute(query_rel)

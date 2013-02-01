# coding: utf8#
from ae2012.models import *
from django.core.files import File

class AnswerType(object):

  """
   

  :version:
  :author:
  """

  """ ATTRIBUTES

   

  idAnswerType  (public)

   A dictionary containing the meaning of the answers alternatives in the form {
   'A':'meaningA' , 'B':'meaningB' , ...}
   
   um dicionario contendo os significados das alternativas na forma: {
   'A':'significadoA' , 'B':'significadoB' , ...}

  meaning  (public)

   answerType category
   
   categoria do tipoResposta

  category  (public)

  """

  def __init__(self, name, meaning):
    """
     name and meaning are the necessary data to create an AnswerType

    @param string name : nome do tipoResposta
    @param string{} meaning : um dicionario contendo os significados das alternativas na forma: { 'A':'significadoA' , 'B':'significadoB' , ...}
    @return  :
    @author
    """
    self.name = name
    self.meaning = meaning

  def pickById(self, idAnswerType):
    """
     returns an AnswerType object given an idAnswerType
     

    @param int idAnswerType : 
    @return AnswerType :
    @author
    """
    targetMeanings = multiDominio.objects.filter(idTipoResposta = idAnswerType ).values('alternativas','significado')
    meaning = {}
    for targetMeaning in targetMeanings:
        meaning[targetMeaning['alternativas']] = targetMeaning['significado']
    #print meaning
    name = tipoDeResposta.objects.filter(id = idAnswerType).values('catResposta')[0]['catResposta']
    #print name
    answerType = AnswerType(name,meaning)
    return answerType

  def pickByCategory(self, category):
    """
     returns an AnswerType object once given a category

    @param string category : 
    @return AnswerType :
    @author
    """
    name = category
    targetIdAnswerType = tipoDeResposta.objects.filter(catResposta = category).values('id')
    idAnswerType = targetIdAnswerType[0]['id']
    #print idAnswerType
    targetMeanings = multiDominio.objects.filter(idTipoResposta = targetIdAnswerType ).values('alternativas','significado')
    meaning = {}
    for targetMeaning in targetMeanings:
        meaning[targetMeaning['alternativas']] = targetMeaning['significado']
    #print meaning
    answerType = AnswerType(name,meaning)
    return answerType

  def store(self):
    """
     changes object on table or adds it to database if object is absent. Returns true
     if object is stored and false if it fails.
     
     insere no banco caso o objeto não exista na tabela ou altera, caso contrário.
     Retorna true caso o objeto tenha sido armazenado ou false, caso contrário

    @return  :
    @author
    """
    pass




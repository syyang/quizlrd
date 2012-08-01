struct Question {
  1: string question,
  2: string answer
}

service QuestionStore {
  list<Question> getQuestions(),
  void addQuestion(1:Question question)
}
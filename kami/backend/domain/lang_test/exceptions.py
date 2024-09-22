class LangTestNotFound(Exception):
    """Error when language test not found"""


class NoCurrentQuestionError(Exception):
    """Error when current question not found"""


class NoQuestionsError(Exception):
    """Error when no questions"""


class NoRepliesError(Exception):
    """Error when no replies"""


class LangTastCreationFailedError(Exception):
    """Error when trying create language test by ChatGPT"""

from crewai.tools import tool


# docstring과 인자의 이름, type을 제대로 작성해야 CrewAI가 함수에 대한 schema를 정확히 생성할 수 있다.
@tool
def count_letters(sentence: str) -> int:
    """
    This function is to count the amount of letters in a sentence.
    The input is a 'sentence' string.
    The output is a number
    """

    return len(sentence)

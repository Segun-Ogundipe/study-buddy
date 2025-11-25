from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from src.config.settings import settings
from src.llm.groq_client import get_groq_llm
from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template

class QuestionGenerator:
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)
        
    def _retry_and_parse(self, prompt: PromptTemplate, parser: PydanticOutputParser, topic: str, difficulty: str):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed = parser.parse(response.content)
                
                self.logger.info("Sucessfully parsed the question")
                
                return parsed
            except Exception as e:
                self.logger.error(f"Error generating and parsing the question: {e}")
                
                if attempt == settings.MAX_RETRIES-1:
                    raise CustomException(f"Question Generation failed after {settings.MAX_RETRIES} attempts", e)
                
    def generate_mcq(self, topic: str, difficulty: str="medium") -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self._retry_and_parse(mcq_prompt_template, parser, topic, difficulty)
            
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.logger.info("Generated a valid MCQ Question")
            
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {e}")
            raise CustomException("MCQ generation failed", e)
        
    def generate_fill_in_the_blank(self, topic: str, difficulty: str="medium") -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic, difficulty)
            
            if "___" not in question.question:
                raise ValueError(f"Fill in the blanks question should contain '_____'.\nBut istead got: {question.question}")
            
            self.logger.info("Generated a valid Fill in The Blanks Question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate fill question: {e}")
            raise CustomException("Fill in The Blanks generation failed", e)

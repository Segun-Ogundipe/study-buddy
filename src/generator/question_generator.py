from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from src.common.custom_exception import CustomException
from src.common.logger import get_logger
from src.llm.clients import get_groq_llm, get_openai_llm
from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template

class QuestionGenerator:
    def __init__(self, user_controls):
        self.user_controls = user_controls
        self.llm = get_groq_llm(user_controls) if user_controls["model_provider"] == "Groq" else get_openai_llm(user_controls)
        self.logger = get_logger(self.__class__.__name__)
        
    def _retry_and_parse(self, prompt: PromptTemplate, parser: PydanticOutputParser, topic: str, difficulty: str, questions: List[str]):
        for attempt in range(self.user_controls["num_retries"]):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")
                response = self.llm.invoke(
                    prompt.format(
                        model_name=self.user_controls["model_name"],
                        topic=topic,
                        difficulty=difficulty,
                        questions="\n-->".join(questions)
                    )
                )
                parsed = parser.parse(response.content)
                
                self.logger.info("Sucessfully parsed the question")
                
                return parsed
            except Exception as e:
                self.logger.error(f"Error generating and parsing the question: {e}")
                
                if attempt == self.user_controls["num_retries"]-1:
                    raise CustomException(f"Question Generation failed after {self.user_controls['num_retries']} attempts", e)
                
    def generate_mcq(self, topic: str, questions: List[str], difficulty: str="medium") -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self._retry_and_parse(mcq_prompt_template, parser, topic, difficulty, questions)
            
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.logger.info("Generated a valid MCQ Question")
            
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {e}")
            raise CustomException("MCQ generation failed", e)
        
    def generate_fill_in_the_blank(
        self,
        topic: str,
        questions: List[str],
        difficulty: str="medium"
    ) -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic, difficulty, questions)
            
            if "___" not in question.question:
                raise ValueError(f"Fill in the blanks question should contain '_____'.\nBut istead got: {question.question}")
            
            self.logger.info("Generated a valid Fill in The Blanks Question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate fill question: {e}")
            raise CustomException("Fill in The Blanks generation failed", e)

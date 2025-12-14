import os

from dotenv import load_dotenv
import streamlit as st
load_dotenv()

from src.config.ui_config import Config
from src.generator.question_generator import QuestionGenerator
from src.utils.helpers import *

ui_config = Config()

def main():
    st.set_page_config(page_title=f"{ui_config.get_page_title()}", page_icon="🎧🎧")
    
    if "model_provider" not in st.session_state:
        st.session_state.model_provider = ""
    
    if "model" not in st.session_state:
        st.session_state.model = ""
        
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
        
    if "model_name" not in st.session_state:
        st.session_state.model_name = ""
    
    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
        
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
        
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    
    st.title(f"GenAI {ui_config.get_page_title()}")
    
    with st.sidebar:
        with st.expander("Quiz Settings", icon="🏆", expanded=True):
        
            question_type = st.selectbox(
                "Select Question Type",
                ["Multiple Choice", "Fill in The Blank"],
                index=0,
                help="Select one of Multiple Choice questions or Fill in the Blank type questions"
            )
            
            topic = st.text_input(
                "Enter Topic",
                placeholder="African History, Geography...",
                help="Enter the topic the questions should be generated from"
            )
            
            difficulty = st.selectbox(
                "Difficulty Level",
                ["Easy", "Medium", "Hard"],
                index=1,
                help="Select level of difficulty"
            )
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Select low value for a more deterministic LLM"
            )
            
            num_questions = st.slider(
                "Number of Questions",
                min_value=1,
                max_value=10,
                value=5,
                help="Number of questions to be generated"
            )
            
            num_retries = st.slider(
                label="Number of Retries",
                min_value=1,
                max_value=5,
                value=3,
                help="How many times should the LLM try to generate a question after initial falure"
            )
            
            if st.button("Generate Quiz"):
                st.session_state.quiz_submitted = False
                
                generator = QuestionGenerator(
                    user_controls={
                        "model_provider": st.session_state.model_provider,
                        "model": st.session_state.model,
                        "api_key": st.session_state.api_key,
                        "temperature": temperature,
                        "model_name": st.session_state.model_name,
                        "num_retries": num_retries
                    }
                )
                success = st.session_state.quiz_manager.generate_questions(
                    generator,
                    topic,
                    "MCQ" if question_type == "Multiple Choice" else "FiTB",
                    difficulty,
                    num_questions
                )
                
                st.session_state.quiz_generated = success
    
        with st.expander("Model Configuration", icon="⚙️"):
            providers = ui_config.get_providers()
            openai_models = ui_config.get_openai_models()
            groq_models = ui_config.get_groq_models()
            
            st.session_state.model_provider = st.selectbox("Select Provider", providers)
            st.session_state.model_name = st.text_input("Model Name", value="Tidal")
            if st.session_state.model_provider == "Groq":
                st.session_state.model = st.selectbox("Select Groq Model", groq_models)
                st.session_state.api_key = st.text_input("Enter Groq API Key", type="password")
                if not st.session_state.api_key:
                    st.warning("⚠️ Groq API Key is required. Using key set in GROQ_API_KEY")
            elif st.session_state.model_provider == "OpenAI":
                st.session_state.model = st.selectbox("Select OpenAI Model", openai_models)
                st.session_state.api_key = st.text_input("Enter OpenAI API Key", type="password")
                if not st.session_state.api_key:
                    st.warning("⚠️ OpenAI API Key is required. Using key set in OPENAI_API_KEY")
    
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()
        
        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
        
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        
        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count/total_questions) * 100
            st.write(f"Score: {score_percentage}")
            
            for _, result in results_df.iterrows():
                question_num = result["question_number"]
                if result["is_correct"]:
                    st.success(f"✅ Question {question_num}: {result['question']}")
                else:
                    st.error(f"❌ Question {question_num}: {result['question']}")
                    st.write(f"Your answer: {result['user_answer']}")
                    st.write(f"Correct answer: {result['correct_answer']}")
                    
                st.markdown("-------")
                
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, "rb") as f:
                        st.download_button(
                            label="Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime="text/csv"
                        )
                else:
                    st.warning("No results available")

if __name__ == "__main__":
    main()

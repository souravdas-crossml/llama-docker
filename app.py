"""FastAPI endpoint for generating answers using Llama 2 model."""

# Import dependencies
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import CTransformers
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("llama")

# Define FastAPI application
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

# Define request body model
class InputText(BaseModel):
    """Request body model for input text."""
    text: str

# Initialize the language model
llm = CTransformers(
    model="model\llama-2-7b.Q2_K.gguf",
    model_type="llama",
    config={
        'max_new_tokens': 256,  # Set the maximum number of tokens here
        'temperature': 0.2
    }
)
 

# Define api endpoint to test connection
@app.get("/")
def test_connection() -> dict:
    """
    Test the connection to the FastAPI server.

    Raises:
        HTTPException: If there is an error during the connection test.

    Returns:
        dict: A dictionary indicating the success of the connection test.
    """
    try:
        return {"message": "Connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Define API endpoint
@app.post("/llama")
async def get_answer(input_text: InputText) -> dict:
    """
    Endpoint to generate an answer using Llama 2 model.

    Args:
        input_text (InputText): The input text provided in the request body.

    Returns:
        dict: A dictionary containing the generated answer.
    """
    try:
        start_time = time.time()
        # Log message
        _logger.info("Generating answer using Llama 2 model.")
        
        # Get text from request body
        text = input_text.text
        
        # Define a more concise prompt template
        template = f"Question: {text}\nAnswer: Let's think step by step."
        
        # Generate response using the language model
        answer = llm.invoke(template)
        
        # Log response
        _logger.info("Response from llama: %s" % answer)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        _logger.info("Time elapsed: %.3f seconds" % elapsed_time)
        
        # Return the answer in a dictionary
        return {"answer": answer}
    except Exception as e:
        # Raise an HTTPException if an error occurs
        raise HTTPException(status_code=500, detail=str(e))

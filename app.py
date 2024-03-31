# Import dependencies
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import CTransformers
import time

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger("llama")

# Define FastAPI application
app = FastAPI()

# Define request body model
class InputText(BaseModel):
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

# Define API endpoint
@app.post("/llama")
async def get_answer(input_text: InputText):
    try:
        start_time = time.time()
        _logger.info("Generating answer using Llama 2 model.")
        
        # Get text from request body
        text = input_text.text
        
        # Define a more concise prompt template
        template = f"Question: {text}\nAnswer: Let's think step by step."
        
        # Generate response using the language model
        answer = llm.invoke(template)
        
        _logger.info("Response from llama: %s" % answer)
        elapsed_time = time.time() - start_time
        _logger.info("Time elapsed: %.3f seconds" % elapsed_time)
        
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

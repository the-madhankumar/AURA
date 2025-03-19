import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.endpoints import Research 
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def root():
    logging.info("Root endpoint accessed")
    return {"message": "Autonomous Unified Research Assistant"}

@app.post("/research")
def research(prompt: Prompt):
    logging.info(f"Received research request: {prompt.prompt}")

    try:
        response_generator = Research(prompt.prompt)  # Stream response
        full_response = "".join(str(chunk) for chunk in response_generator)

        if not full_response.strip():
            logging.warning("Empty response received from Research function.")
            raise HTTPException(status_code=500, detail="No research data available")

        return {"response": full_response}

    except Exception as e:
        logging.error(f"Error in research function: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    logging.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120)

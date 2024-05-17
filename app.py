from flask import Flask ,request ,render_template
import os ,sys ,uvicorn
from fastapi import  FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from src.TextSummrization.config.configuration import ConfigurationManager
from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.pipeline.training_pipeline import Training_Pipeline
from src.TextSummrization.pipeline.prediction_pipeline import Prediction_Pipeline 


ROOT_DIR = os.getcwd()
SAVE_MODEL_DIR = 'export_dir'
SAVED_MODEL_DIR_PATH = os.path.join(ROOT_DIR ,SAVE_MODEL_DIR)



app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def training():
    try:
        training_pipeline =Training_Pipeline(
            config= ConfigurationManager()
        )
        training_pipeline.run_pipeline()
        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")
    
@app.post("/predict")
async def predict_route(text):
    try:

        obj = Prediction_Pipeline(export_dir=SAVED_MODEL_DIR_PATH)
        text = obj.prediction(text)
        return text
    except Exception as e:
        raise e

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501)
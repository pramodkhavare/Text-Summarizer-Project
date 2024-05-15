from src.TextSummrization.config.configuration import ConfigurationManager 
from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException

from src.TextSummrization.components.data_ingestion import DataIngestion
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts ,DataValidationArtifacts ,DataTransformationArtifacts ,ModelTrainingArtifacts,ModelEvaluationArtifacts
from src.TextSummrization.components.data_validation import Datavalidation
from src.TextSummrization.components.data_transformation import DataTransformer
from src.TextSummrization.components.model_trainer import ModelTrainer
from src.TextSummrization.components.model_evaluation import ModelEvaluation


import os,sys 
import pandas as pd 
import uuid 
from threading import Thread


class Pipeline():
    def __init__(self,config:ConfigurationManager):
        try:
            os.makedirs(config.get_training_pipeline_config().artifact_dir ,exist_ok=True) 
            self.config = config

        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
    def start_data_ingestion(self ) ->DataIngestionArtifacts:

        try:
            print('Data Ingestion Step Started')
            data_ingestion_config  = self.config.get_data_ingestion_config()

            data_ingestion = DataIngestion(
                data_ingestion_config=data_ingestion_config
            ) 
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

            print('Data Ingestion Step Completed')
            return data_ingestion_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys)
    def start_data_validation(self ,data_ingestion_artifacts : DataIngestionArtifacts) ->DataValidationArtifacts:
        try:
            print('Data Validation Step Started')
            self.data_ingestion_artifacts = data_ingestion_artifacts
  
            data_validation_config = self.config.get_data_validation_config()
            data_validation = Datavalidation(
                data_validation_config= data_validation_config ,
                data_ingestion_artifacts= self.data_ingestion_artifacts 
            )
            data_validation_artifacts = data_validation.initiate_data_validation()
            print('Data Validation Step Completed')
            return data_validation_artifacts 
        except Exception as e:
            raise TextSummarizationException(e ,sys)   
   
    def start_data_transformation(self)->DataTransformationArtifacts:
        try:
            print('Data Transformation Step Started')
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifact)
            data_transformation_config = self.config.get_data_transformation_config()
        
            data_transformation = DataTransformer(
                data_transformation_config= data_transformation_config,
                data_ingestion_artifacts= data_ingestion_artifact,
                data_validation_artifacts= data_validation_artifacts
            )
            data_transformation_artifacts = data_transformation.initiated_data_transformation()
            print('Data Transformation Step Completed')
            return data_transformation_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys)   
    # def start_model_traiing(self)->ModelTrainingArtifacts:
        try:
            print('Model training Step Started') 
            model_training_config = self.config.get_model_training_config()
            data_transformation_artifacts = self.start_data_transformation()
            model_trainer = ModelTrainer(
                model_training_config = model_training_config,
                data_transformation_artifacts = data_transformation_artifacts
   
            )
            model_trainer.initiate_model_training()
        except Exception as e:
            raise TextSummarizationException(e ,sys)  
        
    def start_model_evaluation(self)->ModelEvaluationArtifacts:
        try:
            print("model_evaluation_started") 
            model_evaluation_config = self.config.get_model_evaluation_config()
            # model_training_artifacts = self.start_model_traiing()
            # model_training_artifacts = ''
            data_transformation_artifacts = self.start_data_transformation()
            model_evaluation = ModelEvaluation(
                model_evaluation_config= model_evaluation_config,
                # model_training_artifacts= model_training_artifacts,
                data_transformation_artifacts= data_transformation_artifacts
            )
            model_evaluation_artifacts =model_evaluation.initiate_model_evaluation()
            print(model_evaluation_artifacts)
        except Exception as e:
            raise TextSummarizationException(e ,sys)  




   
# D:\Data Science\NLP\Project\Text-Summarizer-Project\src\TextSummrization\pipeline\training_pipeline.py

if __name__ == '__main__':
    pipeline = Pipeline(config=ConfigurationManager())
    # data_ingestion_artifact = pipeline.start_data_ingestion()
    # data_validation_artifacts = pipeline.start_data_validation(data_ingestion_artifacts= data_ingestion_artifact)
    # data_trandformation_artifacts = pipeline.start_data_transformation()
    # model_training_artifacts = pipeline.start_model_traiing()
    model_evaluation_config = pipeline.start_model_evaluation()

    # D:\Data Science\NLP\Project\Text-Summarizer-Project\src\TextSummrization\pipeline\training_pipeline.py
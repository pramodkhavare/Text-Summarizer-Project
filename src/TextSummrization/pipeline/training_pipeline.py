from src.TextSummrization.config.configuration import ConfigurationManager 
from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException

from src.TextSummrization.components.data_ingestion import DataIngestion
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts ,DataValidationArtifacts ,DataTransformationArtifacts ,ModelTrainingArtifacts,ModelEvaluationArtifacts ,ModelPusherArtifacts
from src.TextSummrization.components.data_validation import Datavalidation
from src.TextSummrization.components.data_transformation import DataTransformer
from src.TextSummrization.components.model_trainer import ModelTrainer
from src.TextSummrization.components.model_evaluation import ModelEvaluation
from src.TextSummrization.components.model_pusher import ModelPusher


import os,sys 
import pandas as pd 
import uuid 
from threading import Thread


class Training_Pipeline():
    def __init__(self,config:ConfigurationManager):
        try:
            os.makedirs(config.get_training_pipeline_config().artifact_dir ,exist_ok=True) 
            self.config = config

        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
    def start_data_ingestion(self ) ->DataIngestionArtifacts:

        try:
            print("\n>>>>>>>>>>>>>>>>>>>>>>>> Data Ingestion Step Started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

            data_ingestion_config  = self.config.get_data_ingestion_config()

            data_ingestion = DataIngestion(
                data_ingestion_config=data_ingestion_config
            ) 
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

            print('>>>>>>>>>>>>>>>>>>>>>>>> Data Ingestion Step Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return data_ingestion_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys)
    def start_data_validation(self ,data_ingestion_artifacts : DataIngestionArtifacts) ->DataValidationArtifacts:
        try:
            print('\n>>>>>>>>>>>>>>>>>>>>>>>> Data Validation Step Started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            self.data_ingestion_artifacts = data_ingestion_artifacts
  
            data_validation_config = self.config.get_data_validation_config()
            data_validation = Datavalidation(
                data_validation_config= data_validation_config ,
                data_ingestion_artifacts= self.data_ingestion_artifacts 
            )
            data_validation_artifacts = data_validation.initiate_data_validation()
            print('>>>>>>>>>>>>>>>>>>>>>>>> Data Validation Step Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return data_validation_artifacts 
        except Exception as e:
            raise TextSummarizationException(e ,sys)   
   
    def start_data_transformation(self ,data_ingestion_artifact:DataIngestionArtifacts ,data_validation_artifacts:DataValidationArtifacts)->DataTransformationArtifacts:
        try:
            print('\n>>>>>>>>>>>>>>>>>>>>>>>> Data Transformation Step Started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = self.config.get_data_transformation_config()
        
            data_transformation = DataTransformer(
                data_transformation_config= self.data_transformation_config,
                data_ingestion_artifacts= self.data_ingestion_artifact,
                data_validation_artifacts= self.data_validation_artifacts
            )
            data_transformation_artifacts = data_transformation.initiated_data_transformation()
            print('>>>>>>>>>>>>>>>>>>>>>>>> Data Transformation Step Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return data_transformation_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys) 
          
    def start_model_traiing(self ,data_transformation_artifacts:DataTransformationArtifacts)->ModelTrainingArtifacts:
        """
        Due to system limitations, we are not executing these functions locally.
        Instead, we run the entire code on Google Colab and download the model and tokenizer into a folder separately.
        We use the same model and tokenizer each time.
        In the future, if we upgrade our system, we will execute these functions directly.
        
        """
        try:

            print('\n>>>>>>>>>>>>>>>>>>>>>>>> Model training Step Started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<') 
            model_training_config = self.config.get_model_training_config()
            self.data_transformation_artifacts = data_transformation_artifacts
            model_trainer = ModelTrainer(
                model_training_config = model_training_config,
                data_transformation_artifacts = self.data_transformation_artifacts
   
            )
            model_trainer_artifacts =model_trainer.initiate_model_training()
            print(">>>>>>>>>>>>>>>>>>>>>>>> Model_training_completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            return model_trainer_artifacts
        except Exception as e:
            raise TextSummarizationException(e ,sys)  
        
    def start_model_evaluation(self ,model_training_artifacts:ModelTrainingArtifacts ,data_transformation_artifacts:DataTransformationArtifacts)->ModelEvaluationArtifacts:
        try:
            print("\n>>>>>>>>>>>>>>>>>>>>>>>> model_evaluation_started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<") 
            self.model_evaluation_config = self.config.get_model_evaluation_config()
            self.model_training_artifacts = model_training_artifacts
            self.data_transformation_artifacts = data_transformation_artifacts

            model_evaluation = ModelEvaluation(
                model_evaluation_config= self.model_evaluation_config,
                model_training_artifacts= self.model_training_artifacts,
                data_transformation_artifacts= self.data_transformation_artifacts
            )
            model_evaluation_artifacts =model_evaluation.initiate_model_evaluation()
            print("\n>>>>>>>>>>>>>>>>>>>>>>>> model_evaluation_started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<") 
            return model_evaluation_artifacts
        except Exception as e:
            raise TextSummarizationException(e ,sys)  
        
    def start_model_pusher(self ,model_evaluation_artifacts:ModelEvaluationArtifacts) ->ModelPusherArtifacts:
        try:
            print('\n>>>>>>>>>>>>>>>>>>>>>>>> Model Pushing Started <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            model_pusher_config = self.config.get_model_pusher_config()
            self.model_evaluation_artifacts =model_evaluation_artifacts
            # model_evaluation_artifacts = self.start_model_evaluation()
            model_pusher =ModelPusher(
                model_pusher_config= model_pusher_config,
                model_evaluation_artifacts=  "model_evaluation_artifacts"
            )
            model_pusher_artifacts = model_pusher.initiate_export_model()

            print('>>>>>>>>>>>>>>>>>>>>>>>> Model Pushing Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            return model_pusher_artifacts
        
        except Exception as e:
            raise TextSummarizationException(e ,sys)  
        

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts= data_ingestion_artifact)
            data_trandformation_artifacts = self.start_data_transformation(
                data_ingestion_artifact= data_ingestion_artifact ,
                data_validation_artifacts= data_validation_artifacts
            )
            # model_training_artifacts = self.start_model_traiing(
            #     data_transformation_artifacts= data_trandformation_artifacts
            # )
            model_training_artifacts ="model_training_artifacts"
            model_evaluation_artifacts = self.start_model_evaluation(
                model_training_artifacts=model_training_artifacts ,
                data_transformation_artifacts=data_trandformation_artifacts
            )
            model_pusher_artifacts = self.start_model_pusher(
                model_evaluation_artifacts= model_evaluation_artifacts
            )

        except Exception as e:
            raise TextSummarizationException(e ,sys) 

    def run(self):
        try:
            self.run_pipeline()

        except Exception as e:
            raise TextSummarizationException(e ,sys) from e 
   
if __name__ == '__main__':
    pipeline = Training_Pipeline(config=ConfigurationManager())
    pipeline.run()
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> Training Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n')
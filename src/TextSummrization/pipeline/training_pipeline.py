from src.TextSummrization.config.configuration import ConfigurationManager 
from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException

from src.TextSummrization.components.data_ingestion import DataIngestion
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts 



import os,sys 
import pandas as pd 
import uuid 
from threading import Thread


class Pipeline():
    def __init__(self,config:ConfigurationManager):
        try:
            os.makedirs(config.get_training_pipeline_config() ,exist_ok=True) 
            self.config = config

        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
    def start_data_ingestion(self) ->DataIngestionArtifacts:
        try:
            data_ingestion_config  = self.config.get_data_ingestion_config()

            data_ingestion = DataIngestion(
                data_ingestion_config=data_ingestion_config
            ) 
            data_ingestion_output = data_ingestion.initiate_data_ingestion()

            print(data_ingestion_output)

            return data_ingestion_output

        except Exception as e:
            raise TextSummarizationException(e ,sys)
        
# D:\Data Science\NLP\Project\Text-Summarizer-Project\src\TextSummrization\pipeline\training_pipeline.py
if __name__ == '__main__':
    pipeline = Pipeline(config=ConfigurationManager())
    pipeline.start_data_ingestion()

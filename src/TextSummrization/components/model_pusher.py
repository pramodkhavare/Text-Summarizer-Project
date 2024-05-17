import os ,sys  
import shutil 
from src.TextSummrization.entity.config_entity import ModelPusherConfig 
from src.TextSummrization.entity.artifacts_entity import ModelEvaluationArtifacts,ModelPusherArtifacts

from src.TextSummrization.logger.logging import logging
from src.TextSummrization.exception import TextSummarizationException 

import numpy as np 
from src.TextSummrization.constant import * 



class ModelPusher:
    def __init__(self ,
                 model_pusher_config :ModelPusherConfig ,
                 model_evaluation_artifacts :ModelEvaluationArtifacts) :
        try:
            logging.info(f'\n\n{">" * 10} Model Pusher Step Started {"<" *10}') 
            self.model_pusher_config = model_pusher_config 
            self.model_evaluation_artifacts = model_evaluation_artifacts
        except Exception as e:
            raise TextSummarizationException(e,sys) from e 
        
    def initiate_export_model(self):
        try:
            # evaluated_model_file_path = self.model_evaluation_artifacts.model_file_path 
            # tokenizer_file_path = self.model_evaluation_artifacts.tokennizer_file_path 

            tokenizer_file_path = "D:\\Data Science\\NLP\\Project\\Text-Summarizer-Project\\artifact\\model_training\\tokenizer"
            evaluated_model_file_path = "D:\\Data Science\\NLP\\Project\\Text-Summarizer-Project\\artifact\\model_training\\pegasus-samsun_model"


            exported_model_file_path = self.model_pusher_config.export_model_file_path 
            exported_tokenizer_file_path = self.model_pusher_config.export_tokenizer_file_path
            # os.makedirs(self.model_pusher_config.export_dir_path ,exist_ok=True) 

            logging.info(f"Exporting model file from: [{evaluated_model_file_path}]")
            shutil.copytree(src=evaluated_model_file_path ,dst=exported_model_file_path) 
            logging.info(f"Exporting model file at: [{exported_model_file_path}]")
            

            logging.info(f"Exporting tokenizer file from: [{tokenizer_file_path}]")
            shutil.copytree(src= tokenizer_file_path,dst=exported_tokenizer_file_path)
            logging.info(f"Exporting tokenizer file at: [{exported_tokenizer_file_path}]") 

            model_pusher_artifacts = ModelPusherArtifacts(
                is_model_pushed =True ,
                export_model_file_path = exported_model_file_path,
                export_tokenizer_file_path = exported_tokenizer_file_path
            )
            return model_pusher_artifacts
            
            

        except Exception as e:
            raise TextSummarizationException(e,sys) from e 

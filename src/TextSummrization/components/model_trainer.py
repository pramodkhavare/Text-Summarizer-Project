from src.TextSummrization.config.configuration import ConfigurationManager
import os,sys 
from src.TextSummrization.entity.config_entity import ModelTrainingConfig
from src.TextSummrization.entity.artifacts_entity import DataIngestionArtifacts ,DataValidationArtifacts ,DataTransformationArtifacts ,ModelTrainingArtifacts
from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.exception import TextSummarizationException 
import pandas as pd 
import numpy as np 
from src.TextSummrization.utils.utils import read_yaml ,create_directories 
from datasets import load_dataset ,load_from_disk  ,load_metric
from src.TextSummrization.constant import * 
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
class ModelTrainer():
    def __init__(self ,
                 model_training_config : ModelTrainingConfig ,
                 data_transformation_artifacts : DataTransformationArtifacts): 
      
        try:
            logging.info(f'\n\n{"*" *20} Model Training Started{"*" *20}') 
            self.model_training_config = model_training_config
            self.data_transformation_artifacts = data_transformation_artifacts 
            model_config_file_path= self.model_training_config.model_config_file_path
            self.model_config_data = read_yaml(model_config_file_path)['model_details']

        except Exception as e:
            raise TextSummarizationException(e,sys)
    def train(self):
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            tokenizer = AutoTokenizer.from_pretrained(self.model_config_data["model_name"])
            model_pegasus =AutoModelForSeq2SeqLM.from_pretrained(self.model_config_data['model_name']).to(device)
            seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

            # dataset_samsun_pt = load_from_disk(self.data_transformation_artifacts.transformed_data_folder)

            trainer_args = TrainingArguments(
                output_dir = self.model_training_config.trained_model_folder_path ,
                num_train_epochs=self.model_config_data['num_train_epochs'],
                warmup_steps=self.model_config_data['warmup_steps'],
                per_device_train_batch_size=self.model_config_data['per_device_train_batch_size'], 
                per_device_eval_batch_size=self.model_config_data['per_device_eval_batch_size'],
                weight_decay=self.model_config_data['weight_decay'], 
                logging_steps=self.model_config_data['logging_steps'],
                evaluation_strategy=self.model_config_data['evaluation_strategy'], 
                eval_steps=self.model_config_data['eval_steps'], 
                save_steps=self.model_config_data['save_steps'],
                gradient_accumulation_steps=self.model_config_data['gradient_accumulation_steps']
            )
            
            dataset_samsun_pt =  load_from_disk(self.data_transformation_artifacts.transformed_data_folder )

            trainer = Trainer(model=model_pegasus, args=trainer_args,
                            tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                            train_dataset=dataset_samsun_pt['test'],
                            eval_dataset=dataset_samsun_pt["validation"])
            #Saving model
            os.makedirs(self.model_training_config.trained_model_folder_path ,exist_ok=True)
            
            trainer =trainer.train()
            model_pegasus.save_pretrained(self.model_training_config.trained_model_file_path)

            return trainer
        except Exception as e:
            raise TextSummarizationException(e,sys) 
    
    def initiate_model_training(self) ->ModelTrainingArtifacts:
        try:
            logging.info("Loading Transformed Data Into Varible") 
            self.train()
            trained_model_file_path = self.model_training_config.trained_model_file_path
            tokenizer_file_path =self.model_training_config.tokenizer_file_path
            model_training_artifacts = ModelTrainingArtifacts(
                trained_model_file_path= trained_model_file_path ,
                tokenizer_file_path= tokenizer_file_path
            )
            return model_training_artifacts
        except Exception as e:
            raise TextSummarizationException(e,sys)
        



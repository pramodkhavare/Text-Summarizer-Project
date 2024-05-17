from src.TextSummrization.exception import TextSummarizationException 
from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.entity.config_entity import ModelEvaluationConfig 
from src.TextSummrization.entity.artifacts_entity import ModelTrainingArtifacts,DataTransformationArtifacts,ModelEvaluationArtifacts 

import os ,sys 
from transformers import AutoTokenizer ,AutoModelForSeq2SeqLM 
from datasets import load_dataset ,load_from_disk ,load_metric 
import torch 
import pandas as pd 
import tqdm
import numpy as np 
from tqdm import tqdm

class ModelEvaluation():
    def __init__(self ,model_evaluation_config : ModelEvaluationConfig,
                 model_training_artifacts : ModelTrainingArtifacts ,
                 data_transformation_artifacts : DataTransformationArtifacts) :
        try:
            self.model_evaluation_config = model_evaluation_config 
            # self.model_training_artifacts = model_training_artifacts 
            self.data_transformation_artifacts = data_transformation_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys)  

    def generate_batch_sized_chunks(self,list_of_elements, batch_size):
        """split the dataset into smaller batches that we can process simultaneously
        Yield successive batch-sized chunks from list_of_elements."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]





    
    def calculate_metric_on_test_ds(self,dataset, metric, model, tokenizer, 
                               batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
                               column_text="article", 
                               column_summary="highlights"):
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
            zip(article_batches, target_batches), total=len(article_batches)):
            
            inputs = tokenizer(article_batch, max_length=1024,  truncation=True, 
                            padding="max_length", return_tensors="pt")
            
            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                            attention_mask=inputs["attention_mask"].to(device), 
                            length_penalty=0.8, num_beams=8, max_length=128)
            ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''
            
            # Finally, we decode the generated texts, 
            # replace the  token, and add the decoded texts with the references to the metric.
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, 
                                    clean_up_tokenization_spaces=True) 
                for s in summaries]      
            
            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]
            
            
            metric.add_batch(predictions=decoded_summaries, references=target_batch)
            
        #  Finally compute and return the ROUGE scores.
        score = metric.compute()
        return score

    def initiate_model_evaluation(self):
        try:

            device = "cuda" if torch.cuda.is_available() else "cpu"
            # os.makedirs(self.model_evaluation_config.model_evalution_dir ,exist_ok=True)

            """I was unable to run code on local sysytem so download model and tokenizer from colab"""
            # tokenizer = self.model_training_artifacts.tokenizer_file_path 
            # model_pegasus = self.model_training_artifacts.trained_model_file_path 
            # print(f"Tokenizer : {self.model_training_artifacts.tokenizer_file_path }") 
            # print(f"Model : {self.model_training_artifacts.trained_model_file_path }") 

            tokenizer_path = "D:\\Data Science\\NLP\\Project\\Text-Summarizer-Project\\artifact\\model_training\\tokenizer"
            model_pegasus_path = "D:\\Data Science\\NLP\\Project\\Text-Summarizer-Project\\artifact\\model_training\\pegasus-samsun_model"

            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_pegasus_path).to(device)
            # loading data ned(model_pegasus_path).to(device)


            dataset_samsum_pt = load_from_disk(self.data_transformation_artifacts.transformed_data_folder)
     

            rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
  
            rouge_metric = load_metric('rouge')

            score = self.calculate_metric_on_test_ds(
              dataset_samsum_pt['test'][0:10], rouge_metric, model_pegasus, tokenizer, batch_size = 2, column_text = 'dialogue', column_summary= 'summary'
               )



            rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )
            df = pd.DataFrame(rouge_dict ,index=['pegasus']) 

            os.makedirs(self.model_evaluation_config.model_evalution_dir ,exist_ok=True)
            df.to_csv(self.model_evaluation_config.report_file_path ,index=False) 


            model_file_path = model_pegasus_path

            tokennizer_file_path = tokenizer_path


            model_evaluation_artifacts = ModelEvaluationArtifacts(
                report_file_path= self.model_evaluation_config.report_file_path,
                message=f"Model Evaluation Completed .Thank you Pramod Khavare" ,
                model_file_path = model_file_path,
                tokennizer_file_path = tokennizer_file_path
            )

            return model_evaluation_artifacts

        except Exception as e:
            raise TextSummarizationException(e ,sys) 



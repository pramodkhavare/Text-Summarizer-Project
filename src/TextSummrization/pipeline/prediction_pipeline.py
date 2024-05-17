from src.TextSummrization.constant import * 
from src.TextSummrization.config.configuration import * 
from src.TextSummrization.utils.utils import * 
from src.TextSummrization.logger.logging import logging 
from src.TextSummrization.exception import TextSummarizationException
from transformers import AutoModelForSeq2SeqLM ,AutoTokenizer
from transformers import pipeline ,set_seed


class Summarization():
    def __init__(self  ):
        pass 

class Prediction_Pipeline():
    def __init__(self ,export_dir :str):
        try:
            self.model_dir = export_dir 
 
        except Exception as e:
            raise TextSummarizationException(e,sys)
        
    def get_latest_model_path(self):
        try:
            folder_list = os.listdir(self.model_dir) 

            sorted_folders = sorted(folder_list ,reverse=True) 

            newest_folder = sorted_folders[0] 

            filename  = os.listdir(os.path.join(self.model_dir ,newest_folder))[0]
            model_file_path = os.path.join(self.model_dir , newest_folder ,filename) 

            print(model_file_path)

            return model_file_path 
        
        except Exception as e:
            raise TextSummarizationException(e,sys)
        
    def get_latest_tokenizer_path(self):
        try:
            folder_list = os.listdir(self.model_dir)

            sorted_folders = sorted(folder_list ,reverse=True) 
            newest_folder = sorted_folders[0]
            filename  = os.listdir(os.path.join(self.model_dir ,newest_folder))[1]

            tokenizer_file_path = os.path.join(self.model_dir , newest_folder ,filename) 
            print(tokenizer_file_path) 

            return tokenizer_file_path 
 
        except Exception as e:
            raise TextSummarizationException(e,sys) 
    
    def prediction(self ,sample_data):
        try:
            logging.info("Prediction Has Been Started")

            model_path = self.get_latest_model_path()
            tokenizer_path = self.get_latest_tokenizer_path()



            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
            pegasus_samsum_model = AutoModelForSeq2SeqLM.from_pretrained(model_path) 


            gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": 300}

            pipe = pipeline(task='summarization' , model=pegasus_samsum_model ,tokenizer=tokenizer)

            output =  pipe(sample_data ,**gen_kwargs)[0]["summary_text"]

            print(output)
            return output

        except Exception as e:
            raise TextSummarizationException(e,sys) 

    
        
# if __name__ == "__main__":
#     prediction  =Prediction_Pipeline(export_dir="D:\\Data Science\\NLP\\Project\\Text-Summarizer-Project\\export_dir")
#     prediction.prediction("PRamod")

    # D:\Data Science\NLP\Project\Text-Summarizer-Project\src\TextSummrization\pipeline\prediction_pipeline.py
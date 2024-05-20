import typing
import numpy as np
import pandas as pd
from tqdm import tqdm

from mltu.configs import BaseModelConfigs
from mltu.inferenceModel import OnnxInferenceModel
from mltu.preprocessors import WavReader
from mltu.utils.text_utils import ctc_decoder, get_cer, get_wer

class WavToTextModel(OnnxInferenceModel):
    
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, data: np.ndarray):
        data_pred = np.expand_dims(data, axis=0)

#       Get Prediction accross spectogram
        preds = self.model.run(self.output_names, {self.input_names[0]: data_pred})[0]

#       Get Predicted characters
        text = ctc_decoder(preds, self.char_list)[0]

        return text
    
class STT():
    config_path = "Models/05_sound_to_text/202302051936/configs.yaml"
    val_path = "Models/05_sound_to_text/202302051936/val.csv"
    
    audio_path = ""
    
    def parse_config(self):
        self.configs = BaseModelConfigs.load(self.config_path)
    
    def load_model(self):
        self.model = WavToTextModel(model_path=self.configs.model_path, char_list=self.configs.vocab, force_cpu=False)
    
    def parse_model_val(self):
        self.val = pd.read_csv(self.val_path).values.tolist()
        
    def parse_spectogram(self, file_path):
        spectrogram = WavReader.get_spectrogram(file_path, frame_length=self.configs.frame_length, frame_step=self.configs.frame_step, fft_length=self.configs.fft_length)
        
        spectrogram = np.pad(spectrogram, ((0, self.configs.max_spectrogram_length - spectrogram.shape[0]), (0, 0)), mode='constant', constant_values=0)

        segment_length = self.configs.max_spectrogram_length
        
        # Check if need to be segmented
        if (spectrogram.shape[0] > segment_length):
            num_segments = spectrogram.shape[0] // segment_length
            
            # split spectrogram 
            spectrogram = np.split(spectrogram[:num_segments * segment_length], num_segments)
        
        return spectrogram
    
    def predict(self, file_path):
        text = ""
        
        self.parse_config()
        self.load_model()
        self.parse_model_val()
        
        # check if spectogram segmented 
        spec = self.parse_spectogram(file_path)
        text = self.model.predict(spec)
        
        return text
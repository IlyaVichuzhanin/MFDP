from transformers import BlipForConditionalGeneration, BlipProcessor

class MLmodel:

    def __init__(self):
        self.__model= BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.__image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")


    @property
    def model(self):
        return self.__model
    
    @property
    def image_processor(self):
        return self.__image_processor
    
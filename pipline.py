import nemo.collections.nlp.models as nlp_models

def nlp_model_pipeline(text):
    # Load the pretrained BERT model
    model = nlp_models.PunctuationCapitalizationModel.from_pretrained("bert-base-uncased")
    return model
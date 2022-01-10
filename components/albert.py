from rasa.nlu.featurizers.dense_featurizer.lm_featurizer import LanguageModelFeaturizer
from typing import List, Text
import numpy as np

from transformers import TFAlbertModel # correct model for laoding from PyTorch
from transformers import AlbertTokenizer


class AlbertFeaturizer(LanguageModelFeaturizer):
    """
    AlbertFeaturizer
        Custom LanguageModelFeaturizer that uses pretrained Albert
        doesn't need any pre component and returns word embeddings
    """
    def _load_model_metadata(self) -> None:
        self.model_name = 'albert'
        self.model_weights = 'm3hrdadfi/albert-fa-base-v2'
        self.max_model_sequence_length = 512

    def _load_model_instance(self, skip_model_load: bool) -> None:
        self.tokenizer = AlbertTokenizer.from_pretrained(self.model_weights)
        # the original model is just available in PyTorch
        self.model = TFAlbertModel.from_pretrained(self.model_weights, from_pt=True)
        # check model freeze later
        self.model.trainable = False
        self.pad_token_id = self.tokenizer.unk_token_id

    def _lm_specific_token_cleanup(self, split_token_ids: List[int], token_strings: List[Text]):
        token_ids_string = list(zip(split_token_ids, token_strings))
        token_ids_string = [(id, string.replace("▁", "")) for id, string in token_ids_string]
        # remove empty strings
        token_ids_string = [(id, string) for id, string in token_ids_string if string]
        # return as individual token ids and token strings
        token_ids, token_strings = zip(*token_ids_string)
        return token_ids, token_strings


    def _add_lm_specific_special_tokens(self, token_ids: List[List[int]]):
        augmented_tokens = []
        for example_token_ids in token_ids:
            example_token_ids.insert(0, 2)  # insert CLS token id (in Albert)
            example_token_ids.append(3)  # # insert SEP token id (in Albert)
            augmented_tokens.append(example_token_ids)
        return augmented_tokens


    def _post_process_sequence_embeddings(self, sequence_embeddings: np.ndarray):
        sentence_embeddings = []
        post_processed_sequence_embeddings = []

        for example_embedding in sequence_embeddings:
            sentence_embeddings.append(example_embedding[0]) # use CLS token as sentence embeddings
            post_processed_sequence_embeddings.append(example_embedding[1:-1])

        return np.array(sentence_embeddings), np.array(post_processed_sequence_embeddings)

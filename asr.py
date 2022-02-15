import os
import logging
import time
import string

import jiwer
import soundfile as sf
import numpy as np
from unidecode import unidecode
import wandb

import torch
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_inference import Speech2Text

lang = 'en'
fs = 16000
tag = 'Shinji Watanabe/spgispeech_asr_train_asr_conformer6_n_fft512_hop_length256_raw_en_unnorm_bpe5000_valid.acc.ave'

def setup_model():
    d = ModelDownloader()
    # It may takes a while to download and build models
    return Speech2Text(
        **d.download_and_unpack(tag),
        device="cuda",
        minlenratio=0.0,
        maxlenratio=0.0,
        ctc_weight=0.3,
        beam_size=10,
        batch_size=0,
        nbest=1
    )

def evaluate(testset, audio_directory):
    model = setup_model();
    predictions = []
    targets = []
    for i, datapoint in enumerate(testset):
        target_text = unidecode(datapoint['text'])
        if len(target_text.strip()) < 2:
            continue
        targets.append(target_text)
        audio, rate = sf.read(os.path.join(audio_directory,f'example_output_{i}.wav'))
        assert rate == fs, 'wrong sample rate'
        # audio_int16 = (audio*(2**15)).astype(np.int16)
        nbests = model(audio)
        text, *_ = nbests[0]
        predictions.append(text)
    transformation = jiwer.Compose([jiwer.RemovePunctuation(), jiwer.ToLowerCase()])
    targets = transformation(targets)
    predictions = transformation(predictions)
    wer = jiwer.wer(targets, predictions)
    logging.info(f'targets: {targets}')
    logging.info(f'predictions: {predictions}')
    logging.info(f'wer: {wer}')
    wandb.run.summary["wer"] = wer
    wandb.run.summary["targets"] = targets
    wandb.run.summary["predictions"] = predictions

#!/bin/bash

export LD_LIBRARY_PATH=~/silent_speech/nv_wavenet/pytorch:$LD_LIBRARY_PATH

python3 evaluate.py --models ./models/phoneme_transduction_model/model.pt --pretrained_wavenet_model ./models/wavenet_model/wavenet_model.pt --output_directory open_vocab_output
# python3 evaluate.py --models ./models/closed_vocab_model/model.pt --pretrained_wavenet_model ./models/wavenet_model/wavenet_model.pt --output_directory closed_vocab_output --silent_data_directories emg_data/closed_vocab/silent --voiced_data_directories emg_data/closed_vocab/voiced  --testset_file testset_closed.json

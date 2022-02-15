#!/bin/bash

export LD_LIBRARY_PATH=~/silent_speech/nv_wavenet/pytorch:$LD_LIBRARY_PATH

python3 transduction_model.py --pretrained_wavenet_model "./models/wavenet_model/wavenet_model.pt" --output_directory "./models/test_vocab_model/" --silent_data_directories emg_data/closed_vocab/silent --voiced_data_directories emg_data/closed_vocab/voiced --testset_file testset_closed.json

#!/bin/bash

export LD_LIBRARY_PATH=~/silent_speech/nv_wavenet/pytorch:$LD_LIBRARY_PATH

python3 wavenet_model.py --output_directory "./models/closed_wavenet_model/" --silent_data_directories "" --voiced_data_directories emg_data/closed_vocab/voiced --testset_file testset_closed.json

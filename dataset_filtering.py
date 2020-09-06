from glob import glob
from os.path import join, exists, basename
from os import makedirs, listdir
from shutil import copy
from random import shuffle

import argparse



def filter_wav_dataset(wav_path, output_path, n_wav_actor=10):

    for actor in listdir(wav_path):
        actor_path = join(wav_path, actor)
        wavs = glob(actor_path + '/**/*.wav', recursive=True)

        actor_out_path = join(output_path, actor)
        if not exists(actor_out_path):
            makedirs(actor_out_path)
        shuffle(wavs)
        count = 0
        for wav in wavs:
            count += 1
            if count > n_wav_actor: 
                break
            copy(wav, join ( actor_out_path ,basename(actor_out_path) + '_' + str(count) + '.wav'))
            
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Filter wav datset')
    parser.add_argument('path_wavs',  type=str, help='Wav path')
    parser.add_argument('out_path', type=str, help='out_dir')                    
    parser.add_argument('--nwav',type=int, help='Number of wavs for each actor')
    
    args = parser.parse_args()

    
    filter_wav_dataset(args.path_wavs, args.out_path, args.nwav)

    


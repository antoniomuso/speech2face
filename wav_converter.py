from glob import glob
from os.path import join, exists, basename
from os import makedirs, listdir
import numpy as np
from tqdm import tqdm
import librosa

def power_law(signal):
  converted = signal
  sign = np.sign(converted)
  converted[:, :, 0] = np.abs(converted[:, :, 0])** 0.3
  converted[:, :, 1] = np.abs(converted[:, :, 1])** 0.3
  return sign * converted
  

def load_wav(wav_path):
  def adjust(stft):
    if stft.shape[1] == 601:
      return stft
    else:
      return np.concatenate((stft,stft[:,0:601 - stft.shape[1]]),axis = 1)

  wav, sr = librosa.load(wav_path,sr = 16000, duration = 6.0 ,mono = True)
  spectro = librosa.core.stft(wav, n_fft = 512, hop_length = int(np.ceil(0.01 * sr)),win_length = int(np.ceil(0.025 * sr)) , window='hann', center=True,pad_mode='reflect') 
  spectroComplex = adjust(spectro)
  converted = np.zeros((spectroComplex.shape[0], spectroComplex.shape[1], 2))
  i = np.arange(spectroComplex.shape[0])
  j = np.arange(spectroComplex.shape[1])
  
  converted[i,j[:,np.newaxis], 0] = spectroComplex[i,j[:,np.newaxis]].real
  converted[i,j[:,np.newaxis], 1] = spectroComplex[i,j[:,np.newaxis]].imag

  return power_law(converted)


def convert_files(main_dir, out_dir):
    actors = listdir(main_dir)
    for i in tqdm(range(len(actors))):
        actor = actors[i]
        actor_path = join(main_dir, actor)
        wavs = glob(actor_path + '/**/*.wav', recursive=True)

        actor_out_path = join(out_dir, actor)
        if not exists(actor_out_path):
            makedirs(actor_out_path)    
        for wav in wavs:
            conv = load_wav(wav)
            sav = wav.replace('.wav', '.npy')
            sav = sav.replace('wav_filtered_20_per_actor', 'wav_filtered_20_per_actor_np')
            #print(sav)

            np.save(sav, conv)

    #np.save

if __name__ == '__main__':
    md = '/home/kron/shared/Desktop/Uni-Informatica/Magistrale/Deep Learning/Project/wav_filtered_20_per_actor'
    od = '/home/kron/shared/Desktop/Uni-Informatica/Magistrale/Deep Learning/Project/wav_filtered_20_per_actor_np'

    convert_files(md, od)
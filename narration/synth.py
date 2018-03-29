
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer as synth
import os
import json
# Create your views here.

#print(type(post.title))            
Synthesizer = synth()
hparams.parse("")
cwd = os.getcwd()
print(cwd)
checkpoint=cwd+"/narration/saved_model/tacotron-20170720/model.ckpt"
print(checkpoint)
Synthesizer.load(checkpoint)

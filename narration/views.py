from django.shortcuts import render
from .forms import ContentForm
from django.utils import timezone
import os

from speechmodel import textToAudio
from video import video_generator
from imagemodel import textToImage
           
no_of_sentences = 2
folder_name = 'narration/audio'


def home(request):
    if request.method == "POST":
        form=ContentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            g = post.text
            if g[-1] == '.':
                g = g[:-1]
            TTA = textToAudio()
            # Object for generating Images
            TTI = textToImage()
            #    Returns paragraph list and saves audio in a folder named audio
            para_list = TTA.generate_audio(text = g, no_of_sentences = no_of_sentences, folder_name = folder_name)
            tags = TTI.getTags(para_list = para_list, get_urls = False, download = True)
            video_generator(para_list, tags)
            pdc = "temp/hello.mp4"
            post.created_date = timezone.now()
            post.save()
            return render(request,'views/index.html', {'media':pdc} )
    else:    
        form=ContentForm()
    return render(request, "views/home.html", {"form":form})

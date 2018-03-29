import os
from contextlib import closing
import sys
import re
from synth import Synthesizer, checkpoint



class textToAudio(object):

    def split_into_sentences(self, text):
        caps = "([A-Z])"
        digits = "([0-9])"
        prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov|me|edu)"

        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = text.replace("—", " ")
        text = text.replace("\t", " ")
        text = text.replace('\r', " ")
        text = text.replace('\'', "")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
        text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        if "..." in text: text = text.replace("...","<prd><prd><prd>")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>","")
        if text[-1] == '.':
            text = text[:-1]
        sentences = text.split("<stop>")
        if sentences[-1] == '':
            sentences = sentences[:-1]
        #sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    def paragraph_creator(self, sentences, sentences_length):
        count = 0
        segment = ""

        sentences_segments = []

        for i in range(len(sentences)):
            segment = segment + " " + sentences[i]
            count+=1

            if (count == sentences_length or i == len(sentences)-1):
                count = 0
                sentences_segments.append(segment)
                segment = ""

        return sentences_segments

    def final_audio_files(self, paragraphs, client, folder_name = 'narration/audio'):
        for i in range(len(paragraphs)):
            Synthesizer.synthesize(paragraphs[i] , 'audio_file_' +str(i+1) + '.wav' )
    

    def generate_audio(self, text, no_of_sentences, folder_name = 'audio'):
        sentences = self.split_into_sentences(text)
        paragraphs = self.paragraph_creator(sentences, no_of_sentences)
        self.final_audio_files(paragraphs, client, folder_name = 'narration/audio')
        
        return paragraphs






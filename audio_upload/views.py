from django.shortcuts import render
import openai

from whisperHandle import settings
from .forms import Profile_Form
from .models import Upload_audio
import os
import csv


# Create your views here.
IMAGE_FILE_TYPES = ['mp3', 'wav']

def create_upload(request):
    form = Profile_Form()
    
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.display_audio = request.FILES['display_audio']
            file_type = user_pr.display_audio.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'profile_maker/error.html')
            user_pr.save()
            
            audio_file_path = os.path.join(settings.MEDIA_ROOT, str(request.FILES['display_audio']))
            print(request.FILES['display_audio'])
            print(settings.MEDIA_ROOT)

            openai.api_key = "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"

            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    file=audio_file,
                    model="whisper-1",
                    response_format="srt",
                    language="ja"
                )
                print(transcript)

                num_array = []
                time_array = []
                content_array = []

                # Split the transcript by newline character
                lines = transcript.split("\n")

                # Loop through each line of the transcript
                for i in range(0, len(lines), 4):
                    # Extract the number value and append to the num_array
                    if not lines[i].strip().isdigit():
                        continue
                    num = int(lines[i])
                    num_array.append(num)

                    # Extract the time value and append to the time_array
                    time = lines[i+1].strip()
                    time_array.append(time)

                    # Extract the content value and append to the content_array
                    content = lines[i+2].strip()
                    content_array.append(content)

                # Print the arrays
                print("num_array:", num_array)
                print("time_array:", time_array)
                print("content_array:", content_array)

                with open('transcript.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Number', 'Time', 'Content'])  # Write column headers
                    for i in range(len(num_array)):
                        writer.writerow([num_array[i], time_array[i], content_array[i]])

                # Open the CSV file
                os.startfile('transcript.csv')

    context = {"form": form,}
    return render(request, 'profile_maker/create.html', context)
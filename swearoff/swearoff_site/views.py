from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from .forms import AudioForm
from .models import Audio

def uploadView(request):
	if request.method == 'POST':
		form = AudioForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/result/');
	else:
		form = AudioForm()
		return render(request, 'index.html', {'form': form})

def downloadView(request):
	if request.method == 'POST':		
		audios = Audio.objects.all()
		response = FileResponse(audios[0].audio, as_attachment=True)
		audios[0].delete()
		return response
	else :
		return render(request, 'result.html', {})
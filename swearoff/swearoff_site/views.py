from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from .forms import AudioForm
from .models import Audio
from .swearoffAPI.recognition import Censored

def uploadView(request):
	request.session.set_expiry(0)
	if request.method == 'POST':
		form = AudioForm(request.POST, request.FILES)
		if form.is_valid():
			model = form.save()
			request.session['fileId'] = model.id
			print(model.language)
			return redirect('/result/');
	else:
		form = AudioForm()
		return render(request, 'index.html', {'form': form})

def downloadView(request):
	audio = Audio.objects.get(id=request.session['fileId'])
	if request.method == 'POST':		
		response = FileResponse(audio.censored_audio, as_attachment=True)
		audios.delete()
		return response
	else :
		Censored(audio.audio.path,audio.language, audio)
		return render(request, 'result.html', {})
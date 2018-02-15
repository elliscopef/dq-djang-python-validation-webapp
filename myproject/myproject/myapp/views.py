# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
from resource.LibraryFile import simpleHTTPServerWithUpload
from resource import validateMarginFile
from resource import varSettings
global logInfo 

logInfo = []
def list(request):
    # Handle file upload

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            print(request.FILES['docfile'])
            #handle the validation of the newly loaded file
            #fn = os.path.join(path, fn[0])
            
            validateMarginFile.validateMarginFileProcess("/Users/mifang/Documents/Expedia/Project/tutorial/djangoTutorial/dq-djang-python-validation-webapp/myproject/myproject/myapp/resource/DataFile/sample3.0.csv",3,logInfo)
            # print logInfo
            #simpleHTTPServerWithUpload.validateCsvFile()
            #simpleHTTPServerWithUpload.validateCsvFile("/Users/mifang/Documents/Expedia/Project/tutorial/djangoTutorial/dq-djang-python-validation-webapp/myproject/myproject/myapp/resource/DataFile/sample3.0.csv",3)
            #navigation to a validation log page

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('log'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )

def log(request):
    return render(
        request,
        'log.html',
        {'documents': logInfo}
    )


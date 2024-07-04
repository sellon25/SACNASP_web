import subprocess
# Use pip to install Pythonnet
subprocess.call(["pip", "install", "pythonnet"])
from django.shortcuts import render
import clr
print("Pythonnet is working and can load Mono")
import os
from System.Collections.Generic import List

project_root = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(project_root, 'SACNASP_DLL', 'SACNASP_DATA.dll')
print(dll_path)
clr.AddReference(dll_path)
from SACNASP_DATA import PercentageComputation
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
import json

#from .models import Universities, Qualifications

obj=PercentageComputation()
csv_files=[] 
university_folder = 'SACNASP_DLL\\Necessary Files\\UniversityFiles\\'
university_folder1 = 'SACNASP_DLL\\Necessary Files\\UniversityFiles'

csv_files = [file for file in os.listdir(university_folder) if file.endswith('.csv')]
# Convert the Python list to a List[string] object
csv_files_list=[]
csv_files_list = List[str]()
emptyList= [] = List[str]()

for file in csv_files:
   
    if file.strip() != None:            
        # print(str(i)+": "+file)
        # i=i+1
        csv_files_list.Add(file)
print("======set===========")      

obj.setUniversuty(csv_files_list) 

y=0   



print("=======get==========")    
universities=obj.getUniversities()




# VIEWS
def check(request):
    return render(request, 'SACNASPregister.html', {})

def university_list(request):
    global obj  
    i=0
    print("HERE university_list:")
    for uni in universities:
        i=i+1
        print(str(i)+"uni: "+uni) 
     
       
    context = {'uniName': universities}
   
    return render(request, 'SACNASPregister.html', context)


temp=[]
def qualification_names(request): 
    global obj,temp 
    print("HERE qualification_names")
    fullfile=List[str]()
    for file in csv_files:
        fullfile.Add(university_folder+"\\"+file)
    for file in fullfile:
         print(file)
   
   
    print("======get index========")
    if request.body:
        try:
            response_data = {
                'availQualifications': ''  #empty list
            }
            # Get the selected university from the request body
            data = json.loads(request.body)
            selected_university = int(data.get('university'))          
            
            

            # Return the qualifications as JSON response
            print("index:" + str(selected_university) + "=========")
            index = selected_university          
            
            obj.UniversityFiles=emptyList
            obj.QualificationNames =emptyList
            print("====empty uni list====")
            for q in obj.UniversityFiles: 
                print("here after emptying--"+q)
            print("=========new set qualifications==========")
            obj.setUniversuty(fullfile) 
            qualifications=[]         
            qualifications = obj.getQualifications(index)
            qualifications = [q for q in qualifications if q not in temp]
            temp = qualifications
            #for q in qualifications: 
            #    print("here--"+q)
            qualifications_text = "\n".join(qualifications)
            print("---qt: \n"+qualifications_text)
            response_data = {
                'availQualifications': qualifications_text  # Changed key name to match the one used in JavaScript
            }
           
            return JsonResponse(response_data)

            
        except json.JSONDecodeError:
            # Handle the error when the request body does not contain valid JSON
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    else:
        # Handle the error when the request body is empty
        return HttpResponseBadRequest('Empty request body') 
    



def results(request):
    global obj
    print("===== request.POST.get==========")
    data=json.loads(request.body)
    print(str(data))
    selectedQualification = data.get('qualification')
    selectedNQFLevel = data.get('nqfLevel')
    selectedYearsOfExp = data.get('selectedYearsOfExp')

    results="None"
    selectedNQFLevel=int(selectedNQFLevel)+1
    print("=====getResults selectedQualification:"+ str(selectedQualification) +" ,selectedNQFLevel:"+str(selectedNQFLevel)+" ,selectedYesrsOfExp: "+str(selectedYearsOfExp)+"==========")
    if selectedQualification and selectedNQFLevel and selectedYearsOfExp:       

        if selectedQualification is not None and selectedNQFLevel is not None and selectedYearsOfExp is not None:
            score = obj.getQualificationPercentage(selectedQualification)
            print("===scoreI:"+str(score))
            x = obj.CalculationAdditions(int(selectedNQFLevel), int(selectedYearsOfExp))
            print("==x:"+str(x))
            bl=""
            score += x
            score/=3
            if score >= 50:
                results = "You are eligible to register as a SACNASP Scientist."
                bl=True
            else:
                results = "Unfortunately, you are not eligible to register as a SACNASP Scientist."
                bl=False
            print("======scoreF: " + str(score))
            
            

            print("=====Results: " + str(score) +", bool:"+ str(bl)+"==========")
        context = {'result': results,
                   'bl': bl }
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'One or more fields are missing or invalid.'}, status=400)

def results_page(request):
    return render(request, 'SACNASPResults.html')
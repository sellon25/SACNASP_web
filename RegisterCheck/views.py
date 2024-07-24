from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json
import os
from .PercentageComputation import PercentageComputation

obj = PercentageComputation()
csv_files = []
university_folder = 'SACNASP_DLL/Necessary Files/UniversityFiles/'

csv_files = [os.path.join(university_folder, file) for file in os.listdir(university_folder) if file.endswith('.csv')]
obj.set_university(csv_files)

print("=======get uni names==========")
universities = obj.get_universities()

# VIEWS
def check(request):
    return render(request, 'SACNASPregister.html', {})

def university_list(request):
    print("HERE university_list:")
    for i, uni in enumerate(universities, 1):
        print(f"{i} uni: {uni}")

    context = {'uniName': universities}
    return render(request, 'SACNASPregister.html', context)

temp = []

def qualification_names(request):
    global obj, temp
    print("HERE qualification_names")
    fullfile = csv_files

    print("======get index========")
    if request.body:
        try:
            response_data = {'availQualifications': ''}  # empty list
            data = json.loads(request.body)
            selected_university = int(data.get('university'))

            print("index:" + str(selected_university) + "=========")
            index = selected_university
            obj.set_university(fullfile)
            qualifications = obj.get_qualifications(index)
            qualifications = [q for q in qualifications if q not in temp]
            temp = qualifications
            qualifications_text = "\n".join(qualifications)
            print("---qt: \n" + qualifications_text)
            response_data = {'availQualifications': qualifications_text}  # Changed key name to match the one used in JavaScript

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    else:
        return HttpResponseBadRequest('Empty request body')

def results(request):
    global obj
    print("===== request.POST.get==========")
    data = json.loads(request.body)
    print(str(data))
    selected_qualification = data.get('qualification')
    selected_nqf_level = data.get('nqfLevel')
    selected_years_of_exp = data.get('selectedYearsOfExp')

    results = "None"
    selected_nqf_level = int(selected_nqf_level) + 1
    print("=====getResults selected_qualification:" + str(selected_qualification) +
          " ,selected_nqf_level:" + str(selected_nqf_level) +
          " ,selected_years_of_exp: " + str(selected_years_of_exp) + "==========")
    
    if selected_qualification and selected_nqf_level and selected_years_of_exp:
        if selected_qualification is not None and selected_nqf_level is not None and selected_years_of_exp is not None:
            score = obj.get_qualification_percentage(selected_qualification)
            print("===scoreI:" + str(score))
            x = obj.calculation_additions(int(selected_nqf_level), int(selected_years_of_exp))
            print("==x:" + str(x))
            bl = ""
            score += x
            score /= 3
            if score >= 50:
                results = "You are eligible to register as a SACNASP Scientist."
                bl = True
            else:
                results = "Unfortunately, you are not eligible to register as a SACNASP Scientist."
                bl = False
            print("======scoreF: " + str(score))
            
            print("=====Results: " + str(score) + ", bool:" + str(bl) + "==========")
        context = {'result': results, 'bl': bl}
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'One or more fields are missing or invalid.'}, status=400)

def results_page(request):
    return render(request, 'SACNASPResults.html')

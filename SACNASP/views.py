# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponseBadRequest
# import json
# import os
# from .percentage_computation import PercentageComputation

# obj = PercentageComputation()
# csv_files = []
# university_folder = 'SACNASP_DLL/Necessary Files/UniversityFiles/'

# csv_files = [os.path.join(university_folder, file) for file in os.listdir(university_folder) if file.endswith('.csv')]
# obj.setUniversuty(csv_files)

# print("=======get uni names==========")
# universities = obj.getUniversities()

# # VIEWS
# def check(request):
#     return render(request, 'SACNASPregister.html', {})

# def university_list(request):
#     print("HERE university_list:")
#     for i, uni in enumerate(universities, 1):
#         print(f"{i} uni: {uni}")

#     context = {'uniName': universities}
#     return render(request, 'SACNASPregister.html', context)

# temp = []

# def qualification_names(request):
#     global obj, temp
#     print("HERE qualification_names")
#     fullfile = csv_files

#     print("======get index========")
#     if request.body:
#         try:
#             response_data = {'availQualifications': ''}  # empty list
#             data = json.loads(request.body)
#             selected_university = int(data.get('university'))

#             print("index:" + str(selected_university) + "=========")
#             index = selected_university
#             obj.setUniversuty(fullfile)
#             qualifications = obj.getQualifications(index)
#             qualifications = [q for q in qualifications if q not in temp]
#             temp = qualifications
#             qualifications_text = "\n".join(qualifications)
#             print("---qt: \n" + qualifications_text)
#             response_data = {'availQualifications': qualifications_text}  # Changed key name to match the one used in JavaScript

#             return JsonResponse(response_data)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
#     else:
#         return HttpResponseBadRequest('Empty request body')

# def results(request):
#     global obj
#     print("===== request.POST.get==========")
#     data = json.loads(request.body)
#     print(str(data))
#     selectedQualification = data.get('qualification')
#     selectedNQFLevel = data.get('nqfLevel')
#     selectedYearsOfExp = data.get('selectedYearsOfExp')

#     results = "None"
#     selectedNQFLevel = int(selectedNQFLevel) + 1
#     print("=====getResults selectedQualification:" + str(selectedQualification) +
#           " ,selectedNQFLevel:" + str(selectedNQFLevel) +
#           " ,selectedYearsOfExp: " + str(selectedYearsOfExp) + "==========")
    
#     if selectedQualification and selectedNQFLevel and selectedYearsOfExp:
#         if selectedQualification is not None and selectedNQFLevel is not None and selectedYearsOfExp is not None:
#             score = obj.getQualificationPercentage(selectedQualification)
#             print("===scoreI:" + str(score))
#             x = obj.CalculationAdditions(int(selectedNQFLevel), int(selectedYearsOfExp))
#             print("==x:" + str(x))
#             bl = ""
#             score += x
#             score /= 3
#             if score >= 50:
#                 results = "You are eligible to register as a SACNASP Scientist."
#                 bl = True
#             else:
#                 results = "Unfortunately, you are not eligible to register as a SACNASP Scientist."
#                 bl = False
#             print("======scoreF: " + str(score))
            
#             print("=====Results: " + str(score) + ", bool:" + str(bl) + "==========")
#         context = {'result': results, 'bl': bl}
#         return JsonResponse(context)
#     else:
#         return JsonResponse({'error': 'One or more fields are missing or invalid.'}, status=400)

# def results_page(request):
#     return render(request, 'SACNASPResults.html')


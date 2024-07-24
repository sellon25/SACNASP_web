import os
import csv
from typing import List
from fuzzywuzzy import fuzz  # Install fuzzywuzzy for Levenshtein distance calculation

class PercentageComputation:
    def __init__(self):
        self.input_text = ""
        self.output_text = ""
        self.university_index = 0
        self.qualification_names = []
        self.qualification_indexes = []
        self.list_of_fields = []
        self.university_files = []
        self.folder_with_files = os.path.join('RegisterCheck','SACNASP_DLL', 'Necessary Files', 'data')
        self.agriculture_score = 0
        self.biology_score = 0
        self.maths_and_statistics_score = 0
        self.physics_score = 0
        self.chemistry_score = 0
        self.content = ""
        # Adjust base directory to correctly locate files
        self.base_data_dir = os.path.join('RegisterCheck','SACNASP_DLL', 'Necessary Files', 'data')

    def set_input_text(self, text: str):
        self.input_text = text

    def get_output_text(self) -> str:
        return self.output_text

    def set_output_text(self, text: str):
        self.output_text = text

    def set_university(self, university_files: List[str]):
        self.university_files = university_files

    def set_folder_with_files(self, folder: str):
        self.folder_with_files = folder

    def get_qualification_content(self) -> str:
        return self.content

    def check_for_keywords(self, search_text: str, file_path: str) -> int:
        # Read the keywords from the file
        found_terms = []
        keywords = []
        print(os.path.join(self.folder_with_files, file_path))
        with open(os.path.join(self.folder_with_files, file_path), 'r', encoding='utf-8') as file:
            keywords = file.read().splitlines()

        # Split the search text into individual words
        search_words = search_text.split()

        # Count the number of matches between the keywords and the search text
        score = 0
        for search_word in search_words:
            for keyword in keywords:
                if fuzz.ratio(keyword.lower(), search_word.lower()) >= 80:  # Adjust threshold as needed
                    score += 1
                    break

        return score

    def calculate_percentage(self, input_text: str, subject_file: str) -> float:
        # Sort and remove duplicates from file
        file_path = os.path.join(self.base_data_dir, subject_file)
        self.sort_and_remove_duplicates_from_file(os.path.join(self.base_data_dir, "listOfConjuctions.txt"))
        self.sort_and_remove_duplicates_from_file(file_path)

        # Process input text and calculate score
        curated_txt = self.curate_text(input_text, os.path.join(self.base_data_dir, "listOfConjuctions.txt"))
        self.set_output_text(curated_txt)
        score = self.check_for_keywords(curated_txt, subject_file)
        y = len(curated_txt.split())
        percentage = (score / y) * 100 if y > 0 else 0
        return percentage

    def sort_and_remove_duplicates_from_file(self, filepath: str):
        print(f"Attempting to open file at: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Sort the lines in alphabetical order and remove duplicates
        lines = sorted(set(line.strip() for line in lines))

        # Write the unique lines back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))

    def curate_text(self, text: str, filepath: str) -> str:
        terms_to_remove = []
        with open(filepath, 'r', encoding='utf-8') as file:
            terms_to_remove = file.read().splitlines()

        # Split the input text into words
        words = text.split()

        # Remove the terms from the words
        curated_words = [word for word in words if word.lower() not in [term.lower() for term in terms_to_remove]]

        return ' '.join(curated_words)

    def get_universities(self) -> List[str]:
        self.list_of_fields.clear()
        university_names = []

        for university in self.university_files:
            filename = os.path.basename(university)
            name, _ = os.path.splitext(filename)
            university_names.append(name.replace('_', ' '))

        return university_names

    def get_faculties(self) -> List[str]:
        faculties = []
        if self.university_index != -1:
            for row in self.list_of_fields:
                if row[1] and row[1] != "null" and row[1] not in faculties:
                    faculties.append(row[1])
        return faculties

    def get_qualifications(self, university_index: int) -> List[str]:
        qualifications = []
        self.list_of_fields.clear()
        if university_index != -1:
            file_path = self.university_files[university_index]
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    for row in reader:
                        self.list_of_fields.append(row)
            except UnicodeDecodeError:
                try:
                    # Retry with another encoding
                    with open(file_path, 'r', encoding='latin1') as file:
                        reader = csv.reader(file, delimiter=';')
                        for row in reader:
                            self.list_of_fields.append(row)
                except Exception as e:
                    # Handle or log the exception if needed
                    print(f"Error reading file {file_path}: {e}")
                    return qualifications

            row_count = 0
            for row in self.list_of_fields:
                if row[2] and row[2] not in ["null", "none", "N/A", "n/a"]:
                    if row[2].upper() not in qualifications:
                        self.qualification_indexes.append(row_count)
                        self.qualification_names.append(row[2].upper())
                        qualifications.append(row[2].upper())
                row_count += 1

        return qualifications

    def get_qualification_percentage(self, qualification_selected: str) -> float:
        self.content = ""
        descriptions = ""
        start_reading = False
        stop_reading = False
        qualification_name = ""
        start_qualification_record = 0
        end_qualification_record = 0
        record_count = 1
        qualification_index = 0

        for qualification in self.qualification_names:
            if qualification == qualification_selected:
                start_qualification_record = self.qualification_indexes[qualification_index]
                try:
                    end_qualification_record = self.qualification_indexes[qualification_index + 1]
                except IndexError:
                    end_qualification_record = len(self.list_of_fields)

            qualification_index += 1

        for record in self.list_of_fields:
            if record_count == start_qualification_record:
                start_reading = True
                qualification_name = record[4]
                if record[7] in ["null", "none", "N/A", "n/a"]:
                    descriptions += " " + qualification_name
                    self.content += " " + qualification_name
            elif record_count == end_qualification_record:
                stop_reading = True
            elif not stop_reading and start_reading:
                descriptions += " " + record[7]
                self.content += " " + record[7]
            record_count += 1

        self.agriculture_score = self.calculate_percentage(descriptions, "Agriculture.txt")
        self.biology_score = self.calculate_percentage(descriptions, "Biology.txt")
        self.chemistry_score = self.calculate_percentage(descriptions, "Chemistry.txt")
        self.maths_and_statistics_score = self.calculate_percentage(descriptions, "Mathematics and Statistics.txt")
        self.physics_score = self.calculate_percentage(descriptions, "Physics.txt")

        return self.calculate_percentage(descriptions, "Combined.txt")

    def other_selected(self, other_qualification_name: str) -> float:
        self.agriculture_score = self.calculate_percentage(other_qualification_name, "Agriculture.txt")
        self.biology_score = self.calculate_percentage(other_qualification_name, "Biology.txt")
        self.chemistry_score = self.calculate_percentage(other_qualification_name, "Chemistry.txt")
        self.maths_and_statistics_score = self.calculate_percentage(other_qualification_name, "Mathematics and Statistics.txt")
        self.physics_score = self.calculate_percentage(other_qualification_name, "Physics.txt")
        return self.calculate_percentage(other_qualification_name, "Combined.txt")

    def calculation_additions(self, nqf_level: int, years_of_experience: int) -> float:
        score_addition = 0
        valid_nqf_levels = {4, 5, 6, 7, 8, 9, 10}
        if nqf_level in valid_nqf_levels:
            score_addition = {4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100}.get(nqf_level, 0)

        if years_of_experience in {1, 2}:
            score_addition += 20
        elif years_of_experience in {3, 4}:
            score_addition += 40
        elif years_of_experience in {5, 6}:
            score_addition += 60
        elif years_of_experience in {7, 8}:
            score_addition += 80
        elif years_of_experience in {9, 10}:
            score_addition += 100
        elif years_of_experience > 10:
            score_addition += 100

        return score_addition

import os
from typing import List
import Levenshtein

class PercentageComputation:
    inputText = ""
    outputText = ""
    universityIndex = 0
    QualificationNames = []
    QualificationIndexes = []
    list_of_fields = []
    UniversityFiles = []
    content = ""

    def __init__(self):
        self.folderWithFiles = ""
        self.agricultureScore = 0
        self.biologyScore = 0
        self.mathsAndStatisticsScore = 0
        self.physicsScore = 0
        self.chemistryScore = 0

    def setInputText(self, text):
        PercentageComputation.inputText = text

    def getOutputText(self):
        return PercentageComputation.outputText

    def setOutputText(self, text):
        PercentageComputation.outputText = text

    def setUniversuty(self, universityFiles):
        PercentageComputation.UniversityFiles = universityFiles

    def setFolderWithFiles(self, folder):
        self.folderWithFiles = folder

    def getQualificationContent(self):
        return PercentageComputation.content

    def checkForKeywords(self, searchText, filePath):
        foundterms = []
        keywords = open(os.path.join(self.folderWithFiles, filePath)).read().splitlines()
        searchWords = searchText.split(' ')

        score = 0
        for word in searchWords:
            foundTerm = False
            for keyword in keywords:
                if not foundTerm and Levenshtein.distance(keyword.lower(), word.lower()) <= 2:
                    score += 1
                    foundTerm = True
        return score

    def CalculatePercentaged(self, inputText, subjectFile):
        self.SortAndRemoveDuplicatesFromFile("listOfConjuctions.txt")
        self.SortAndRemoveDuplicatesFromFile(subjectFile)
        curatedTxt = self.CurateText(inputText, "listOfConjuctions.txt")
        self.setOutputText(curatedTxt)
        x = self.checkForKeywords(curatedTxt, subjectFile)
        y = len(curatedTxt.split(' '))
        score = (float(x) / float(y)) * 100
        return score

    def SortAndRemoveDuplicatesFromFile(self, filepath):
        lines = open(os.path.join(self.folderWithFiles, filepath)).read().splitlines()
        lines = sorted(set(lines))
        with open(os.path.join(self.folderWithFiles, filepath), 'w') as f:
            for line in lines:
                f.write(line + '\n')

    def CurateText(self, text, filepath):
        termsToRemove = open(os.path.join(self.folderWithFiles, filepath)).read().splitlines()
        words = text.split(' ')
        curatedWords = [word for word in words if word.lower() not in (term.lower() for term in termsToRemove)]
        return ' '.join(curatedWords)

    def getUniversities(self):
        self.list_of_fields.clear()
        universityNames = []
        for university in PercentageComputation.UniversityFiles:
            universityNames.append(os.path.splitext(os.path.basename(university))[0].replace('_', ' '))
        return universityNames

    def getFaculties(self):
        faculties = []
        if PercentageComputation.universityIndex != -1:
            for row in self.list_of_fields:
                if row[1] != "null" and row[1] not in faculties:
                    faculties.append(row[1])
        return faculties

    def getQualifications(self, UniversityIndex):
        qualifications = []
        self.list_of_fields.clear()
        if UniversityIndex != -1:
            filePath = PercentageComputation.UniversityFiles[UniversityIndex]
            with open(filePath, 'r') as file:
                for line in file:
                    fields = line.strip().split(';')
                    self.list_of_fields.append(fields)
        rowCount = 0
        for row in self.list_of_fields:
            if row[2] not in ["null", "none", "N/A", "n/a"] and row[2] not in qualifications:
                PercentageComputation.QualificationIndexes.append(rowCount)
                PercentageComputation.QualificationNames.append(row[2].upper())
                qualifications.append(row[2].upper())
            rowCount += 1
        return qualifications

    def getQualificationPercentage(self, QualificationSelected):
        descriptions = ""
        startReading = False
        stopReading = False
        startQualificationRecord = 0
        endQualificationRecord = 0
        recordCount = 1

        for idx, qualification in enumerate(PercentageComputation.QualificationNames):
            if qualification == QualificationSelected:
                startQualificationRecord = PercentageComputation.QualificationIndexes[idx]
                endQualificationRecord = (PercentageComputation.QualificationIndexes[idx + 1]
                                          if idx + 1 < len(PercentageComputation.QualificationIndexes)
                                          else len(self.list_of_fields))
                break

        for record in self.list_of_fields:
            if recordCount == startQualificationRecord:
                startReading = True
                if record[7] not in ["null", "none", "N/A", "n/a"]:
                    descriptions += " " + record[7]
                    PercentageComputation.content += " " + record[7]
            elif recordCount == endQualificationRecord:
                stopReading = True
            elif startReading and not stopReading:
                descriptions += " " + record[7]
                PercentageComputation.content += " " + record[7]
            recordCount += 1

        self.agricultureScore = self.CalculatePercentaged(descriptions, "Agriculture.txt")
        self.biologyScore = self.CalculatePercentaged(descriptions, "Biology.txt")
        self.chemistryScore = self.CalculatePercentaged(descriptions, "Chemistry.txt")
        self.mathsAndStatisticsScore = self.CalculatePercentaged(descriptions, "Mathematics and Statistics.txt")
        self.physicsScore = self.CalculatePercentaged(descriptions, "Physics.txt")

        return self.CalculatePercentaged(descriptions, "Combined.txt")

    def OtherSelected(self, OtherQualificationName):
        self.agricultureScore = self.CalculatePercentaged(OtherQualificationName, "Agriculture.txt")
        self.biologyScore = self.CalculatePercentaged(OtherQualificationName, "Biology.txt")
        self.chemistryScore = self.CalculatePercentaged(OtherQualificationName, "Chemistry.txt")
        self.mathsAndStatisticsScore = self.CalculatePercentaged(OtherQualificationName, "Mathematics and Statistics.txt")
        self.physicsScore = self.CalculatePercentaged(OtherQualificationName, "Physics.txt")
        return self.CalculatePercentaged(OtherQualificationName, "Combined.txt")

    def CalculationAdditions(self, NQFLevel, YearsOfExperience):
        scoreAddition = 0
        if NQFLevel in range(4, 11):
            scoreAddition += 10 * NQFLevel
        if YearsOfExperience > 0:
            scoreAddition += min(10 * (YearsOfExperience // 2), 100)
        return scoreAddition

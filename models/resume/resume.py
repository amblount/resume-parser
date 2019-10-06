from typing import List, Dict
from glom import glom
import pathlib

SECTION_NAMES = [
    "BASICS",
    "WORK",
    "VOLUNTEER",
    "EDUCATION",
    "AWARDS",
    "PUBLICATIONS"
    "PROJECTS",
    "SKILLS",
    "LANGUAGES",
    "INTERESTS",
    "REFERENCES"
]

def load_resumes(filepath: str) -> List:
    """
    load_resumes: Method for ingesting resume files from specified filepath.

    Params:
        - filepath:
    Return:
        - List of Resume files 
    """
    resume_filepath = pathlib.Path(filepath)
    return resume_filepath

class Resume(object):

    def __init__(self, resume:str):
        self.resume = resume
        self.sections: Dict = self.process_pdf(resume, SECTION_NAMES)

    @property 
    def resume_file(self):
        """
        resume_file: Property method to access the original resume file.
        May be useful for testing.
        """
        return self.resume

    @staticmethod
    def process_resume(self, resume: str, structure: List[str]):
        """
        process_pdf: This is the function for processing a resume file. All helper methods
        for extracting different subsections of the resume (extract_education_section) should be 
        called in this method, and the output should be a JSON object.
        """
        pass

    def _preprocess_resume_text():
        """
        Method for pre-processing the overall text of the resume (whitespace, character-case, and 
        non-standard characters)
        """
        pass

    def _get_section_idx():
        pass

    def _extract_education_section(self, resume: str) -> List[Dict]:
        #Method for extracting education information goes here
        education:List = []
         # Logic for looping through skills listed.
        # For each skill in the resume.
        # Pull out the skill in the relevant format, and store it to our list
            education.append({
                "institution": institution,
                "area": area
                "startDate": start_date,
                "endDate": end_date,
                "gpa": gpa
            })
        return education

    def _extract_skills_section(self, resume: str) -> List[Dict]:
        #Method for extracting skill information goes here
        skills:List = []
        # Logic for looping through skills listed.
        # For each skill in the resume.
        # Pull out the skill in the relevant format, and store it to our list
            skills.append({
                "name": name,
                "level": level,
                "keywords": keywords
            })
        
        return skills
        
    
    def anonymize_component(self, component:str):
        """
        anonymize_component: Method for anonymizing different attributes of the resume. This is meant
        for removing important PII from the data.

        component: Attribute of resume that is to be hashed or anonymized in some ways.
        """
        pass

    def access_section(self, section_name:str) -> Dict:
        """
        access_section: Method for accessing a sub-section of the resume.

        """
        return self.sections.get(section_name, "Section does not exist")

    def access_attribute(self, target_name:str):
        """
        Access_attributes: Method for accessing a nested attribute for section
        of the resume.

        Params:
            Target_Name: A pathway string (eg. SectionName.Subsection.Attribute) for a particular attribute
        Return:
            Attribute: The value of the target attribute

        access_attribute("Education.College.Name") >> 'Carnegie Mellon University'
        """
        return glom(self.sections, target_name)

    def export_resume(self):
        return self.sections
    
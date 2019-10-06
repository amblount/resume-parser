from typing import List, Dict
from glom import glom

SECTION_NAMES = [
    "BASICS",
    "WORK",
    "VOLUNTEER",
    "EDUCATION",
    "AWARDS",
    "PROJECTS",
    "SKILLS",
    "REFERENCES"
]



class Resume(object):

    def __init__(self, resume:str):
        self.sections: Dict = self_process_pdf(resume, SECTION_NAMES)

    
    @classmethod
    def _process_pdf(self, resume: str, structure: List[str]):
        #possible multiple submethods heres
        pass

    
    def anonymize_component(self, component:str)
        pass

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

    
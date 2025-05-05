import os
class TemplateParser:
    def __init__(self, language: str,default_language: str = "en"):
        self.language = None
        self.default_language = default_language
        self.current_path= os.path.dirname(os.path.abspath(__file__))

        self.set_language(language=language)
    def set_language(self, language: str):
        if not language:
            self.language = self.default_language
        
        language_path = os.path.join(self.current_path, "locales", language)
        if  os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language


    def get(self,group:str,key:str,vars:dict={}):
        

        if not group or not key:
            return None
        print(f"TemplateParser initialized with current_path: {self.current_path}")

        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")

        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py") 
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None
        
        #import group module
        module=__import__(f"stores.llm.templetes.locales.{targeted_language}.{group}", fromlist=[group])
        if not module:
            return None
        
        key_attrbuite=getattr(module, key).substitute(vars)
        if not key_attrbuite:
            return None
        return key_attrbuite

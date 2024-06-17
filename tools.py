from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import ToolException
from menu_dectection import *
from utlis import preprocess_menu_text,segment_menu_text,clean_dish_names
import os

class Filepath(BaseModel):
    f:str=Field(...,description="Path to the image file")
@tool("OCR tool",args_schema=Filepath)
def extract_menu_info(menu:str)->list[str]:
    "Extract dish names from a menu image"
    inital_menu = information_found(useCamera=False, imgPath=menu)
    process_txt=preprocess_menu_text(inital_menu)
    segment_txt=segment_menu_text(process_txt)
    cleaned_dish_names=clean_dish_names(segment_txt)
    return cleaned_dish_names

class FileSearch(BaseModel):
    file_name:str=Field(...,description="Name of the file to search")

@tool("Find file path",args_schema=FileSearch)
def find_file_path(file_name:str)->str:
    "Find the path of the file"
    search="C:/Users/lucil/Gen-AI-Contest/uploaded_files/"
    for root, dirs, files in os.walk(search):
        if file_name in files: 
            p=os.path.join(root, file_name)
            print()
            return p
    
    
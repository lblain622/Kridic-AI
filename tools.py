from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.tools import ToolException
from menu_dectection import *
from utlis import preprocess_menu_text,segment_menu_text,clean_dish_names

@tool
def extract_dish_names(menu)->list[str]:
    "Extract dish names from a menu image"
    inital_menu = information_found(useCamera=False, imgPath=menu)
    process_txt=preprocess_menu_text(inital_menu)
    segment_txt=segment_menu_text(process_txt)
    cleaned_dish_names=clean_dish_names(segment_txt)
    return cleaned_dish_names
from aiogram.filters.callback_data import CallbackData

class Switcher(CallbackData, prefix = "ABC"):
    page: int
    side: str

class SwitchProject(CallbackData, prefix= "switch_project"):
    page: int
    side: str
    
class SwitchChatsProject(CallbackData, prefix= "switch_chat_project"):
    page: int
    side: str
    
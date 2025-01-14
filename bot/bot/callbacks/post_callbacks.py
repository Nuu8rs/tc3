from aiogram.filters.callback_data import CallbackData

class SendPostToProject(CallbackData, prefix = "send_post"):
    post_id: int
    project_id: int
    
class DeletePostProject(CallbackData, prefix = "delete_post"):
    post_id: int
    project_id: int
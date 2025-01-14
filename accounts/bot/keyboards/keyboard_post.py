from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from accounts.bot.callbacks.callbacks_post import SendPostToProject, DeletePostProject

def select_options_for_post(post_id: int, project_id: int) -> InlineKeyboardMarkup:
    return (
        InlineKeyboardBuilder()
        .button(
            text = "✅ Опубликовать пост", 
            callback_data=SendPostToProject(
                    post_id=post_id,
                    project_id=project_id
                                            )
                )
        .button(
            text = "❌ Удалить пост",
            callback_data=DeletePostProject(
                post_id=post_id,
                project_id=project_id
            )
        )
        .adjust(1)
        .as_markup()
    )
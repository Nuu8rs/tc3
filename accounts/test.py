# import re
# import emoji

# html_text = '''<strong>⚡️</strong><strong>YouTube ожил и на компах у части пользователей</strong>: юзеры сообщают, что видосы загружаются даже в 4K без плагинов и VPN.

# Бегом проверять.

# 🕹🥰✅❌🥰☹️❌<a href="https://t.me/+6fyKjmOWmW5lYzMy">КиберТопор — Подписаться</a>'''

# def remove_trailing_emojis_and_link(text):
#     TEMPLATE_delete_cta = r'\s*<a href="[^"]*">.*?</a>$'
    
#     text_split_line = text.split("\n")
#     last_line_no_emj = emoji.replace_emoji(text_split_line[-1], replace='')
#     text_split_line[-1] = last_line_no_emj
#     text = "\n".join(text_split_line)
    
#     cleaned_text = re.sub(TEMPLATE_delete_cta, '', text)
#     return cleaned_text
    

# cleaned_text = remove_trailing_emojis_and_link(html_text)
# print(cleaned_text)
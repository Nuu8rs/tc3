import re
import emoji

def delete_cta_link(text: str) -> str:
    TEMPLATE_delete_cta = r'\s*<a href="[^"]*">.*?</a>$'
    
    text_split_line = text.split("\n")
    if len(text_split_line) == 1:
        return text
    last_line_no_emj = emoji.replace_emoji(text_split_line[-1], replace='')
    text_split_line[-1] = last_line_no_emj
    text = "\n".join(text_split_line)
    
    cleaned_text = re.sub(TEMPLATE_delete_cta, '', text)
    return cleaned_text
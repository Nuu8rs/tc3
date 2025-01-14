from fastapi.templating import Jinja2Templates

from app.components.jinja2.filters import format_datetime, format_media, post_status, format_html, format_html_news_feed, replace_to_br_tag


class CustomJinja(Jinja2Templates):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.env.filters['format_datetime'] = format_datetime
        self.env.filters['format_html'] = format_html
        self.env.filters['format_html_news_feed'] = format_html_news_feed
        self.env.filters['format_media'] = format_media
        self.env.filters['post_status'] = post_status 
        self.env.filters['replace_to_br_tag'] = replace_to_br_tag 
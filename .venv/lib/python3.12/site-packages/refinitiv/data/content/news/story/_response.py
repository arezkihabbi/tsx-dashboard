from ....delivery._data._response import Response


class NewsStoryResponse(Response):
    def __str__(self):
        if self.data.raw:
            return (
                self.data.raw.get("newsItem", {}).get("contentSet", {}).get("inlineData", [{}])[0].get("$")
                or self.data.story.content.text
            )
        else:
            return f"{self.errors}"

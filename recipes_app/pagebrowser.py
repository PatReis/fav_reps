import math


class PageBrowser:

    def __init__(self, total_items: int, items_per_page: int):
        self.total_items = int(total_items)
        self.items_per_page = int(max(items_per_page, 1))
        self.number_of_pages = int(math.ceil(total_items/items_per_page))

    def valid_page(self, page_index: int):
        if self.number_of_pages <= 0:
            return 0
        return min(max(0, page_index), self.number_of_pages - 1)

    def get_items_for_page(self, list_of_items, page_index: int):
        if self.number_of_pages <= 0:
            return []
        return list_of_items[page_index*self.items_per_page:(page_index+1)*self.items_per_page]

    def make_page_browser(self, page_index: int, number_page_choices: int = 10):
        """
        For a django template like the example below. The number is displayed from 1...N using the 'add:"1"' filter
        but the page indices range from 0...N-1.

        ```html
        <form method="GET" action="{% url 'home' %}">

            {% if page_browser_show_back is not None %}
                <button type="submit" name="pgNr" value="{{page_browser_show_back}}">&larr; Back</button>
            {% endif %}
            {% if page_browser_show_start is not None %}
                <button type="submit" name="pgNr" value="{{page_browser_show_start}}">{{page_browser_show_start|add:"1"}}</button>
            {% endif %}
            {% if page_browser_show_start_dots %}
                ...
            {% endif %}
            {% for i in page_browser_choices_down %}
                <button type="submit" name="pgNr" value="{{i}}">{{i|add:"1"}}</button>
            {% endfor %}
            {{page_browser_current_index|add:"1"}}
            {% for i in page_browser_choices_up %}
                <button type="submit" name="pgNr" value="{{i}}">{{i|add:"1"}}</button>
            {% endfor %}
            {% if page_browser_show_stop_dots %}
                ...
            {% endif %}
            {% if page_browser_show_stop is not None %}
                <button type="submit" name="pgNr" value="{{page_browser_show_stop}}">{{page_browser_show_stop|add:"1"}}</button>
            {% endif %}
            {% if page_browser_show_next is not None %}
                <button type="submit" name="pgNr" value="{{page_browser_show_next}}">Next &rarr;</button>
            {% endif %}

            <!-- Hidden input... -->
        </form>
        ```

        """

        page_index = self.valid_page(page_index)
        number_page_choices = max(number_page_choices, 0)

        context = {
            "page_browser_max_number_pages": int(self.number_of_pages),
            "page_browser_current_index": page_index,
            "page_browser_show_start": None,
            "page_browser_show_start_dots": None,
            "page_browser_show_stop": None,
            "page_browser_show_stop_dots": None,
        }

        show_back = True if page_index > 0 else False
        show_next = False if page_index >= self.number_of_pages - 1 else True
        context.update({
            "page_browser_show_back": page_index - 1 if show_back else None,
            "page_browser_show_next": page_index + 1 if show_next else None,
        })

        avg_left = int(number_page_choices/2)
        avg_right = number_page_choices - avg_left
        b_right = page_index + avg_right
        b_left = page_index - avg_left

        if (b_left >= 0) and (b_right < self.number_of_pages):
            # page_choices = [i for i in range(b_left, b_right)]
            page_choices_down = [i for i in range(b_left, page_index)]
            page_choices_up = [i for i in range(page_index+1, b_right)]

        elif (b_left < 0) and (b_right < self.number_of_pages):
            # page_choices = [i for i in range(0, min(self.number_of_pages, number_page_choices))]
            page_choices_down = [i for i in range(0, page_index)]
            page_choices_up = [i for i in range(page_index+1, min(self.number_of_pages, number_page_choices))]

        elif (b_left >= 0) and (b_right >= self.number_of_pages):
            # page_choices = [i for i in range(
            #     max(0, self.number_of_pages - number_page_choices), self.number_of_pages
            # )]
            page_choices_down = [i for i in range(
                max(0, self.number_of_pages - number_page_choices), page_index
            )]
            page_choices_up = [i for i in range(
                page_index+1, self.number_of_pages
            )]
        else:
            # page_choices = [i for i in range(0, self.number_of_pages)]
            page_choices_down = [i for i in range(0, page_index)]
            page_choices_up = [i for i in range(page_index+1, self.number_of_pages)]

        page_choices = page_choices_down + [page_index] + page_choices_up

        context.update({
            "page_browser_choices": page_choices,
            "page_browser_choices_up": page_choices_up,
            "page_browser_choices_down": page_choices_down
        })

        if self.number_of_pages > 0:
            if page_choices[0] > 0:
                context["page_browser_show_start"] = 0
            if page_choices[-1] < self.number_of_pages-1:
                context["page_browser_show_stop"] = self.number_of_pages-1
            if page_choices[0] > 1:
                context["page_browser_show_start_dots"] = True
            if page_choices[-1] < self.number_of_pages-2:
                context["page_browser_show_stop_dots"] = True
        return context


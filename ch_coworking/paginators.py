from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator


class ESPaginator(Paginator):
    """
    A better paginator for search results

    The normal Paginator does a .count() query and then a slice. Since ES
    results contain the total number of results, we can take an optimistic
    slice and then adjust the count.
    """

    def validate_number(self, number):
        """
        Validates the given 1-based page number.

        This class overrides the default behavior and ignores the upper bound.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a page object.

        This class overrides the default behavior and ignores "orphans" and
        assigns the count from the ES result to the Paginator.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        page = Page(self.object_list[bottom:top], number, self)

        # Force the search to evaluate and then attach the count. We want to
        # avoid an extra useless query even if there are no results, so we
        # directly fetch the count from hits.
        # Overwrite `object_list` with the list of ES results.
        ex = page.object_list.execute()

        page.object_list = ex.hits
        # Update the `_count`.
        self._count = ex.hits.total

        return page

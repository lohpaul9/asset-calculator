import logging
from ..baseentries.atdate import *


class SortedByDate:
    def __init__(self, entries: list[Dated]):
        """
        creates a list of entries sorted by date
        :param stock_entries: unsorted list of dated entries
        """
        self.sorted = entries
        self.sorted.sort(key=lambda entry: entry.rounded_date())

    # To-Do refactor for BST
    def add_entry(self, entry):
        """
        Add single entry to time-sorted list
        :param entry: dated entry
        :return: NIL
        """
        if len(self.sorted) == 0:
            self.sorted.append(entry)
            return

        for i in range(len(self.sorted)):
            if (entry.rounded_date() < self.sorted[i].rounded_date()):
                self.sorted.insert(i, entry)
                break
            if (i == len(self.sorted) - 1):
                self.sorted.append(entry)

    def entries_by_date(self, date) -> list[Dated]:
        """
`       Generates a list of entries by EOD of date given
        :param date: datetime.date Obj
        :return: sorted list of dated entries
        """
        for i in range(len(self.sorted)):
            b = date < self.sorted[i].rounded_date()
            if b:
                logging.debug(f"returning the following dated entries: {[entry for entry in self.sorted[:i]]}")
                return (self.sorted[:i])
        logging.debug(f"returning the following dated entries: {[entry for entry in self.sorted]}")
        return self.sorted.copy()

    def entries_between_dates(self, date_bef: datetime, date_after: datetime) -> list[Dated]:
        """
        returns all stock entries between earlier date EOD (ie next day)
        and later date EOD

        :param date_bef:  earlier date
        :param date_after:  later date
        """
        if date_bef > date_after:
            raise ValueError

        set_start = False
        start = 0
        end = len(self.sorted)

        for i, stockEntry in enumerate(self.sorted):
            # Exclusive of before date
            if (date_bef < stockEntry.date and not set_start):
                start = i
                set_start = True
            # Inclusive of after date
            if (date_after < stockEntry.date):
                end = i
                break
        return self.sorted[start:end]

    def all_entries(self):
        return self.sorted.copy()

    def __repr__(self):
        str_rep = f"SortedByDate\n{self.sorted}"
        return str_rep

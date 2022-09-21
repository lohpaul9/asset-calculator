import logging
from .timesorted import SortedByDate
from ..baseentries.atdate import OwnedCashAtDate
from datetime import datetime

class OwnedCashHistory(SortedByDate) :
    def __init__(self, cash_entries: list[OwnedCashAtDate]):
        super().__init__(cash_entries)

    def cash_owned_at_date(self, date:datetime) -> OwnedCashAtDate:
        """
        returns owned cash at given date EOD
        :param given date
        :return: single OwnedCashAtDate obj
        """
        cashEntries = self.entries_by_date(date)
        totalEntries = len(cashEntries)
        # If no values before date, we are going too far back in time
        # Consider - returning no cash instead
        if totalEntries == 0:
            logging.error(f"No cash entry found before {date.strftime('%m/%d/%Y')}")
            return OwnedCashAtDate(date, {})
        # Return the most updated value
        most_updated = cashEntries[totalEntries - 1]
        return most_updated

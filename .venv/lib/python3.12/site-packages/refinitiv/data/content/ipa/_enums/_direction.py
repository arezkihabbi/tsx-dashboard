from enum import unique

from ...._base_enum import StrEnum


@unique
class Direction(StrEnum):
    """
    - 'Paid' (the cash flows of the leg are paid to the counterparty),
    - 'Received' (the cash flows of the leg are received from the counterparty).
      Optional for a single leg instrument (like a bond), in that case default value
      is Received. It is mandatory for a multi-instrument leg instrument (like Swap
      or CDS leg).
    """

    PAID = "Paid"
    RECEIVED = "Received"

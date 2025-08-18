from typing import Optional, List

from ._butterfly_shift import ButterflyShift
from ._combined_shift import CombinedShift
from ._flattening_shift import FlatteningShift
from ._long_end_shift import LongEndShift
from ._parallel_shift import ParallelShift
from ._short_end_shift import ShortEndShift
from ._time_bucket_shift import TimeBucketShift
from ._twist_shift import TwistShift
from ...._object_definition import ObjectDefinition
from ......_tools import try_copy_to_list


class ShiftDefinition(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    butterfly_shift : ButterflyShift, optional
        The definition of attributes for butterfly shift scenario. the start and end
        curve points are shifted by amount. the curve point at pivot tenor is not
        shifted.
    combined_shifts : list of CombinedShift, optional
        The definition of attributes for combined shifts scenario. each element of the
        combined shifts scenario describes separate shift scenario applied to curve
        points. if one scenario follows the other, they are added to each other.
    flattening_shift : FlatteningShift, optional
        The definition of attributes for flattening / steepening shift scenario. the
        start curve point is shifted by [amount / 2], the end curve point is shifted by
        [-amount / 2].
    long_end_shift : LongEndShift, optional
        The definition of attributes for long end shift scenario. the end curve point is
        shifted by amount. the start curve point is not shifted. the shift rises from 0
        to amount between the start and the end curve point.
    parallel_shift : ParallelShift, optional
        The definition of attributes for parallel shift scenario. each curve point is
        shifted by amount.
    short_end_shift : ShortEndShift, optional
        The definition of attributes for short end shift scenario. the start curve point
        is shifted by amount. the end curve point is not shifted. the shift decreases
        from 0 to amount between the start and the end curve point
    time_bucket_shifts : list of TimeBucketShift, optional
        The definition of attributes for time bucket shift scenario. each element of
        timebucketshifts describes the separate parallel shift. this shift applies from
        starttenor to endtenor.
    twist_shift : TwistShift, optional
        The definition of attributes for twist shift scenario. the start and end curve
        points are shifted by amount. the curve point at pivot tenor is not shifted.
    """

    def __init__(
        self,
        butterfly_shift: Optional[ButterflyShift] = None,
        combined_shifts: Optional[List[CombinedShift]] = None,
        flattening_shift: Optional[FlatteningShift] = None,
        long_end_shift: Optional[LongEndShift] = None,
        parallel_shift: Optional[ParallelShift] = None,
        short_end_shift: Optional[ShortEndShift] = None,
        time_bucket_shifts: Optional[List[TimeBucketShift]] = None,
        twist_shift: Optional[TwistShift] = None,
    ) -> None:
        super().__init__()
        self.butterfly_shift = butterfly_shift
        self.combined_shifts = try_copy_to_list(combined_shifts)
        self.flattening_shift = flattening_shift
        self.long_end_shift = long_end_shift
        self.parallel_shift = parallel_shift
        self.short_end_shift = short_end_shift
        self.time_bucket_shifts = try_copy_to_list(time_bucket_shifts)
        self.twist_shift = twist_shift

    @property
    def butterfly_shift(self):
        """
        The definition of attributes for butterfly shift scenario. the start and end
        curve points are shifted by amount. the curve point at pivot tenor is not
        shifted.
        :return: object ButterflyShift
        """
        return self._get_object_parameter(ButterflyShift, "butterflyShift")

    @butterfly_shift.setter
    def butterfly_shift(self, value):
        self._set_object_parameter(ButterflyShift, "butterflyShift", value)

    @property
    def combined_shifts(self):
        """
        The definition of attributes for combined shifts scenario. each element of the
        combined shifts scenario describes separate shift scenario applied to curve
        points. if one scenario follows the other, they are added to each other.
        :return: list CombinedShift
        """
        return self._get_list_parameter(CombinedShift, "combinedShifts")

    @combined_shifts.setter
    def combined_shifts(self, value):
        self._set_list_parameter(CombinedShift, "combinedShifts", value)

    @property
    def flattening_shift(self):
        """
        The definition of attributes for flattening / steepening shift scenario. the
        start curve point is shifted by [amount / 2], the end curve point is shifted by
        [-amount / 2].
        :return: object FlatteningShift
        """
        return self._get_object_parameter(FlatteningShift, "flatteningShift")

    @flattening_shift.setter
    def flattening_shift(self, value):
        self._set_object_parameter(FlatteningShift, "flatteningShift", value)

    @property
    def long_end_shift(self):
        """
        The definition of attributes for long end shift scenario. the end curve point is
        shifted by amount. the start curve point is not shifted. the shift rises from 0
        to amount between the start and the end curve point.
        :return: object LongEndShift
        """
        return self._get_object_parameter(LongEndShift, "longEndShift")

    @long_end_shift.setter
    def long_end_shift(self, value):
        self._set_object_parameter(LongEndShift, "longEndShift", value)

    @property
    def parallel_shift(self):
        """
        The definition of attributes for parallel shift scenario. each curve point is
        shifted by amount.
        :return: object ParallelShift
        """
        return self._get_object_parameter(ParallelShift, "parallelShift")

    @parallel_shift.setter
    def parallel_shift(self, value):
        self._set_object_parameter(ParallelShift, "parallelShift", value)

    @property
    def short_end_shift(self):
        """
        The definition of attributes for short end shift scenario. the start curve point
        is shifted by amount. the end curve point is not shifted. the shift decreases
        from 0 to amount between the start and the end curve point
        :return: object ShortEndShift
        """
        return self._get_object_parameter(ShortEndShift, "shortEndShift")

    @short_end_shift.setter
    def short_end_shift(self, value):
        self._set_object_parameter(ShortEndShift, "shortEndShift", value)

    @property
    def time_bucket_shifts(self):
        """
        The definition of attributes for time bucket shift scenario. each element of
        timebucketshifts describes the separate parallel shift. this shift applies from
        starttenor to endtenor.
        :return: list TimeBucketShift
        """
        return self._get_list_parameter(TimeBucketShift, "timeBucketShifts")

    @time_bucket_shifts.setter
    def time_bucket_shifts(self, value):
        self._set_list_parameter(TimeBucketShift, "timeBucketShifts", value)

    @property
    def twist_shift(self):
        """
        The definition of attributes for twist shift scenario. the start and end curve
        points are shifted by amount. the curve point at pivot tenor is not shifted.
        :return: object TwistShift
        """
        return self._get_object_parameter(TwistShift, "twistShift")

    @twist_shift.setter
    def twist_shift(self, value):
        self._set_object_parameter(TwistShift, "twistShift", value)

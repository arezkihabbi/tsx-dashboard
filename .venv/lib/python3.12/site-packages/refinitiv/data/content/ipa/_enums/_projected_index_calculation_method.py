from enum import unique
from ...._base_enum import StrEnum


@unique
class ProjectedIndexCalculationMethod(StrEnum):
    CONSTANT_COUPON_PAYMENT = "ConstantCouponPayment"
    CONSTANT_INDEX = "ConstantIndex"
    FORWARD_INDEX = "ForwardIndex"

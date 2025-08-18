from typing import Optional

from ..._param_item import param_item
from ..._serializable import Serializable


class RepoParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    coupon_paid_at_horizon : bool, optional
        Flag that defines whether coupons paid at horizon.  this has no impact on
        pricing.
    haircut_rate_percent : float, optional
        The reduction applied to the value of an underlying asset for purposes of
        calculating a repo collateral. the value is computed as [(initialmarginpercent -
        100) / initialmarginpercent] and expressed in percentages. either haircut or
        initial marging field can be bet. optional. by default it is computed from
        initialmarginpercent.
    initial_margin_percent : float, optional
        The initial market value of collateral expressed as a percentage of the purchase
        price of the underlying asset. either haircutratepercent or initialmarginpercent
        can be overriden. optional. default value is 100.
    purchase_price : float, optional
        Purchase price of the asset. this parameter can be used to solve repurchaseprice
        from this purchaseprice value. optional. by default it is computed from net
        present value and initial margin.
    repurchase_price : float, optional
        Repurchase price of the asset. this parameter can be used to solve purchaseprice
        from this repurchaseprice value. optional. by default it is computed from
        underlying end price, or solved from purchaseprice and repo rate.
    """

    def __init__(
        self,
        coupon_paid_at_horizon: Optional[bool] = None,
        haircut_rate_percent: Optional[float] = None,
        initial_margin_percent: Optional[float] = None,
        purchase_price: Optional[float] = None,
        repurchase_price: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.coupon_paid_at_horizon = coupon_paid_at_horizon
        self.haircut_rate_percent = haircut_rate_percent
        self.initial_margin_percent = initial_margin_percent
        self.purchase_price = purchase_price
        self.repurchase_price = repurchase_price

    def _get_items(self):
        return [
            param_item.to_kv("couponPaidAtHorizon", self.coupon_paid_at_horizon),
            param_item.to_kv("haircutRatePercent", self.haircut_rate_percent),
            param_item.to_kv("initialMarginPercent", self.initial_margin_percent),
            param_item.to_kv("purchasePrice", self.purchase_price),
            param_item.to_kv("repurchasePrice", self.repurchase_price),
        ]

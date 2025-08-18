from ._history_df_builder import HistoryDFBuilder
from .context_collection import RDPMixin, UDFMixin
from ..content.fundamental_and_reference._data_grid_type import DataGridType


class HistoryDFBuilderRDP(RDPMixin, HistoryDFBuilder):
    pass


class HistoryDFBuilderUDF(UDFMixin, HistoryDFBuilder):
    pass


df_builder_by_data_grid_type = {
    DataGridType.UDF: HistoryDFBuilderUDF(),
    DataGridType.RDP: HistoryDFBuilderRDP(),
}


def get_history_df_builder(data_grid_type: "DataGridType") -> "HistoryDFBuilder":
    df_builder = df_builder_by_data_grid_type.get(data_grid_type)

    if not df_builder:
        raise TypeError(f"Unexpected platform type. Type: {data_grid_type}")

    return df_builder

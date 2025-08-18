from dataclasses import dataclass
from typing import Union, TYPE_CHECKING, Dict

from ._properties import Properties
from ._property_type import PropertyType

if TYPE_CHECKING:
    from ._property import Property
    from pandas import DataFrame


@dataclass
class SearchPropertyExplorerResponse:
    """
    Response object that has stores requested properties data.
    """

    hits_count: int
    properties: Dict[str, "Property"]
    df: "DataFrame"
    navigators: "DataFrame"

    def get_by_name(self, name: str) -> Properties:
        """
        Browse the properties names that have relative match with specified query. Results are represented
        as the dataframe and dict of objects.

        Parameters
        ----------
        name: str
            String to specify expected properties data.

        Returns
        -------
            Properties

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> active = santander_bonds.get_properties_object("active")
        """
        return Properties(df=self.get_properties_df(name), properties=self.get_properties_object(name))

    def get_properties_object(self, name: Union[str, bool, int]) -> Dict[str, "Property"]:
        """
        Browse the properties names that have relative match with specified query. Results are represented
        as dict of objects.

        Parameters
        ----------
        name: Union[str, bool, int]
            Argument to specify expected properties data.

        Returns
        -------
            dict of Property objects

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> active = santander_bonds.get_properties_object("active")
        """
        name = str(name).lower()
        return {
            prop_name: prop_value for prop_name, prop_value in self.properties.items() if name in str(prop_name).lower()
        }

    def get_properties_df(self, name: str) -> "DataFrame":
        """
        Browse the properties names that have relative match with specified query.

        Parameters
        ----------
        name: str
            String to specify expected properties data.

        Returns
        -------
            pd.DataFrame

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> active = santander_bonds.get_properties_df("active")
        """
        return self.df.loc[self.df.Property.str.contains(name.replace(" ", ""), na=False, case=False)]

    def get_by_type(self, property_type: Union[str, PropertyType]) -> Properties:
        """
        Browse the types that match the specified query. Results are represented as the dataframe and dict of objects.

        Parameters
        ----------
        property_type: str, PropertyType
            Argument to specify expected properties data.

        Returns
        -------
            Properties

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> str_properties = santander_bonds.get_by_type(PropertyType.String)
        """
        return Properties(
            df=self.df.loc[self.df.Type.str.contains(property_type, na=False, case=False)],
            properties={
                prop_name: prop_value
                for prop_name, prop_value in self.properties.items()
                if str(prop_value.type) == property_type
            },
        )

    def get_by_value(self, value: Union[str, bool, int]) -> Properties:
        """
        Browse the properties example values that match the specified query. Results are represented
        as the dataframe and dict of objects.

        Parameters
        ----------
        value: str, bool, int
            Argument to specify expected properties data.

        Returns
        -------
            Properties

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> active = santander_bonds.get_by_value("active")
        """
        if isinstance(value, bool):
            value = str(value)
            result = self.get_by_type(PropertyType.Boolean)
            df = result.df
            properties = Properties(
                df=df[df["Example Value"] == value],
                properties={
                    prop_name: prop_value
                    for prop_name, prop_value in result.properties.items()
                    if prop_value.value == value
                },
            )

        elif isinstance(value, str) or isinstance(value, int):
            value = str(value)
            lower = str.lower
            value_lower = value.lower()
            properties = Properties(
                df=self.df.loc[self.df["Example Value"].str.contains(value, na=False, case=False)],
                properties={
                    prop_name: prop_value
                    for prop_name, prop_value in self.properties.items()
                    if value_lower in lower(prop_value.value)
                },
            )

        else:
            raise ValueError("Invalid data type. Please provide number, boolean or string.")

        return properties

    def get_navigable(self, prop: str = None) -> "Properties":
        """
        Browse all navigable properties, narrow down results by specifying name of navigable property. Results are
        represented as the dataframe and dict of objects.

        Parameters
        ----------
        prop: str
            String to specify expected properties data.

        Returns
        -------
            Properties

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> from refinitiv.data.content import search
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))",
        ... )
        >>> navigable = santander_bonds.get_navigable()
        """
        if prop is None:
            properties = self.properties

        else:
            properties = self.get_properties_object(prop)

        df = self.df.loc[self.df["Navigable"] == "True"]
        if prop:
            df = df.loc[df.Property.str.contains(prop, na=False, case=False)]

        return Properties(
            df=df,
            properties={
                prop_name: prop_value for prop_name, prop_value in properties.items() if prop_value.navigable is True
            },
        )

import json

from . import _json_requests as json_requests
from ._tools import is_string_type, get_default_session, convert_content_data_to_df_udf, to_datetime

News_Headlines_UDF_endpoint = "News_Headlines"
News_Story_UDF_endpoint = "News_Story"


def get_news_headlines(
    query=None,
    count=10,
    repository="NewsWire",
    date_from=None,
    date_to=None,
    raw_output=False,
    debug=False,
):
    """
    Returns a list of news headlines

    Parameters
    ----------
    query: string, optional
        News headlines search criteria.
        The text can contain RIC codes, company names, country names and
        operators (AND, OR, NOT, IN, parentheses and quotes for explicit search…).

        Tip: Append 'R:' in front of RIC names to improve performance.

        Default: Top News written in English

    count: int, optional
        Max number of headlines retrieved.
        Value Range: [1-100].
        Default: 10

    repository: string, list of strings, optional
        Possible values:
            - "NewsWire"
            - "NewsRoom"
            - "WebNews"
        For "NewsRoom" and "WebNews" repositories a query must be defined.

    date_from: string or datetime, optional
        Beginning of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    date_to: string or datetime, optional
        End of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    raw_output: boolean, optional
        Set this parameter to True to get the data in json format
        if set to False, the legacy will return a data frame
        Default: False

    debug: boolean, optional
        When set to True, the json request and response are printed.
        Default: False

    Returns
    -------
    pandas.DataFrame
        Returns a DataFrame of news headlines with the following columns:

        - Index               : Timestamp of the publication time
        - version_created     : Date of the latest update on the news
        - text                : Text of the Headline
        - story_id            : Identifier to be used to retrieve the full story using the get_news_story legacy
        - source_code         : Second news identifier

    Raises
    ----------
    Exception
        If http request fails or if server returns an error
    AttributeError
        If a parameter type is wrong

    Examples
    --------
    >> import refinitiv.data as ek
    >> ek.set_app_key('set your app id here')
    >> headlines = ek.get_news_headlines("R:MSFT.O", 2)
    >> headlines
                                    versionCreated                                              text \
    2016-04-13 18:28:57.000 2.016-04-13 18:28:59.001 RBC Applies Blockchain as a Loyalty Boost<MSFT...
    2016-04-13 17:28:21.577 2016-04-13 17:28:21.671 UPDATE 2-Long-stalled email privacy bill advan...
                                                                    storyId
    2016-04-13 18:28:57.000    urn:newsml:reuters.com:20160413:nNRA1uxh03:1
    2016-04-13 17:28:21.577    urn:newsml:reuters.com:20160413:nL2N17G16Q:2

    >> headlines = ek.get_news_headlines("R:MSFT.O IN FRANCE")
    >> headlines = ek.get_news_headlines("R:MSFT.O IN FRANCE IN ENGLISH", count=5)
    >> headlines = ek.get_news_headlines("OBA* OR CLINTON IN ENGLISH", count=5)
    """
    logger = get_default_session().logger()

    if query is None:
        query = "Topic:TOPALL and Language:LEN"

    # check parameters type and values
    if not is_string_type(query):
        error_msg = "query must be a string"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # query string must be formated as a "" string containing '' substrings
    #   (and not a '' string containing "" substrings)
    query = query.replace('"', "'")

    # validate query JSON format
    test_query = '{"query":"' + query + '"}'
    try:
        json.loads(str(test_query))
    except ValueError as error:
        error_msg = "query {} has invalid format. {}".format(test_query, str(error))
        logger.debug(error_msg)
        raise ValueError(error_msg)

    if type(count) is not int:
        error_msg = "count must be an integer"
        logger.error(error_msg)
        raise ValueError(error_msg)
    elif count < 0:
        error_msg = "count must be equal or greater than 0"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if isinstance(repository, list):
        repository = ",".join(repository)
    if not isinstance(repository, str):
        error_msg = "repository must be a string or a list of strings"
        raise ValueError(error_msg)

    # build the payload
    app_key = get_default_session().app_key
    payload = {
        "number": str(count),
        "query": query,
        "repository": repository,
        "productName": app_key,
        "attributionCode": "",
    }

    if date_from is not None:
        payload.update({"dateFrom": to_datetime(date_from).isoformat()})

    if date_to is not None:
        payload.update({"dateTo": to_datetime(date_to).isoformat()})

    response = json_requests.send_json_request(News_Headlines_UDF_endpoint, payload, debug=debug)
    result = response.json()

    if raw_output:
        return result
    else:
        return convert_content_data_to_df_udf(result)


def get_news_story(story_id, raw_output=False, debug=False):
    """
    Return a single news story corresponding to the identifier provided in story_id

    Parameters
    ----------
    story_id:  The story id. The story id is a field you will find in every headline you retrieved
        with the legacy get_news_headlines

    raw_output: boolean
        Set this parameter to True to get the data in json format
        if set to False, the legacy will return returns the story content
        The default value is False

    debug: bool
        When set to True, the json request and response are printed.

    Raises
    ------
    Exception
        If http request fails or if Refinitiv Services return an error
    ValueError
        If a parameter type or value is wrong

    Examples
    --------
    >> import refinitiv.data as ek
    >> ek.set_app_key('set your app key here')
    >> headlines = ek.get_news_headlines('IBM')
    >> for index, headline_row in headlines.iterrows():
           story = ek.get_news_story(headline_row['storyId'])
           print (story)
    """
    logger = get_default_session().logger()

    # check parameters type and values
    if not is_string_type(story_id):
        error_msg = "story_id must be a string"
        logger.error(error_msg)
        raise ValueError(error_msg)

    app_key = get_default_session().app_key
    payload = {"attributionCode": "", "productName": app_key, "storyId": story_id}
    response = json_requests.send_json_request(News_Story_UDF_endpoint, payload, debug=debug)
    json_data = response.json()
    if raw_output:
        return json_data

    if json_data:
        if json_data.get("story"):
            if json_data.get("story").get("storyHtml"):
                return json_data.get("story").get("storyHtml")
            else:
                return None
        elif json_data.get("viewURL"):
            return json_data.get("viewURL")
        elif json_data.get("webURL"):
            return json_data.get("webURL")

    return None

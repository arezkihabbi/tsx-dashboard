import threading
from concurrent.futures import ThreadPoolExecutor, wait
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from ..._content_type import ContentType
    from ._stream_factory import StreamDetails
    from .._stream import StreamConnection
    from ..._core.session import Session

StreamConnections = List["StreamConnection"]


class CacheItem:
    def __init__(self, cxn: "StreamConnection", details: "StreamDetails", owner: dict) -> None:
        self.api_config_key = details.api_config_key
        self.owner = owner
        self.cxn: "StreamConnection" = cxn
        self.number_in_use = 0

        session_listeners = cxn.session._listeners
        cxn_events = cxn.events
        cxn_events.on_connecting(session_listeners.connecting)
        cxn_events.on_connected(session_listeners.connected)
        cxn_events.on_disconnected(session_listeners.disconnected)
        cxn_events.on_reconnecting(session_listeners.reconnecting)
        cxn_events.on_login_success(session_listeners.login_success)
        cxn_events.on_login_fail(session_listeners.login_fail)

    @property
    def is_using(self):
        return self.number_in_use > 0

    def inc_use(self):
        self.number_in_use += 1

    def dec_use(self):
        if self.number_in_use == 0:
            raise ValueError(f"CacheItem: number_in_use cannot be less 0, cxn={self.cxn.state}")

        self.number_in_use -= 1

        if self.number_in_use == 0 and (self.cxn.is_disconnecting or self.cxn.is_disposed):
            self.dispose()

    def dispose(self):
        self.number_in_use = -1
        self.owner.pop(self.api_config_key, None)
        self.api_config_key = None
        self.owner = None

        session_listeners = self.cxn.session._listeners
        cxn = self.cxn
        if not cxn.is_disposed:
            cxn_events = cxn.events
            cxn_events.off_connecting(session_listeners.connecting)
            cxn_events.off_connected(session_listeners.connected)
            cxn_events.off_disconnected(session_listeners.disconnected)
            cxn_events.off_reconnecting(session_listeners.reconnecting)
            cxn_events.off_login_success(session_listeners.login_success)
            cxn_events.off_login_fail(session_listeners.login_fail)
            cxn.dispose()

        try:
            cxn.join(5)
        except RuntimeError:
            # silently
            pass

        self.cxn = None

    def __str__(self) -> str:
        if self.cxn:
            name = self.cxn.name
        else:
            name = "disposed"
        return f"CacheItem(cxn={name}, number_in_use={self.number_in_use})"


class StreamCxnCache(object):
    def __init__(self) -> None:
        self._cache: Dict["Session", Dict[str, CacheItem]] = {}
        self._lock = threading.Lock()
        self.cxn_created = threading.Event()

    def has_cxn(self, session: "Session", details: "StreamDetails") -> bool:
        item = self._cache.get(session, {}).get(details.api_config_key)
        return bool(item)

    def get_cxn(self, session: "Session", details: "StreamDetails") -> "StreamConnection":
        with self._lock:
            content_type = details.content_type
            protocol_type = details.protocol_type

            is_debug = session._is_debug()
            if not self.has_cxn(session, details):
                from ._stream_factory import create_stream_cxn

                self.cxn_created.clear()

                cxn = create_stream_cxn(details, session)
                cxn.start()
                self._add_cxn(cxn, session, details)

                self.cxn_created.set()

                is_debug and session.debug(
                    f" + StreamCxnCache created new connection: "
                    f"id={cxn.id}, daemon={cxn.daemon}, content_type={content_type}, "
                    f"protocol_type={protocol_type}"
                )

            item = self._get_cache_item(session, details)
            cxn = item.cxn

            is_debug and session.debug(
                f"StreamCxnCache wait for connection: "
                f"id={cxn.id}, content_type={content_type}, "
                f"protocol_type={protocol_type}"
            )

            cxn.wait_connection_result()

            if cxn.is_disconnected or cxn.is_disposed:  # Connection failure for some reason
                is_debug and session.debug("StreamCxnCache: Connection will be deleted, because failure")
                self.del_cxn(cxn, session, details)
                raise ConnectionError(f"Cannot prepare connection {cxn}")

            else:
                item.inc_use()
                is_debug and session.debug(f" <=== StreamCxnCache connection id={cxn.id} is ready")

            return cxn

    def release(self, session: "Session", details: "StreamDetails") -> None:
        content_type = details.content_type
        if not self.has_cxn(session, details):
            session._is_debug() and session.debug(
                f"Cannot release stream connection, because it’s not in the cache\n"
                f"(content_type={content_type}, session={session})"
            )
            return

        item_by_api_type = self._cache[session]
        item = item_by_api_type[details.api_config_key]
        item.dec_use()
        session._is_debug() and session.debug(
            f"StreamCxnCache release (item={item}, content_type={content_type}, session={session.name})"
        )

    def del_cxn(self, cxn: "StreamConnection", session: "Session", details: "StreamDetails") -> None:
        content_type = details.content_type

        if not cxn:
            raise ValueError(
                f"Cannot delete stream connection, "
                f"because it is empty (content_type={content_type}, "
                f"cxn={cxn}, session={session})"
            )

        if not self.has_cxn(session, details):
            raise ValueError(
                f"Cannot delete stream connection, "
                f"because already deleted (content_type={content_type}, "
                f"cxn={cxn}, session={session})"
            )

        item_by_api_type = self._cache[session]
        item = item_by_api_type[details.api_config_key]
        if item.is_using:
            raise AssertionError(
                f"Cannot delete stream connection, "
                f"because it is using (content_type={content_type}, "
                f"cxn={cxn}, session={session})"
            )

        cached_cxn = item.cxn

        if cxn is not cached_cxn:
            raise ValueError(
                f"Cannot delete stream connection, "
                f"because cxn is not the same \n"
                f"(cxn={cxn} != cached_cxn={cached_cxn},"
                f"content_type={content_type}, session={session})"
            )

        item.dispose()

    def del_cxns(self, session: "Session") -> None:
        item_by_content_type = self._cache.get(session, {})
        for item in list(item_by_content_type.values()):
            item.dispose()

        self._cache.pop(session, None)

    def has_cxns(self, session: "Session") -> bool:
        item_by_content_type = self._cache.get(session, {})
        has_cxns = bool(item_by_content_type.values())
        return has_cxns

    def get_cxns(self, session: "Session") -> StreamConnections:
        item_by_content_type = self._cache.get(session, {})
        return [item.cxn for item in item_by_content_type.values()]

    def get_all_cxns(self) -> StreamConnections:
        cxns = []
        for session, item_by_content_type in self._cache.items():
            for cache_item in item_by_content_type.values():
                cxns.append(cache_item.cxn)
        return cxns

    def close_cxns(self, session: "Session") -> None:
        def _close_cxn(item):
            if item.is_using:
                item.cxn.start_disconnecting()

            else:
                item.cxn.start_disconnecting()
                item.cxn.end_disconnecting()
                item.dispose()

        with ThreadPoolExecutor(thread_name_prefix="CloseCxns-Thread") as executor:
            futures = []
            for item in self._get_cache_items(session):
                futures.append(executor.submit(_close_cxn, item))
            wait(futures)
            for fut in futures:
                exception = fut.exception()
                if exception:
                    raise exception

        self._cache.pop(session, None)

    def _add_cxn(self, cxn: "StreamConnection", session: "Session", details: "StreamDetails") -> CacheItem:
        content_type = details.content_type

        if not cxn:
            raise ValueError(
                f"Cannot add stream connection, "
                f"because it is empty: content_type={content_type}, "
                f"cxn={cxn}, session={session}"
            )

        if self.has_cxn(session, details):
            raise ValueError(
                f"Cannot add stream connection, "
                f"because already added: content_type={content_type}, "
                f"cxn={cxn}, session={session}"
            )

        owner = self._cache.setdefault(session, {})
        item = CacheItem(cxn, details, owner)
        owner[details.api_config_key] = item
        return item

    def _get_cache_items(self, session: "Session") -> List[CacheItem]:
        item_by_content_type = self._cache.get(session, {})
        return [item for item in item_by_content_type.values()]

    def _get_cache_item(self, session: "Session", details: "StreamDetails") -> CacheItem:
        cache_item = self._cache[session][details.api_config_key]
        return cache_item

    def is_cxn_alive(self, session: "Session", content_type: "ContentType") -> bool:
        from ._stream_factory import content_type_to_details

        details = content_type_to_details(content_type)
        is_alive = False
        if self.has_cxn(session, details):
            item = self._get_cache_item(session, details)
            is_alive = item.cxn.is_alive()

        return is_alive


stream_cxn_cache: StreamCxnCache = StreamCxnCache()

from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, public_key_b64: str, private_key_b64: str) -> int:
        pass

    @abstractmethod
    def get_public(self, key_id: int) -> str | None:
        pass


class InMemoryKeyStorage(Storage):
    def __init__(self) -> None:
        self._store: dict[int, tuple[str, str]] = {}
        self._next_id: int = 1

    def add(self, public_key_b64: str, private_key_b64: str) -> int:
        key_id = self._next_id
        self._next_id += 1

        self._store[key_id] = (public_key_b64, private_key_b64)
        return key_id

    def get_public(self, key_id: int) -> str | None:
        pair = self._store.get(key_id)
        return pair[0] if pair else None

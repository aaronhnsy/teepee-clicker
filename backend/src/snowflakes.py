import datetime as dt
import time


__all__ = [
    "Snowflake",
    "SnowflakeGenerator",
]


EPOCH: int = 1739003400  # Saturday, 8th February 2025 at 08:30 UTC

MACHINE_ID_BITS: int = 5
MAX_MACHINE_ID: int = -1 ^ (-1 << MACHINE_ID_BITS)

PROCESS_ID_BITS: int = 5
MAX_PROCESS_ID: int = -1 ^ (-1 << PROCESS_ID_BITS)

SEQUENCE_BITS: int = 12
MAX_SEQUENCE_ID: int = -1 ^ (-1 << SEQUENCE_BITS)

PROCESS_ID_SHIFT: int = SEQUENCE_BITS
MACHINE_ID_SHIFT: int = SEQUENCE_BITS + PROCESS_ID_BITS
TIMESTAMP_SHIFT: int = SEQUENCE_BITS + PROCESS_ID_BITS + MACHINE_ID_BITS


class Snowflake:

    def __init__(self, snowflake: int, /) -> None:
        self.snowflake: int = snowflake

    @property
    def timestamp(self) -> int:
        return (self.snowflake >> TIMESTAMP_SHIFT) + EPOCH

    @property
    def created_at(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(
            self.timestamp / 1000,
            tz=dt.UTC,
        )

    @property
    def machine_id(self) -> int:
        return (self.snowflake >> MACHINE_ID_SHIFT) & MAX_MACHINE_ID

    @property
    def process_id(self) -> int:
        return (self.snowflake >> PROCESS_ID_SHIFT) & MAX_PROCESS_ID

    @property
    def sequence(self) -> int:
        return self.snowflake & MAX_SEQUENCE_ID

    def __int__(self) -> int:
        return self.snowflake

    def __str__(self) -> str:
        return str(self.snowflake)

    def __repr__(self) -> str:
        return (
            f"<Snowflake: id={self.snowflake}, timestamp={self.timestamp}, created_at=<{self.created_at!r}>, "
            f"sequence={self.sequence}, machine_id={self.machine_id}, process_id={self.process_id}>"
        )


class SnowflakeGenerator:

    def __init__(self, *, machine_id: int, process_id: int) -> None:
        if machine_id < 0 or machine_id > MAX_MACHINE_ID:
            msg = f"machine id must be between 0 and {MAX_MACHINE_ID} inclusive."
            raise ValueError(msg)
        if process_id < 0 or process_id > MAX_PROCESS_ID:
            msg = f"process id must be between 0 and {MAX_PROCESS_ID} inclusive."
            raise ValueError(msg)
        self.machine_id: int = machine_id
        self.process_id: int = process_id
        self.sequence: int = 0
        self.last_timestamp: int = -1

    def generate(self) -> int:
        while True:
            timestamp = int(time.time() * 1000)
            if timestamp < self.last_timestamp:
                print("clock is moving backwards. waiting until it catches up.")
                time.sleep((self.last_timestamp - timestamp) / 1000)
                continue
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & MAX_SEQUENCE_ID
                if self.sequence == 0:
                    print("sequence overflow. waiting until next millisecond.")
                    time.sleep(1 / 1000)
                    continue
            else:
                self.sequence = 0
            self.last_timestamp = timestamp
            return (
                ((timestamp - EPOCH) << TIMESTAMP_SHIFT)
                | (self.machine_id << MACHINE_ID_SHIFT)
                | (self.process_id << PROCESS_ID_SHIFT)
                | self.sequence
            )

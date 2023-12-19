from collections import defaultdict
from collections.abc import Generator

def HASHMAP() -> Generator[None, bytes | None, int]:
    map_: dict[int, dict[bytes, int]] = defaultdict(dict)
    hash_: int = 0
    key: bytes = bytes([])
    input_: bytes | None = None
    while True:
        input_ = yield 
        if input_ is None:
            return sum(f * (i + 1) * (b + 1) 
                       for b, d in map_.items() 
                       for i, f in enumerate(d.values()))
        else:
            match(input_):
                case b',':
                    hash_ = 0
                    key = bytes([])
                case b'-':
                    if key in map_[hash_]:
                        del map_[hash_][key]
                case b'=':
                    focal = yield
                    if focal is not None:
                        map_[hash_][key] = int(focal)
                    else:
                        return -1
                case _:
                    hash_ = ((hash_ + int.from_bytes(input_)) * 17) & 255
                    key += input_


with open("data.txt", "rb") as file:
    hash_map = HASHMAP()
    next(hash_map)
    try:
        while len(next_byte := file.read(1)) > 0:
            hash_map.send(next_byte)
        next(hash_map)
    except StopIteration as e:
        print(e.value)
import hashlib

def det_seed(base_seed:int, particle_count: int, dataset_id:int) -> int:
    # Suche nur ne ausrede um mal hashs zu benutzen lol, aber ein guter weg um deterministische random seeds für bestimmte experiment config zu kriegen ig
    payload = f"{base_seed}:{particle_count}:{dataset_id}"
    return int.from_bytes((hashlib.sha256(payload).digest())[:8], "big")


    
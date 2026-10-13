"""Hostname generator logic.

Format (8 characters): OS (1) + Environment (2) + Country (3-5) + Node (6-8).
Example: AIGER789 -> AIX | Integration | Germany | Node 789

A keyword (e.g. "IRL", "LP", "007") can be fixed anywhere inside the hostname.
Generation then samples from the original probabilities, conditioned on the
hostname containing that keyword.
"""
import random
import pandas as pd

OS_CODES = {"L": ("Linux", 40), "S": ("Solaris", 30), "A": ("AIX", 20), "H": ("HP-UX", 10)}
ENV_CODES = {"D": ("Development", 10), "I": ("Integration", 10), "T": ("Testing", 25),
             "S": ("Staging", 25), "P": ("Production", 30)}
COUNTRY_CODES = {"NOR": ("Norway", 6), "FRA": ("France", 9), "ITA": ("Italy", 16),
                 "ESP": ("Spain", 16), "GER": ("Germany", 23), "IRL": ("Ireland", 30)}
NODES = [str(i).zfill(3) for i in range(1, 1000)]
LENGTH = 8


def clean_keyword(keyword: str) -> str:
    return "".join(ch for ch in (keyword or "").upper() if ch.isalnum())[:LENGTH]


def _matches(code: str, slot: str) -> bool:
    """slot uses '?' for free characters."""
    return all(s == "?" or s == c for c, s in zip(code, slot))


def _placements(keyword: str) -> list:
    """Every position where the keyword fits, with the compatible options for each part."""
    if not keyword:
        return [(1.0, list(OS_CODES), list(ENV_CODES), list(COUNTRY_CODES), NODES)]
    result = []
    for start in range(LENGTH - len(keyword) + 1):
        template = "?" * start + keyword + "?" * (LENGTH - start - len(keyword))
        os_opts = [c for c in OS_CODES if _matches(c, template[0])]
        env_opts = [c for c in ENV_CODES if _matches(c, template[1])]
        ctry_opts = [c for c in COUNTRY_CODES if _matches(c, template[2:5])]
        node_opts = [n for n in NODES if _matches(n, template[5:])]
        weight = (sum(OS_CODES[c][1] for c in os_opts) / 100
                  * sum(ENV_CODES[c][1] for c in env_opts) / 100
                  * sum(COUNTRY_CODES[c][1] for c in ctry_opts) / 100
                  * len(node_opts) / len(NODES))
        if weight > 0:
            result.append((weight, os_opts, env_opts, ctry_opts, node_opts))
    return result


def is_possible(keyword: str) -> bool:
    return bool(_placements(clean_keyword(keyword)))


def _pick(options: list, codes: dict) -> str:
    return random.choices(options, weights=[codes[c][1] for c in options])[0]


def generate_hostnames(n: int, keyword: str = "", unique: bool = True) -> list[str]:
    """Generate up to n hostnames containing the keyword.

    With unique=True the list may be shorter than n when the keyword
    leaves fewer possible combinations.
    """
    keyword = clean_keyword(keyword)
    placements = _placements(keyword)
    if not placements:
        raise ValueError(f"No valid hostname can contain '{keyword}'.")
    weights = [p[0] for p in placements]
    names, seen = [], set()
    attempts, max_attempts = 0, n * 50 + 1000
    while len(names) < n and attempts < max_attempts:
        attempts += 1
        _, os_o, env_o, ctry_o, node_o = random.choices(placements, weights=weights)[0]
        name = (_pick(os_o, OS_CODES) + _pick(env_o, ENV_CODES)
                + _pick(ctry_o, COUNTRY_CODES) + random.choice(node_o))
        if unique and name in seen:
            continue
        seen.add(name)
        names.append(name)
    return names


def is_valid(hostname: str) -> bool:
    return (len(hostname) == LENGTH and hostname[0] in OS_CODES and hostname[1] in ENV_CODES
            and hostname[2:5] in COUNTRY_CODES and hostname[5:].isdigit()
            and hostname[5:] != "000")


def decode(hostname: str) -> dict:
    return {"hostname": hostname,
            "os": OS_CODES.get(hostname[0], ("Unknown",))[0],
            "environment": ENV_CODES.get(hostname[1], ("Unknown",))[0],
            "country": COUNTRY_CODES.get(hostname[2:5], ("Unknown",))[0],
            "node": int(hostname[-3:])}


def build_dataframe(n: int, keyword: str = "", unique: bool = True) -> pd.DataFrame:
    rows = [decode(h) for h in generate_hostnames(n, keyword, unique)]
    return pd.DataFrame(rows, columns=["hostname", "os", "environment", "country", "node"])


if __name__ == "__main__":
    build_dataframe(1500, unique=False).to_csv("hosts.csv", index=False)
    print("hosts.csv generated")

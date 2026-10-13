"""Hostname generator logic (extracted from the Hostnames_Generator.ipynb notebook).

Key change from the notebook: global lists are no longer used.
In an API, global variables would accumulate hostnames across requests.
"""
import random
import pandas as pd

OS_CODES = {"L": ("Linux", 40), "S": ("Solaris", 30), "A": ("AIX", 20), "H": ("HP-UX", 10)}
ENV_CODES = {"D": ("Development", 10), "I": ("Integration", 10), "T": ("Testing", 25),
             "S": ("Staging", 25), "P": ("Production", 30)}
COUNTRY_CODES = {"NOR": ("Norway", 6), "FRA": ("France", 9), "ITA": ("Italy", 16),
                 "ESP": ("Spain", 16), "GER": ("Germany", 23), "IRL": ("Ireland", 30)}


def _pick(codes: dict) -> str:
    return random.choices(list(codes), weights=[w for _, w in codes.values()])[0]


def generate_hostnames(n: int) -> list[str]:
    return [_pick(OS_CODES) + _pick(ENV_CODES) + _pick(COUNTRY_CODES)
            + str(random.randint(1, 999)).zfill(3) for _ in range(n)]


def is_valid(hostname: str) -> bool:
    return (len(hostname) == 8 and hostname[0] in OS_CODES and hostname[1] in ENV_CODES
            and hostname[2:5] in COUNTRY_CODES and hostname[5:].isdigit())


def get_os(hostname: str) -> str:
    return OS_CODES.get(hostname[0], ("Unknown",))[0]


def get_environment(hostname: str) -> str:
    return ENV_CODES.get(hostname[1], ("Unknown",))[0]


def get_country(hostname: str) -> str:
    return COUNTRY_CODES.get(hostname[2:5], ("Unknown",))[0]


def decode(hostname: str) -> dict:
    return {"hostname": hostname, "os": get_os(hostname), "environment": get_environment(hostname),
            "country": get_country(hostname), "node": int(hostname[-3:])}


def build_dataframe(n: int) -> pd.DataFrame:
    return pd.DataFrame([decode(h) for h in generate_hostnames(n)])


def stats(df: pd.DataFrame) -> dict:
    return {"total": len(df),
            "by_os": df["os"].value_counts().to_dict(),
            "by_environment": df["environment"].value_counts().to_dict(),
            "by_country": df["country"].value_counts().to_dict()}


if __name__ == "__main__":
    # Same as the notebook: generate 1500 hosts and save them to CSV
    build_dataframe(1500).to_csv("hosts.csv", index=False)
    print("hosts.csv generated")

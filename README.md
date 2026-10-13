# Random Hostname Generator

Generates 1,500 hostnames following a structured format based on operating systems, environments, and countries. Hostnames are stored in a pandas DataFrame and exported to CSV.

Hostname Structure (8 characters)

| Position | Component   | Codes                                                              | Probability                |
| -------- | ----------- | ------------------------------------------------------------------ | -------------------------- |
| 1        | OS          | L (Linux), S (Solaris), A (AIX), H (HP-UX)                         | 40%, 30%, 20%, 10%         |
| 2        | Environment | D (Dev), I (Integration), T (Testing), S (Staging), P (Production) | 10%, 10%, 25%, 25%, 30%    |
| 3-5      | Country     | NOR, FRA, ITA, ESP, GER, IRL                                       | 6%, 9%, 16%, 16%, 23%, 30% |
| 6-8      | Node        | 001–999                                                            | Uniform                    |

Example: `AIGER789` → AIX | Integration | Germany | Node 789

Key Functions

* `set_hostnames(n)`
* `get_os(hostname)`, `get_environment(hostname)`, `get_country(hostname)`
* `set_dataframe(count)`

Visualizations

* Hosts per country and environment
* OS distribution by country
* Total OS counts

Output

* `hosts.csv` with 1,500 hostnames
* Distribution charts

Requirements

* Python 3.x, pandas, numpy, matplotlib, seaborn

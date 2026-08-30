# SkyHelper-Networth-Tests

This is for testing the difference in networth calculation between my Python rewrite and the
original Node.js module. Order to run scripts:

1. `prepare_test_data.py` (optional if you don't want to refresh data, also needs to provide a
   Hypixel API key at the top of the script)
2. `calculate_node.js` and `calculate_python.py` (in any order)
3. `check_results.py`

It will round the results to 2 decimals and check if it's the same.
It checks regular networth and unsoulbound networth.
The last script will output a Markdown table in the console
and in the GitHub Actions Summary if run in CI.

beancount_portfolio_report
==============================

### Note
This repo is forked from [beancount_portfolio_allocation](https://github.com/ghislainbourgeois/beancount_portfolio_allocation)
minor changes are made for portfolio performance report.

Reports on portfolio performance in beancount. Useful for risk analysis.

Installation
------------

### From source

```bash
$ python3 setup.py install
```

Usage
-----

```text
usage: Report on portfolio asset classes.
       [-h] --portfolio PORTFOLIO bean

positional arguments:
  bean                  Path to the beancount file.

optional arguments:
  -h, --help            show this help message and exit
  --portfolio PORTFOLIO
                        Name of portfolio to report on
```

### Example

```bash
$ bean-portfolio-allocation-report ledger.beancount --portfolio default
BOND
====
Subclass            Book Value    Market Value    PnL    PnL %
----------------  ------------  --------------  -----  -------
Domestic Bond             0.00            0.00   0.00     0.00
Overseas Bond             0.00            0.00   0.00     0.00
SUM                       0.00            0.00   0.00     0.00


STOCK
=====
Subclass             Book Value    Market Value    PnL    PnL %
----------------   ------------  --------------  -----  -------
Domestic Stock             0.00            0.00   0.00     0.00
Overseas Stock             0.00            0.00   0.00     0.00
SUM                        0.00            0.00   0.00     0.00


CASH
====
Subclass      Book Value    Market Value    PnL    PnL %
----------  ------------  --------------  -----  -------
CNY                 0.00            0.00   0.00     0.00
SUM                 0.00            0.00   0.00     0.00


TOTAL
=====
Subclass      Book Value    Market Value     PnL    PnL %
----------  ------------  --------------  ------  -------
SUM                 0.00            0.00    0.00     0.00
```


Prerequisites
-------------

Before running this tool, your beancount files will need some additional
metadata to help it do its job.

### Commodities

All the commodities/currency you want to track will need to have the
`asset-class` and `asset-subclass` metadata strings filled in. The actual
values are up to you. Here are some examples:

```beancount
1867-01-01 commodity CAD
  asset-class: "cash"
  asset-subclass: "cash"

1986-03-13 commodity MSFT
  asset-class: "equity"
  asset-subclass: "us-stock"

1977-01-03 commodity AAPL
  asset-class: "equity"
  asset-subclass: "us-stock"

2007-04-04 commodity VAB
  asset-class: "fixed-income"
  asset-subclass: "ca-bond"
```

You will also need valid price directives for all commodities held at cost and
at least one 'operating_currency' option defined. The values in the report will
all be converted to the first 'operating_currency' defined. A future version
will offer a way to specify the currency to use for reporting.

### Accounts

Accounts need to be part of a specific portfolio to track. Only one portfolio
is supported by account, but you can have multiple portfolios over multiple
accounts:

```beancount
2000-01-01 open Assets:CA:Employer:PensionPlan
  portfolio: "pension"

2000-01-01 open Assets:CA:Questrade:RRSP
  portfolio: "pension"

2000-01-01 open Assets:CA:Questrade:Trading
  portfolio: "day-trading"
```

#### Cash Based Accounts

It is possible to specify `asset-class` and `asset-subclasse` or accounts that
are reported as a cash-value, but are backed by specific asset classes.

This is use in particular for managed retirement accounts.

```beancount
2000-01-01 open Assets:CA:Employer:PensionPlan
  portfolio: "pension"
  asset-class: "fixed-income"
  asset-subclass: "ca-bond"
```

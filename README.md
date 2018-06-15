beancount_portfolio_allocation
==============================

Reports on portfolio asset allocations in beancount. Useful for risk analysis
and for rebalancing purposes.

Installation
------------

### From source

```bash
$ python3 setup.py install
```

### PIP

```bash
$ pip install beancount_portfolio_allocation
```

Usage
-----

```text
usage: Report on portfolio asset classes allocation vs targets.
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
$ bean-portfolio-allocation-report ledger.beancount --portfolio pension
cash
===========================================================================
subclass 	 amount 	 percent 	 target 	 difference
---------------------------------------------------------------------------
cash       	 380.00 	 19.00 		 0.00 		 -380.00

equity
===========================================================================
subclass 	 amount 	 percent 	 target 	 difference
---------------------------------------------------------------------------
ca-stock   	 700.00 	 35.00 		 30.00 		 -100.00
us-stock   	 600.00 	 30.00 		 30.00 		 0.00

fixed
===========================================================================
subclass 	 amount 	 percent 	 target 	 difference
---------------------------------------------------------------------------
ca-bond    	 320.00 	 16.00 		 40.00 		 480.00
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

You will also need valid price directives for all commodities held at cost.

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

### Target allocations

You can currently define your target allocation percentages for different asset
subclasses in a portfolio using custom directives. There can currently be only
one directive for the same portfolio and asset subclass. Missing allocation
targets will be assumed to be 0%. An example 60/40 portfolio target might look
like this (*NOT* a financial advice):

```beancount
2018-06-14 custom "allocation" "pension" "ca-stock" 30
2018-06-14 custom "allocation" "pension" "us-stock" 30
2018-06-14 custom "allocation" "pension" "ca-bond" 40
```


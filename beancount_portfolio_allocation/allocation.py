__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import logging


class Allocations(list):
    def asset_classes(self):
        result = set()
        for p in self:
            result.add(p.asset_class)
        return sorted(result)

    def asset_subclasses(self, asset_class):
        result = set()
        for p in self:
            if p.asset_class == asset_class:
                result.add(p.asset_subclass)
        return sorted(result)

    def value_for_class_subclass(self, asset_class, asset_subclass):
        result = 0
        for p in self:
            if (p.asset_class == asset_class and
                    p.asset_subclass == asset_subclass):
                result += p.value
        return result

    def value_for_class(self, asset_class):
        result = 0
        for p in self:
            if (p.asset_class == asset_class):
                result += p.value
        return result

    def cost_for_class_subclass(self, asset_class, asset_subclass):
        result = 0
        for p in self:
            if (p.asset_class == asset_class and
                    p.asset_subclass == asset_subclass):
                result += p.cost
        return result

    def cost_for_class(self, asset_class):
        result = 0
        for p in self:
            if (p.asset_class == asset_class):
                result += p.cost
        return result

    def pnl_for_class_subclass(self, asset_class, asset_subclass):
        return ((self.value_for_class_subclass(asset_class, asset_subclass) -
                 self.cost_for_class_subclass(asset_class, asset_subclass)))

    def pnl_for_class(self, asset_class):
        return ((self.value_for_class(asset_class) -
                 self.cost_for_class(asset_class)))

    def pnl_percentage_for_class_subclass(self, asset_class, asset_subclass):
        cost = self.cost_for_class_subclass(asset_class, asset_subclass)
        if cost == 0:
            return 0
        else:
            return (100 *
                    (self.pnl_for_class_subclass(asset_class, asset_subclass) /
                     cost))

    def pnl_percentage_for_class(self, asset_class):
        cost = self.cost_for_class(asset_class)
        if cost == 0:
            return 0
        else:
            return (100 * (self.pnl_for_class(asset_class) / cost))

    def percentage_for_class_subclass(self, asset_class, asset_subclass):
        return (100 *
                (self.value_for_class_subclass(asset_class, asset_subclass) /
                 self.total_invested_for_portfolio()))

    def total_invested_for_portfolio(self):
        return sum([p.value for p in self])

    def total_cost_for_portfolio(self):
        return sum([p.cost for p in self])

    def total_pnl(self):
        return self.total_invested_for_portfolio() - self.total_cost_for_portfolio()

    def total_pnl_percentage(self):
        return (100 * (self.total_pnl() / self.total_cost_for_portfolio()))


class Position:
    def __init__(self, symbol, value, cost, asset_class, asset_subclass, account, price):
        self.symbol = symbol
        self.value = value
        self.cost = cost
        self.asset_class = asset_class
        self.asset_subclass = asset_subclass
        self.account = account
        self.price = price
        self.validate_value()

    def validate_value(self):
        if self.value is None:
            if self.price is None:
                logging.error("Could not get a value for currency %s in account %s. Using 0. Are you missing a price directive?" % (self.symbol, self.account))
            else:
                logging.info("Assuming zero value for currency %s in account %s." % (self.symbol, self.account))
            self.value = 0
            self.cost = 0

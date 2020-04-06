#!/usr/bin/env python3
__author__ = "Ghislain Bourgeois"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import beancount_portfolio_allocation.loader as loader

from tabulate import tabulate


def report_data(targets, allocations, total):
    result = dict()
    for asset_class in allocations.asset_classes():
        result[asset_class] = list()
        for subclass in allocations.asset_subclasses(asset_class):
            value = allocations.value_for_class_subclass(asset_class, subclass)
            cost = allocations.cost_for_class_subclass(asset_class, subclass)
            pnl = allocations.pnl_for_class_subclass(asset_class, subclass)
            pnl_percentage = allocations.pnl_percentage_for_class_subclass(asset_class,
                                                                           subclass)
            # percentage = allocations.percentage_for_class_subclass(asset_class,
            #                                                        subclass)
            # target = targets.get(subclass, 0)
            # diff = cash_difference(target, percentage, total)
            line = list()
            line.append(subclass)
            line.append(float(cost))
            line.append(float(value))
            line.append(float(pnl))
            line.append(float(pnl_percentage))
            # line.append(float(percentage))
            # line.append(float(target))
            # line.append(float(diff))
            result[asset_class].append(line)
        value = allocations.value_for_class(asset_class)
        cost = allocations.cost_for_class(asset_class)
        pnl = allocations.pnl_for_class(asset_class)
        pnl_percentage = allocations.pnl_percentage_for_class(asset_class)
        line = list()
        line.append('SUM')
        line.append(float(cost))
        line.append(float(value))
        line.append(float(pnl))
        line.append(float(pnl_percentage))
        result[asset_class].append(line)
    result['TOTAL'] = list()
    value = allocations.total_invested_for_portfolio()
    cost = allocations.total_cost_for_portfolio()
    pnl = allocations.total_pnl()
    pnl_percentage = allocations.total_pnl_percentage()
    line = list()
    line.append('SUM')
    line.append(float(cost))
    line.append(float(value))
    line.append(float(pnl))
    line.append(float(pnl_percentage))
    result['TOTAL'].append(line)
    return result


def report(bean, portfolio):
    targets, allocations, total = loader.load(bean, portfolio)
    data = report_data(targets, allocations, total)

    #head = ["Subclass", "Book Value", "Market Value", "PnL", "PnL%", "Percentage", "Target %", "Difference"]
    head = ["Subclass", "Book Value", "Market Value", "PnL", "PnL %"]
    report = ""
    first = True

    for asset_class in data:
        if not first:
            report += "\n\n"
        else:
            first = False
        report += asset_class.upper()
        report += "\n"
        report += "=" * len(asset_class)
        report += "\n"

        report += tabulate(data[asset_class], head, floatfmt='.2f')
        report += "\n"

    return report


def percentage_difference(target, percentage):
    return float(target - percentage)


def cash_difference(target, percentage, total):
        return percentage_difference(target, percentage) / 100 * float(total)


def main():
    import argparse
    parser = argparse.ArgumentParser("Report on portfolio asset classes allocation vs targets.")
    parser.add_argument('bean', help='Path to the beancount file.')
    parser.add_argument('--portfolio',
                        type=str,
                        help='Name of portfolio to report on',
                        required=True)
    args = parser.parse_args()

    print(report(args.bean, args.portfolio))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
from app.core import engine
from datetime import datetime
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plots transnational covid-19 statistics.')

    # optionally provide the limit date (by default today)
    parser.add_argument('--days', type=int, required=False,
                        help='number of days',
                        default=engine.DEFAULT_DAYS)
    args = parser.parse_args()

    # generate graphs
    nations = engine.collectData(args.days)

    plt.show()


import requests
import collections
import base64
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from io import BytesIO

# URL template to fetch department data
URL_DEP = "https://dashboard.covid19.data.gouv.fr/data/code-DEP-{}.json"

DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DAYS = 30

# Create a sublcass for department metadata, for which labels are defined here
META_NAMES = ['index', 'dep', 'pop', 'raw', 'dates', 'tests', 'cases', 'deaths', 'reanims', 'hospital','sumTests','sumCases']
META_LABEL = ['index', 'dep', 'pop', 'raw', 'dates', 'tests', 'positives', 'deaths', 'reanimations', 'hospitalized','sum of tests','sum of cases']
Meta = collections.namedtuple('Meta', META_NAMES)

def collectData(iDays=DEFAULT_DAYS):
    departments = []

    parseJSON(departments, iDays, '06', 2007684)
    parseJSON(departments, iDays, '13', 1083310)
    parseJSON(departments, iDays, '75', 2187526)

    outputGraphRaw = {}

    chartRaw = BytesIO()
    plotDepartmentData(departments, "Hospitalized and in Reanimation in the last {} days".format(iDays), [9, 8], chartRaw)
    chartRaw.seek(0)

    chartRaw = BytesIO()
    plotDepartmentData(departments,"Cases and Positives in the last {} days".format(iDays), [10,11], chartRaw)
    chartRaw.seek(0)

    chartRaw = BytesIO()
    plotDepartmentData(departments,"Deaths in the last {} days".format(iDays), [7], chartRaw)
    chartRaw.seek(0)

    outputGraphRaw['cases'] = base64.b64encode(chartRaw.getvalue())

    return outputGraphRaw

def parseJSON(iDepartments, iDays, iDep = '06', iPop = 1 ):
    # fetch json data and check the error
    print('Fetching', URL_DEP.format(iDep),'...')
    r = requests.get(URL_DEP.format(iDep))
    if r.status_code != 200:
        print("ERROR",r.status_code)
        return {}
    aJSONDayArray = r.json()

    # prepare the tuple for plotting

    aDepartment = Meta(len(iDepartments), iDep, iPop, r.text, [], [], [], [], [], [], [], [])

    aCasesCounter = 0
    aTestsCounter = 0

    # add info for each date
    for aJSONDay in aJSONDayArray:
        # EXAMPLE:
        #         "deces": 2,
        #         "reanimation": 1,
        #         "hospitalises": 25,
        #         "gueris": 47,
        #         "date": "2020-03-18",
        #         "code": "DEP-06",
        #         "nom": "Alpes-Maritimes",
        #         "testsRealises": 29,
        #         "testsPositifs": 4,

        # skip old tuples
        if any(k not in aJSONDay for k in ("date","testsRealises", "testsPositifs", "deces", "reanimation", "hospitalises")):
            continue
        # skip bogus tuples
        if any(aJSONDay[k] is None for k in ("date","testsRealises", "testsPositifs", "deces", "reanimation", "hospitalises")):
            continue

        currentDate = aJSONDay['date']
        minDate = (datetime.now() - timedelta(days=iDays)).strftime(DATE_FORMAT)
        if currentDate <= minDate:
            continue

        aDepartment.dates.append(currentDate)
        # tests
        aDepartment.tests.append(int(aJSONDay['testsRealises']))
        aTestsCounter += int(aJSONDay['testsRealises'])
        aDepartment.sumCases.append(aTestsCounter)

        # cases
        aDepartment.cases.append(int(aJSONDay['testsPositifs']))
        aCasesCounter += int(aJSONDay['testsPositifs'])
        aDepartment.sumTests.append(aCasesCounter)

        aDepartment.deaths.append(int(aJSONDay['deces']))
        aDepartment.reanims.append(int(aJSONDay['reanimation']))
        aDepartment.hospital.append(int(aJSONDay['hospitalises']))

    iDepartments.append(aDepartment)


def plotDepartmentData(iDepartments, iTitle, iTupleIndexes, iChartRaw):
    # print the delayed plots, use italy as reference country
    plt.figure()
    for aDepartment in iDepartments:
        # skip countries with no data (might happen with deaths)
        if len(aDepartment.dates) == 0:
            continue

        for aTupleIndex in iTupleIndexes:
            y = list(map(int, aDepartment[aTupleIndex]))

            lines = plt.plot(aDepartment.dates, y, lw=0.5, marker='.', label="{} {}".format(aDepartment.dep,META_LABEL[aTupleIndex]))
            # be coherent across different graphs with color coding
            lines[0].set_color('C' + str(aDepartment.index))

    plt.grid()
    plt.xticks(rotation=90)
    plt.legend()
    plt.title(iTitle)
    plt.savefig(iChartRaw, format='png')
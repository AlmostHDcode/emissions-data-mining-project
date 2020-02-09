"""
data_mining_project.py:
Final Project for data mining.
Takes a dataset about greenhouse gasses and uses pandas to retrieve interesting data
"""

__author__ = "Matt Hunt, Corey Wright, Nicar Lopez"
__version__ = "5.0"
__date__ = "Dec 1, 2019"

from matplotlib import pyplot as plt
import pandas as pd


def dataset_info(filename):
    """
    returns information about the csv dataset
    :param filename: the csv file to read
    :return: information about the dataset
    """
    dataset = pd.read_csv(filename)
    print("Rows:", dataset.shape[0], "Columns:", dataset.shape[1])
    print("Total Number of Data:", dataset.shape[0] * dataset.shape[1])
    print("Describe Dataset:")
    print(dataset.describe())
    print(dataset.head(30))


def preprocess(filename, filterID=0):
    """
    Returns a processed dataframe based on the specified
    filterID.

    Filter IDs:
        0 = Basic with world value
        1 = Countries only
        2 = Continents only

    :param filename: the csv file to read
    :param filterID: an integer value specifying what to filter out
    :return: a pre-processed dataframe
    """

    dataframe = pd.read_csv(filename)
    dataframe.set_index("Country", inplace=True)

    # valid filters
    filters = [0, 1, 2]

    if filterID not in filters:

        print("Invalid filterID. Doing very basic pre-processing")

    else:

        # Valid filters
        if filterID == 0:
            None
        elif filterID == 1:
            dataframe = dataframe.drop(
                ['World', 'Africa', 'Americas (other)', 'Asia and Pacific (other)', 'Australia', 'EU-28',
                 'Europe (other)', 'Kyrgysztan', 'Middle East', 'World'])
        elif filterID == 2:
            dataframe = dataframe.loc[
                ['Africa', 'Americas (other)', 'Asia and Pacific (other)', 'Australia', 'EU-28', 'Europe (other)',
                 'United Kingdom', 'United States', 'Canada']]
        else:
            None

    return dataframe


def top_countries(filename):
    """
    Find and return that top 10 countries based on emissions
    :param filename: The csv file to be read
    :return: the list of the top 10 countries based on emissions
    """
    # dataset = pd.read_csv(filename)
    dataset = preprocess(filename, 1)
    dataset = dataset.reset_index()
    total_country_emissions = {}
    top_countries_emissions = {}

    # add all countries and the sum of their emissions into dictionary
    for i in range(0, dataset.shape[0]):
        if dataset.iat[i, 0] != 'World':
            total_country_emissions[dataset.iat[i, 0]] = sum(dataset.loc[i, '1751':])

    # sort the dictionary by emissions descending and add top 10 to new dict
    temp = sort_dict_desc(total_country_emissions)

    for i in range(10):
        top_countries_emissions[temp[i][0]] = temp[i][1]

    return top_countries_emissions


def bottom_countries(filename):
    # dataset = pd.read_csv(filename)
    dataset = preprocess(filename, 1)
    dataset = dataset.reset_index()
    total_country_emissions = {}
    bot_countries_emissions = {}

    # add all countries and the sum of their emissions into dictionary
    for i in range(0, dataset.shape[0]):
        if dataset.iat[i, 0] != 'World':
            total_country_emissions[dataset.iat[i, 0]] = sum(dataset.loc[i, '1751':])

    # sort the dictionary by emissions descending and add top 10 to new dict
    temp = sort_dict_asc(total_country_emissions)

    for i in range(10):
        bot_countries_emissions[temp[i][0]] = temp[i][1]

    return bot_countries_emissions


def sort_dict_desc(dictionary):
    """
    takes a dictionary and sorts it in descending order by the value
    :param dictionary: the dictionary to be sorted
    :return: the sorted dictionary that shows the items and their frequencies sorted by the frequencies
    """
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)


def sort_dict_asc(dictionary):
    """
    takes a dictionary and sorts it in descending order by the value
    :param dictionary: the dictionary to be sorted
    :return: the sorted dictionary that shows the items and their frequencies sorted by the frequencies
    """
    return sorted(dictionary.items(), key=lambda x: x[1])


def top_emissions_over_time(filename, dictionary):
    # dataset = pd.read_csv(filename)
    # dataset.set_index("Country", inplace=True)
    dataset = preprocess(filename, 1)

    yticks = [x for x in range(0, (4 * (10 ** 11)), 10000000000)]

    x = []
    for col in dataset.columns:
        if col != 'Country':
            x.append(col)

    plt.xlabel("Years")
    plt.ylabel("Emissions (tons)")
    plt.title("Fig 1: Emissions of Top Countries Over Time")

    for k in dictionary.keys():
        y = dataset.loc[k, '1751':]
        plt.plot(x, y, label=k)

    plt.yticks(yticks)
    plt.legend()
    plt.show()


def bot_emissions_over_time(filename, dictionary):
    # dataset = pd.read_csv(filename)
    # dataset.set_index("Country", inplace=True)
    dataset = preprocess(filename, 1)

    yticks = [x for x in range(0, (5 * (10 ** 6)), 100000)]

    x = []
    for col in dataset.columns:
        if col != 'Country':
            x.append(col)

    plt.xlabel("Years")
    plt.ylabel("Emissions (tons)")
    plt.title("Fig 2: Emissions of Bottom Countries Over Time")

    for k in dictionary.keys():
        y = dataset.loc[k, '1751':]
        plt.plot(x, y, label=k)

    plt.yticks(yticks)
    plt.legend()
    plt.show()


def emission_percent_of_world(filename, dictionary):
    dataset = pd.read_csv(filename)
    dataset.set_index("Country", inplace=True)
    # dataset = preprocess(filename, 1)

    # use the top 10 dict returned from top_countries
    # sum of dataset.loc["Country name from the dict", '1751':]
    # sum of dataset.loc["World", '1751':]
    # what percent is each country compared to world
    # make pie chart

    percentages = dict()

    world_total = dataset.loc['World']['2017']

    for country, value in dictionary.items():
        percentages[country] = round(value / world_total, 3)

    labels = []
    values = []

    for k, v in percentages.items():
        labels.append(k)
        values.append(v)

    plt.pie(values, labels=labels, autopct='%1.1f%%')
    # plt.legend(labels)
    plt.title("Fig 3: Percentage of World's Emissions (tons)")

    plt.show()


def emissions_over_0(filename):
    # dataset = pd.read_csv(filename)
    dataset = preprocess(filename, 1)
    dataset = dataset.reset_index()

    # for each country find the point where the emissions first went over 0 tons

    over_0 = {}
    years = dataset.columns.values.tolist()

    for i in range(0, dataset.shape[0]):
        for j in range(1, dataset.shape[1]):
            if dataset.iat[i, 0] != 'World' and dataset.iat[i, j] > 0:
                country = dataset.iat[i, 0]
                over_0[country] = years[j]
                break

    return over_0


def time_period_growth(filename, dictionary):
    """
    Asks the user to choose an option of which time period to show info on.
    Contains predefined time frames to choose from.
    """

    dataset = pd.read_csv(filename)
    dataset.set_index("Country", inplace=True)
    # dataset = dataset.drop(['World', 'Kyrgysztan'])

    countries = []

    for k in dictionary.keys():
        countries.append(k)

    dataset = dataset.loc[countries]

    choices = ['1', '2', '3', '4', 'x']
    periodName = ""
    timeBegin = None
    timeEnd = None

    while True:

        # [MENU]
        print("\n[Time Period Growth Menu]\n")
        print("[1]: American Industrialization")
        print("[2]: WWI")
        print("[3]: WWII")
        print("[4]: Modern era (end of WWII-2017)")
        print("[x]: EXIT")

        choice = input("Please choose an option: ")

        if choice not in choices:

            print("Please enter a valid choice..")

        else:

            # Options to choose from start here
            if choice == '1':

                # AMERICAN INDUSTRIALIZATION
                periodName = "Industrial Revolution US"
                # Start 5 years before the industrial revolution
                timeBegin = 1790 - 5
                # End 50 years after 1790
                timeEnd = 1790 + 50

            elif choice == '2':

                # WWI
                periodName = "WWI"
                # Start 5 years before WWI
                timeBegin = 1914 - 5
                # End 5 years after WWI ended
                timeEnd = 1918 + 5

            elif choice == '3':

                # WWII
                periodName = "WWII"
                # Start 5 years before WWII
                timeBegin = 1939 - 5
                # End 5 years after WWII ended
                timeEnd = 1945 + 5

            elif choice == '4':

                periodName = "Modern Era (End of WWII-2017)"
                timeBegin = 1951
                timeEnd = 2017

            else:

                # Stop looping
                break

            plt.xlabel("Country")
            plt.ylabel("Emissions (tons)")
            title = "Fig 4: Growth During" + " " + periodName
            plt.title(title)

            # Create a bar graph showing the emissions created during the time period
            # x denotes countries, y denotes total emissions created during the time frame
            # we only need to get data from the year of timeBegin and timeEnd
            x = dataset[[str(timeBegin), str(timeEnd)]]

            # for each country, we need to take the total emissions allotted from
            # the end of the time frame and subtract the amount it started with.
            y = dataset[str(timeEnd)] - dataset[str(timeBegin)]
            # remove countries that have a value of zero
            y = y[y > 0]

            print("\nEmissions (tons) created during", timeBegin, "-", timeEnd)
            print(y)

            plt.bar(y.index, y)
            plt.show()


if __name__ == '__main__':

    print("Emission Dataset Info:")
    dataset_info("emission data.csv")

    print("\nTop 10 countries by emissions:")
    top10_dict = top_countries("emission data.csv")
    for x, y in top10_dict.items():
        print(x, y)

    print("\nBottom 10 countries by emissions:")
    bot10_dict = bottom_countries("emission data.csv")
    for x, y in bot10_dict.items():
        print(x, y)

    print("\nEmissions of top countries over time (Fig 1):")
    top_emissions_over_time("emission data.csv", top10_dict)

    print("\nEmissions of bottom countries over time (Fig 2):")
    bot_emissions_over_time("emission data.csv", bot10_dict)

    print("\nPercent of world emissions made up by the top 10 countries:")
    emission_percent_of_world("emission data.csv", top10_dict)

    over_0 = emissions_over_0("emission data.csv")
    for x, y in over_0.items():
        print(x, "had emissions over 0 tons starting in:", y)

    print("\nGrowth of top countries in different time periods:")
    time_period_growth("emission data.csv", top10_dict)

    print("\nGrowth of bottom countries in different time periods:")
    time_period_growth("emission data.csv", bot10_dict)

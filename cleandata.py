import numpy as np
import pandas as pd
from datetime import datetime


class data:
    def __init__(self, filename=None, df=None):
        if filename is not None:
            self.df = pd.read_csv(filename)
        else:
            self.df = df

    def dropColumns(self, col):
        self.df.drop(col, inplace=True, axis=1)

    def splitStateCounty(self, colname):
        separated = self.df[colname].str.split(pat="-", expand=True)
        self.df[["state", "county"]] = separated[separated.columns[0:2]]
        self.df.drop(colname, inplace=True, axis=1)

    def convertDateMonthFirst(self, dates):
        for i, d in enumerate(dates):
            if '/' in d:
                dates[i] = datetime.strptime(d, '%m/%d/%Y')
            elif '-' in d:
                dates[i] = datetime.strptime(d, '%m-%d-%Y')
        return dates

    def convertDateYearFirst(self):
        dates = np.asarray(self.df['date'])
        for i, d in enumerate(dates):
            if '/' in d:
                dates[i] = datetime.strptime(d, '%Y/%m/%d')
            elif '-' in d:
                dates[i] = datetime.strptime(d, '%Y-%m-%d')
        self.df['date'] = dates

    def rowPerDay(self, variable_name):
        state = [[s] * 356 for s in self.df['state']]
        state = [s for sublist in state for s in sublist]
        county = [[c] * 356 for c in self.df['county']]
        county = [c for sublist in county for c in sublist]
        dates = self.convertDateMonthFirst(np.tile(self.df.columns[0:356], len(self.df.index)))
        val = self.df[self.df.columns[0:356]].values.flatten()
        self.df = pd.DataFrame(data={'state': state, 'county': county, 'date': dates, variable_name: val})

    def dropZeroRow(self):
        self.df.drop(
            np.asarray(np.where(self.df.loc[:, self.df.columns != 'county name'].eq(0).all(1))[0]))

    def changeColName(self, i, new_name):
        new_col = self.df.columns.values
        new_col[i] = new_name
        self.df.columns = new_col


if __name__ == '__main__':
    confirmed = data('./data/confirmed_case.csv')
    confirmed.dropZeroRow()
    confirmed.splitStateCounty('county name')
    confirmed.rowPerDay('confirmed')

    death = data('./data/death.csv')
    death.dropZeroRow()
    death.splitStateCounty('county name')
    death.rowPerDay('death')

    mobility_20 = data('./data/2020_mobility.csv')
    mobility_21 = data('./data/2021_mobility.csv')
    mobility = data(df=mobility_20.df)
    mobility.df = mobility.df.append(mobility_21.df)
    cols = ['country_region_code',
            'country_region', 'metro_area',
            'iso_3166_2_code',
            'census_fips_code',
            'place_id']
    mobility.dropColumns(cols)
    mobility.changeColName(0, 'state')
    mobility.changeColName(1, 'county')
    mobility.convertDateYearFirst()

    vaccinations = data('./data/vaccinations.csv')
    vaccinations.dropColumns('share_doses_used')

    # Write cleaned data to csv
    confirmed.df.to_csv('./data/confirmed_clean.csv', index=False)
    death.df.to_csv('./data/death_clean.csv', index=False)
    mobility.df.to_csv('./data/mobility_clean.csv', index=False)
    vaccinations.df.to_csv('./data/vaccinations_clean.csv', index=False)

    print()

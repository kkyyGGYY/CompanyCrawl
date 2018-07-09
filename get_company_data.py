from pandas import DataFrame, Series
import numpy as np
import pandas as pd


class Company:
    def __init__(self):
        df = pd.read_csv('companydata.csv')
        self.COM_LIST = df.iloc[:, 0].values

    def get_company_name_list(self):
        company_name_list = []
        for name in self.COM_LIST:
            if ' ' in name:
                name = ''.join(name.split(' '))
            company_name_list.append(name)
        return company_name_list


class Company_excel:
    def __init__(self):
        self.list_1 = pd.read_excel('在管主体名录.xlsx').iloc[:, -1]

    def get_company_name_list(self):
        return [x.strip() for x in list(self.list_1.dropna())]

if __name__ == '__main__':
    company = Company()
    print(company.get_company_name_list())
    a = Company_excel()
    print(a.get_company_name_list())

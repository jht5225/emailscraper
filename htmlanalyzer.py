from bs4 import BeautifulSoup
import pandas as pd
class HtmlAnalyzer:

    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
    
        self.info = {}
        self.__find_info()

    def __find_info(self):
        tables = self.soup.find_all("table")
        if tables:
            self.table_data = {}
            self.tables = tables
            self.__scrape_tables()

    def __scrape_tables(self):
        for table in self.tables:
            self.__scrape_table(table)
    
    def __scrape_table(self, table):
        dfs = pd.read_html(str(table))
        for df in dfs:
            self.__process_df(df)

    def __process_df(self, df):
        self.rows = {}
        if len(df.columns) < 3:
            self.__process_index(df)
        else:
            self.__process_table(df)
        print(self.rows)

    def __process_index(self, df):
        temp_rows = []
        for row in df.values:
            if all(isinstance(item,str) for item in row):
                if all(':' in item for item in row):
                    for item in row:
                        temp_rows.append(item)
                elif any(':' in item for item in row):
                    temp_rows.append(' '.join(row))
        for row in temp_rows:
            split_row = row.split(':')
            if len(split_row) > 1:
                self.rows[split_row[0]] = split_row[1]

    def __process_table(self, df):
        if len(df) > 1:
            for i in range(len(df.values[0])-1):
                self.rows[df.values[0][i]] = df.values[1][i]
    
    
    def get_info(self):
        return self.rows
        
        
import statistics as stat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class stati():

    def __init__(self , df = None):
        self.df = df
        #change_df = self.make_change_df()
        #self.change_df = self.make_change_df()


    def pct_change(self,old_value,new_value):
        return ((new_value-old_value)/abs(old_value))*100

    def dol_change(self,old_value,new_value):
        return new_value - old_value

    def get_values(self,col):
        """
        Gets the first and last nonnan values from a column in the dataframe

        Parameters:
        col (Pandas DataFrame): Column from the pandas data frame

        Returns:
        old_value (float): First non nan value in column
        new_value (float): Last non nan value in column
        """

        for val in col:
            if ~(np.isnan(val)):
                #print(val)
                old_value = val
                #print(old_value)
                break

        for val in reversed(list(col)):
            if ~(np.isnan(val)):
                new_value = val
                break

        return old_value,new_value
    

    def make_change_df(self):
        """
        Calculates the percent change and dollar change of each interval for the stock and puts it in a dataframe

        Returns:
        change_df (Pandas DataFrame): index is year and columns are percent change and dollar change
        """
        cols = [col for col in list(self.df.columns) if not self.df[col].isna().all()] #If it is a newer stock some intervals are completely NaN and we want to exclude these from our calculations
        change_df = pd.DataFrame(columns = ["Percent Change","Dollar Change"], index = cols)
        #cols = list(self.df.columns)
        for col in cols:
            #if self.df[col].isna().all() != True: #If it is a newer stock some intervals are completely NaN and we want to exclude these from our calculations
            old_value,new_value = self.get_values(self.df[col])
            change_df.loc[col] = [self.pct_change(old_value,new_value),self.dol_change(old_value,new_value)]
        return change_df
    

    def sort_pos_neg(self,change_df):
        """
        Sorts the positive and negative pct changes and dollar changes so they can be used for further calculations
        
        Parameters:
        change_df (Pandas DataFrame): Change dataframe with the intervals' pct change and dol change
        
        Returns:
        pct_change_dict (dict): {'pos':[pos percent changes],'neg': [neg percent changes]}
        dol_change_dict (dict): {'pos':[pos dol changes],'neg': [neg dol changes]}
        """

        pct_change_dict = {'pos': [],'neg':[]}
        dol_change_dict = {'pos': [],'neg':[]}
        for row in change_df.iterrows():
        
            pct_val = row[1]['Percent Change']
            dol_val = row[1]['Dollar Change']

            if pct_val > 0:
                pct_change_dict['pos'].append(pct_val)
            if pct_val < 0:
                pct_change_dict['neg'].append(pct_val)
            if dol_val > 0:
                dol_change_dict['pos'].append(dol_val)
            if dol_val < 0:
                dol_change_dict['neg'].append(dol_val)

        return pct_change_dict,dol_change_dict
    

    def make_stats_df(self,index):
        """
        Computes more in depth stats based on all of the intervals, i.e. all of the columns in the Historical Dataframe.
        These statistics include: "Avg_pct_change","Avg_pos_pct_change","Avg_neg_pct_change","Avg_change","Avg_pos_change",
        "Avg_neg_change","Num_pos_change","Pct_num_pos_change","Num_neg_change","pct_num_neg_change"

        Parameters:
        change_df (Pandas DataFrame): Change dataframe with each of the intervals' pct change and dol change
        index (Any | String): The index you want for the currents stocks computed statistics. Typically the ticker

        Returns:
        stats_df (Pandas DataFrame): index x stats_cols. Only returns 1 row df so be careful if going through a loop.
        """
        change_df = self.make_change_df()

        stats_cols = ["Avg_pct_change","Avg_pos_pct_change","Avg_neg_pct_change","Avg_change","Avg_pos_change","Avg_neg_change","Num_pos_change","Pct_num_pos_change","Num_neg_change","pct_num_neg_change"]
        stats_df = pd.DataFrame(index = [index], columns=stats_cols) #If this is put through a for loop it will keep getting reset

        pct_change_dict, dol_change_dict =  self.sort_pos_neg(change_df)

        avg_pct_change = np.nanmean(change_df["Percent Change"])
        avg_pos_pct_change = stat.mean(pct_change_dict['pos']) if len(pct_change_dict['pos']) != 0 else 0
        avg_neg_pct_change = stat.mean(pct_change_dict['neg']) if len(pct_change_dict['neg']) != 0 else 0

        avg_change = np.nanmean(change_df["Dollar Change"])
        avg_pos_change = stat.mean(dol_change_dict['pos']) if len(dol_change_dict['pos']) != 0 else 0
        avg_neg_change = stat.mean(dol_change_dict['neg']) if len(dol_change_dict['neg']) != 0 else 0

        num_pos_change = f"{len(pct_change_dict['pos'])}/{len(change_df)}"
        pct_num_pos_change = len(pct_change_dict['pos'])/len(change_df) if len(change_df) != 0 else 0

        num_neg_change = f"{len(pct_change_dict['neg'])}/{len(change_df)}"
        pct_num_neg_change = len(pct_change_dict['neg'])/len(change_df) if len(change_df) != 0 else 0

        stats_df.loc[index] = [avg_pct_change,avg_pos_pct_change,avg_neg_pct_change,avg_change,avg_pos_change,avg_neg_change,num_pos_change,pct_num_pos_change,num_neg_change,pct_num_neg_change]

        return stats_df
    

    def make_sudoHist(self,full_df,ticker):
        """
        Extract the provided tickers dataframe from the full_df and format it so it looks like the natural hist

        full_df (Pandas DataFrame): The full df from my_csvs
        ticker (str): The tickers hist you want to extract

        Returns:
        sudoHist(Pandas DataFrame): Same format as yfinance hist so should work with all my methods
        
        """
        full_df['Date'] = pd.to_datetime(full_df['Date'])
        sudoHist = full_df[['Date',f'Close_{ticker}',f'Volume_{ticker}']].set_index('Date')
        column_mapping = {f'Close_{ticker}': 'Close', f'Volume_{ticker}': 'Volume'}
        sudoHist.rename(columns=column_mapping,inplace=True)
        return sudoHist
    
    def full_stati_df(self,cat_option,close_or_vol,date_method,intervals_back,year = None, quarter = None, month = None,start_datetime = None, end_datetime = None):
        """
        Makes the full statisical dataframe for all of the stocks in a specified category. Makes the calculations based on the intervals you want.
        
        Parameters:
        cat_option (str): Stock Category you want. i.e. "S&P","Russell2000","NASDAQ100","S&PRealEstate",...
        close_or_vol (str): "Close" or "Volume"
        date_method (str): "year_year","year_month","year_weekday", ...
        intervals_back (int): Number of intervals back you want

        Other Parameters:
        year,quarter,month,start_datetime,end_datetime (int or DateTime): Default None. Specify according to what method you are using

        Returns:
        multi_ss_df (Pandas DataFrame): Multiple Stocks Statistics DataFrame. Index = ticker, 
        columns = "Avg_pct_change","Avg_pos_pct_change","Avg_neg_pct_change","Avg_change","Avg_pos_change","Avg_neg_change","Num_pos_change","Pct_num_pos_change","Num_neg_change","pct_num_neg_change"
        """
        from byDatesClass import byDates
        stocks = pd.read_csv("my_csvs/stock_categories.csv")
        tickers = list(stocks[stocks[cat_option].notna()][cat_option])
        full_cat_data = pd.read_csv("my_csvs/"+cat_option+".csv")
        stats_cols = ["Avg_pct_change","Avg_pos_pct_change","Avg_neg_pct_change","Avg_change","Avg_pos_change","Avg_neg_change","Num_pos_change","Pct_num_pos_change","Num_neg_change","pct_num_neg_change"]
        multi_ss_df = pd.DataFrame(columns = stats_cols )
        for ticker in tickers:
            
            hist = self.make_sudoHist(full_cat_data,ticker) 
            date_obj = byDates(hist,close_or_vol)
            date_obj.choose_interval(interval_str = date_method,intervals_back=intervals_back,year=year, quarter=quarter, month=month ,start_datetime=start_datetime, end_datetime=end_datetime)
            stats_df = date_obj.make_stats_df(ticker)

            multi_ss_df = pd.concat([multi_ss_df,stats_df])

        return multi_ss_df
    
    def filter_stat_data(self,the_stats,stat_to_filter_on:str,num_results:int,largest_or_smallest:bool):
        """
        Filter out the data so that you can get the n-smallest or n-largest rows based on a value.

        Parameters:
        the_stats (Pandas DataFrame): the dataframe we are filtering. Typically the Multi Stocks Stats DF.
        stat_to_filter_on (str): The column from the dataframe that you want to filter on. i.e. Avg_pct_change, Pct_num_pos_change,...
        num_results (int): how many results you want to retreive
        largest_or_smallest (bool): True:'largest' or False:'smallest'
        
        Returns:

        """
        the_stats[stat_to_filter_on] = the_stats[stat_to_filter_on].astype('float')

        if largest_or_smallest:
            return the_stats.nlargest(num_results,stat_to_filter_on,'all')
        else:
            return the_stats.nsmallest(num_results,stat_to_filter_on,'all')
        

    def bar_plotter(self,category,stat,largest_smallest,num_results,datatype,interval_str,intervals_back,year = None, quarter = None, month = None,start_datetime = None, end_datetime = None):
        """
        This method makes a barchart out of all the stocks from a specific index, such as the S&P, NASDAQ100, Russell2000, and S&P Sectors
        based off a specific time frame of your choosing.
        It calculates the statistic you want to check for and filters how many observations you want to see.

        Parameters:
        category (str): Index you want to pull data from: S&P, NASDAQ100, Russell2000, and S&P Sectors, formatted as 'S&PSectorName.csv'
        stat (str): Statistic you want to plot: "Avg_pct_change","Avg_pos_pct_change","Avg_neg_pct_change","Avg_change","Avg_pos_change","Avg_neg_change","Pct_num_pos_change","pct_num_neg_change
        largest_smallest (bool): Do you want to see the top movers in the category (True), or lowest movers (False)
        num_results (int): How many observations do you want plotted. Top 10? Bottom 15?
        datatype (str): 'Close','Volume','Open'... Used for instianating the byDates object
        interval_str (str): yearly_year,yearly_quarter,... 
        intervals_back(int): How many intervals back you want your time frame from
        Other Parameters: byDates.choose_method params: year, month, quarter...

        Returns:
        image_base64 (Base64 Matplotlib Plot): Bar Chart of your selected data
        """
        #stats_inst should be replaced by self
        stats_df = self.full_stati_df(cat_option=category,close_or_vol=datatype,date_method = interval_str,intervals_back = intervals_back,year=year, quarter=quarter, month=month ,start_datetime=start_datetime, end_datetime=end_datetime)

        #self in front of filter_stat_data, I think needa add this to class too
        filtered_df = self.filter_stat_data(stats_df,stat,num_results,largest_smallest)
        
        #Make title for plot
        if largest_smallest:
            word = "Highest"
        else:
            word = "Lowest"

        title = category + " " + word + " " + str(num_results) + " " + stat


        y = list(reversed(filtered_df.index))
        width = list(reversed(filtered_df[stat]))

        fig, ax = plt.subplots(figsize = (8,int(num_results/2)))
        #plt.subplots_adjust(top=0.9)
        fig.set_facecolor('none')

        ax.barh(y= y,width = width, edgecolor='none',color = '#0b89bf')  # Set edgecolor to 'none' to remove the border

        #fig.suptitle(title, fontsize=14,x = .25,color= 'white')
        ax.set_title(title,loc = 'left', fontsize = 20,color='white')
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_facecolor('none')
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.tick_params(axis='y', colors='white')
        for index, value in enumerate(width):
            ax.text(value, index, " " + str(round(value,2))+'%',color = "white")
        ax.set_ylim(bottom=0)
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

    # Convert the image to a Base64-encoded string
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return image_base64


        

        


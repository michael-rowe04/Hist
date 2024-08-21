from global_methods import global_methods
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime,timedelta
import calendar
from historical_stats import stati

class byDates(global_methods,stati):
    def __init__(self,hist,value_to_retrieve):
        """
        Send in the yfinance dataframe along with what type of values you would like to retrieve and perform many different methods on them.

        Parameters:
        hist (Pandas DataFrame): yfinance default history dataframe
        values_to_retrieve (str): What data you would like to see. i.e. "Close", "Volume", "Open", "High", "Low", "RSI"...
        """
        #super().__init__()
        self.hist = hist
        self.value_to_retrieve = value_to_retrieve #Eventually will add the technical indicators in here and will append those to the self df with the corresponding column name

    def return_value(self):
        return self.value_to_retrieve
    
    def by_year_year(self,start_year,years_back):
        """
        Gives us the yearly close data for years_back years
        
        Parameters:
        start_year (int): Starting year of data
        years_back (int): Number of years back you would like to retrieve

        Returns:
        year_year_df (Pandas DataFrame): Year long close data with index = "d-m" and columns = year

        """

        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        #This allows your data to be from multiple months
        date_range = pd.date_range(start=datetime(2023,1,1), end=datetime(2023,12,31))
        year_year_df = pd.DataFrame(index = date_range)
        year_year_df.index = pd.to_datetime(year_year_df.index).strftime('%m-%d')

        for i in range(years_back):
            if i != 0: 
                start_year = start_year - 1

            curr_interval_start = datetime(start_year,1,1).date()
            curr_interval_end = datetime(start_year,12,31).date()

            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%m-%d')

            #Insert each new column as first column. This way it goes oldest to most recent     
            year_year_df.insert(0, start_year, curr_data[self.value_to_retrieve])

        super().__init__(year_year_df)

    def by_year_quarter(self,quarter,start_year,years_back):
        """
        Creates a dataframe of stocks close prices of the specfied quarter for the specified number of years back

        Parameters:
        quarter (int): Q1 = 0,...Q4=3. The quarter you would like to retrieve data from
        years_back (int): The number of years back you would like to see data from this quarter for. Starts at present year.
        hist_df (pandas_df): Can just use self.df once in class

        Returns:
        year_quarter_df (Pandas Dataframe): Data
        """

        month_day_index = self.year_quarter_index(quarter)
        year_q_df = pd.DataFrame(index = month_day_index)

        for i in range(years_back):
            if i != 0:
                start_year = start_year - 1

            curr_data = self.get_data_from_quarter(quarter,start_year,self.hist)
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%m-%d')
            #curr_data.index = curr_data.index.astype(int)

            #curr_data_fixed_index = update_index(curr_data)

            #Insert each new column as first column. This way it goes oldest to most recent     
            year_q_df.insert(0,start_year,curr_data[self.value_to_retrieve])
            #print(qq_df)

        super().__init__(year_q_df)


    def by_year_month(self,start_month,start_year,years_back):

        """
        Groups all close data of specified month for each year for years_back years

        Parameters:
        - start_month (int): The number of the month you want to filter for
        - start_year (int): Starting year of data
        - years_back (int): Number of years back you want to retrieve close data from

        Returns:
        year_month_df (Pandas DataFrame) A dataframe of day x year for that month, NaN values for days where stock market is not open.

        """
        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        year_month_index = [day for day in range(1,32)]
        year_month_df = pd.DataFrame(index = year_month_index)

        for i in range(years_back):
            if i !=0:
                start_year = start_year - 1

            curr_interval_start = datetime(start_year,start_month,1).date()
            curr_interval_end = datetime(start_year,start_month,calendar.monthrange(start_year, start_month)[1]).date()

            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            #Insert each new column as first column. This way it goes oldest to most recent     
            year_month_df.insert(0,str(start_year), curr_data[self.value_to_retrieve])

        super().__init__(year_month_df)
    

    def by_year_day(self,start_date,end_date,years_back):
        """
        DataFrame of close prices of specfied dates for each year.

        Parameters:
        start_date (DateTime): DateTime object of start date.
        end_date (DateTime): DateTime object of end date.
        years_back (int): Number of years back you would like to get data for

        Returns:
        year_day_df (Pandas DataFrame): Index of the form M-D and columns are the year
        """

        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        date_index_list = self.year_day_index(start_date,end_date)
        year_day_df = pd.DataFrame(index = date_index_list)

        start_date_year = start_date.year
        end_date_year = end_date.year

        for i in range(years_back):
            if i != 0:
                start_date_year = start_date_year - 1
                end_date_year = end_date_year - 1
            
            curr_interval_start = datetime(start_date_year,start_date.month,start_date.day).date()
            curr_interval_end = datetime(end_date_year,end_date.month,end_date.day).date()
            
            #curr_data = get_data_from_quarter(quarter,start_year,hist_df)
            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%m-%d')
            #curr_data.index = curr_data.index.astype(int)

            #curr_data_fixed_index = update_index(curr_data)

            #Insert each new column as first column. This way it goes oldest to most recent     
            year_day_df.insert(0,start_date_year,curr_data[self.value_to_retrieve])
            #print(qq_df)

        super().__init__(year_day_df)

    def by_quarter_quarter(self,start_quarter,start_year,quarters_back):
        """
        Retrieves each quarters data from specified quarter for quarters_back quarter.
        
        Parameters:
        start_quarter (int): Q1 = 0, Q2 = 1, Q3 = 2, Q4 = 3
        start_year (int): Starting year you would like data from
        quarters_back (int): How many quarters back you would like data from

        Returns:
        qq_df (Pandas DataFrame): Date from entire quarters in the format of Index = 1a,2a...1b,4b... and Columns = "Qx year"
        """
        
        #this_df = pd.DataFrame(index = q_days_list)
        #Makes Unique index for each day of each of the 3months in a quarter
        q_days_lista = [str(day)+'a' for day in range(1,32)]
        q_days_listb = [str(day)+'b' for day in range(1,32)]
        q_days_listc = [str(day)+'c' for day in range(1,32)]
        q_days_list = q_days_lista + q_days_listb +q_days_listc

        #Initialize the final dataframe with the index that each column being added will follow
        qq_df = pd.DataFrame(index = q_days_list)

        for i in range(quarters_back):
            if i != 0:
                start_quarter = (start_quarter - 1) % 4
            if i!= 0 and start_quarter == 3:
                start_year = start_year - 1
            curr_data = self.get_data_from_quarter(start_quarter,start_year,self.hist)
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            curr_data_fixed_index = self.update_index(curr_data)

            #Insert each new column as first column. This way it goes oldest to most recent     
            qq_df.insert(0,"Q"+str(start_quarter+1)+" "+str(start_year),curr_data_fixed_index[self.value_to_retrieve])
            #print(qq_df)

        super().__init__(qq_df)

    def by_quarter_month(self,start_month,start_year,quarters_back):
        """
        Get monthly intervals from quarters. For example say you want March 2023, well this is the 3rd month of Q1 so it would also pull
        December (3rd month of Q4), September...
        
        Parameters: 
        start_month (int): Start month of interval
        start_year (int): Start year of interval
        quarters_back (int): Number of quarters back you would like to retrieve

        Returns:
        quarter_month_df (Pandas DataFrame): Close data with index = 1a,2a,4a,...,1b,3b,4b... and columns = "startmonth,startyear-endmonth,endyear"
        """

        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        quarter_month_index = [day for day in range(1,32)]
        quarter_month_df = pd.DataFrame(index = quarter_month_index)

        for i in range(quarters_back):

            if i != 0 and ((start_month-3)%12 == 0 or (start_month-3)%12 > start_month):
                start_year = start_year-1
            if i != 0:
                start_month = (start_month - 3)%12 if (start_month -3)%12 != 0 else 12
            
            curr_interval_start = datetime(start_year,start_month,1).date()
            curr_interval_end = datetime(start_year,start_month,calendar.monthrange(start_year, start_month)[1]).date()

            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            #Insert each new column as first column. This way it goes oldest to most recent     
            quarter_month_df.insert(0, str(start_month)+ ", " + str(start_year), curr_data[self.value_to_retrieve])

        super().__init__(quarter_month_df)


    def by_quarter_day(self,start_date,end_date,quarters_back):
        """
        Get intervals based on the number day for each quarter. For example say you want Feb 2nd 2023 to March 3rd 2023,
        it would give you this interval and Nov. 2nd 2022 to Dec. 3rd 2022, August 2nd 2022 to September 3rd 2022...
        
        Parameters: 
        start_date (datetime): Start date of interval
        end_date (datetime): end date of interval
        quarters_back (int): Number of quarters back you would like to retrieve

        Returns:
        quarter_day_df (Pandas DataFrame): Close data with index = 1a,2a,4a,...,1b,3b,4b... and columns = "xx/xx/xxxx-yy/yy/yyyy"
        
        """

        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        #This allows your data to be from multiple months
        date_range = pd.date_range(start=start_date, end=end_date)
        quarter_day_df = pd.DataFrame(index = date_range)
        quarter_day_df.index = pd.to_datetime(quarter_day_df.index).strftime('%d')
        quarter_day_df.index = quarter_day_df.index.astype(int)
        quarter_day_df = self.update_index(quarter_day_df)

        start_date_year = start_date.year
        end_date_year = end_date.year

        start_date_month = start_date.month
        end_date_month = end_date.month
        

        for i in range(quarters_back):

            if i != 0 and ((start_date_month-3)%12 == 0 or (start_date_month-3)%12 > start_date_month):
                start_date_year = start_date_year - 1
            if i!= 0 and ((end_date_month-3)%12 == 0 or (end_date_month-3)%12 > end_date_month):
                end_date_year = end_date_year - 1
            if i != 0:
                start_date_month = (start_date_month - 3)%12 if (start_date_month -3)%12 != 0 else 12
                end_date_month = (end_date_month - 3)%12 if (end_date_month - 3)%12 != 0 else 12
            

            length_of_end_date_month = calendar.monthrange(end_date_year, end_date_month)[1]
            length_of_start_date_month = calendar.monthrange(start_date_year, start_date_month)[1]
            
            #This takes care of if the interval uses days that are not in other months i.e. not all months have 31 days, so cannot create a datetime object for Nov. 31st
            if start_date.day > length_of_start_date_month:
                curr_interval_start = datetime(start_date_year,start_date_month,length_of_start_date_month).date()
            else:
                curr_interval_start = datetime(start_date_year,start_date_month,start_date.day).date()

            if end_date.day > length_of_end_date_month:
                curr_interval_end = datetime(end_date_year,end_date_month,length_of_end_date_month).date()
            else:
                curr_interval_end = datetime(end_date_year,end_date_month,end_date.day).date()
            
            #curr_data = get_data_from_quarter(quarter,start_year,hist_df)
            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            #print(curr_data)
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            curr_data_fixed_index = self.update_index(curr_data)

            #Insert each new column as first column. This way it goes oldest to most recent     
            quarter_day_df.insert(0,str(curr_interval_start) + " - " + str(curr_interval_end),curr_data_fixed_index[self.value_to_retrieve])

        super().__init__(quarter_day_df)


    def by_month_month(self,month,year,months_back):
        """
        Get entire months data for months_back months from starting month
        
        Parameters:
        month (int): Starting month you would like to see data from
        year (int): The starting year for the month that you want to see
        months_back (int): How many previous months' data you would like to see
        hist_df (Self.hist)
        
        Returns:
        month_month_df (PandasDataFrame): Dataframe of close data with index of days = [1,2...31] and columns = "month,year" 
        """

        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        month_month_index = [day for day in range(1,32)]
        month_month_df = pd.DataFrame(index = month_month_index)

        for i in range(months_back):

            if i != 0:
                month = (month-1)%12 if (month-1)%12 != 0 else 12
                if month == 12:
                    year = year - 1
            
            curr_interval_start = datetime(year,month,1).date()
            curr_interval_end = datetime(year,month,calendar.monthrange(year, month)[1]).date()

            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            #Insert each new column as first column. This way it goes oldest to most recent     
            month_month_df.insert(0, str(month)+ ", " + str(year), curr_data[self.value_to_retrieve])

        super().__init__(month_month_df)

        

    def by_month_day(self,start_date,end_date,months_back):
        """
        Get monthly data based on the number day of the input data. For example if you want monthly data from the input dates of
        December 12 2023 - Jan 4 2024 the intervals you will recieve the data for are Nov 12 2023 - Dec 4th 2023, Oct 12 2023 - Nov 4th 2023...
        for however many months back you want date

        Parameters:
        start_date (DateTime): Start date of your interval
        end_date (DateTime): End date of your interval
        months_back (int): Number of months back you would like to retrieve data for

        Returns:
        month_day_df (Pandas DataFrame): Close data with index 1a,2a,4a,...1b,2b,3b,... and columns "dd/mm/yyyy-dd/mm/yyyy"
        """

        #self.hist
        hist_copy = self.hist.copy()
        hist_copy.index = self.hist.index.date

        #This allows your data to be from multiple months
        date_range = pd.date_range(start=start_date, end=end_date)
        month_day_df = pd.DataFrame(index = date_range)
        month_day_df.index = pd.to_datetime(month_day_df.index).strftime('%d')
        month_day_df.index = month_day_df.index.astype(int)
        month_day_df = self.update_index(month_day_df)

        start_date_year = start_date.year
        end_date_year = end_date.year

        start_date_month = start_date.month
        end_date_month = end_date.month
        

        for i in range(months_back):
            if i != 0:
                start_date_month = (start_date_month - 1)%12 if (start_date_month - 1)%12 != 0 else 12
                end_date_month = (end_date_month - 1)%12 if (end_date_month - 1)%12 != 0 else 12
            if i != 0 and start_date_month == 12:
                start_date_year = start_date_year - 1
            if i!= 0 and end_date_month == 12:
                end_date_year = end_date_year - 1

            length_of_end_date_month = calendar.monthrange(end_date_year, end_date_month)[1]
            length_of_start_date_month = calendar.monthrange(start_date_year, start_date_month)[1]
            
            #This takes care of if the interval uses days that are not in other months i.e. not all months have 31 days, so cannot create a datetime object for Nov. 31st
            if start_date.day > length_of_start_date_month:
                curr_interval_start = datetime(start_date_year,start_date_month,length_of_start_date_month).date()
            else:
                curr_interval_start = datetime(start_date_year,start_date_month,start_date.day).date()

            if end_date.day > length_of_end_date_month:
                curr_interval_end = datetime(end_date_year,end_date_month,length_of_end_date_month).date()
            else:
                curr_interval_end = datetime(end_date_year,end_date_month,end_date.day).date()
            
            #curr_data = get_data_from_quarter(quarter,start_year,hist_df)
            curr_data = hist_copy.loc[curr_interval_start:curr_interval_end]
            #print(curr_data)
            curr_data.index = pd.to_datetime(curr_data.index).strftime('%d')
            curr_data.index = curr_data.index.astype(int)

            curr_data_fixed_index = self.update_index(curr_data)

            #Insert each new column as first column. This way it goes oldest to most recent     
            month_day_df.insert(0,str(curr_interval_start) + " - " + str(curr_interval_end),curr_data_fixed_index[self.value_to_retrieve])

        super().__init__(month_day_df)

    def weekday_intervals_df(self,start,end,months_or_years_back,months_or_years = False, quarters = False):
        """
        Returns a dataframe by weekday from either consecutive months or consecutive years. For example if you want the first Monday to the third Friday
        of November for 5 years back. You would get the first Monday to the third Friday for each of the 5 previous years. If you want it monthly
        you would get the first Monday to third Friday from October, September, etc.

        Parameters:
        start (DateTime): Starting date of your interval
        end (DateTime): Ending date of your interval
        months_or_years_back (int): How many years or months or quarters back you would like to retrieve from.
        months_or_years (bool): Default False. If True returns by month. If False returns by year.
        quarters (bool): Default False. If True returns by quarter, regardless of what months_or_years back is. 

        Returns:
        new_df (Pandas DataFrame): Dataframe with close data of specified stock in form of index = Weekday by columns = 
        "mm/dd/yyyy-mm/dd/yyyy" for year or month and "Qx year - Qy year" for quarters.
        """

        #Make a copy of the self.df
        hist_copy = self.hist.copy()
        hist_copy['Weekday'] = hist_copy.index.day_name()
        hist_copy.index = self.hist.index.date



        if months_or_years == True and quarters == False:
            intervals = self.get_previous_months_by_weekday(start,end,months_or_years_back)
            #method_name = 'month'

        if months_or_years == False and quarters == False:
            intervals = self.get_intervals_by_weekday_year(start,end,months_or_years_back)
            #method_name = 'year'

        if quarters == True:
            intervals = self.get_previous_quarters_by_weekday(start,end,months_or_years_back)
  
        interval1_start = datetime(intervals[0][0],intervals[0][1],intervals[0][2]).date()
        interval1_end = datetime(intervals[0][3],intervals[0][4],intervals[0][5]).date()
        

        #Make the DataFrame
        if quarters == False:
            #Since column header is gotten from a method (dynamic) have to put it in a dict first then unpack the whole dict in the assign method with **
            #new_col = {str(getattr(interval1_start, method_name)): hist_copy.loc[interval1_start:interval1_end]['Close']}
            new_col = {str(interval1_start) + " - " + str(interval1_end): hist_copy.loc[interval1_start:interval1_end][self.value_to_retrieve]}
        
        else:
            new_col = {self.get_quarter_for_datetime(interval1_start)+", "+ str(interval1_start.year) + " - " + self.get_quarter_for_datetime(interval1_end)+ ", " +str(interval1_end.year) : hist_copy.loc[interval1_start:interval1_end][self.value_to_retrieve]}
        new_df = pd.DataFrame()
        new_df = new_df.assign(Weekday = hist_copy.loc[interval1_start:interval1_end]['Weekday'],**new_col)
        new_df = new_df.set_index('Weekday')
        new_df.reset_index(inplace = True)
            
        for interval_index in range(1,len(intervals)):

            #Iterate through the rest of the intervals
            current_interval_start = datetime(intervals[interval_index][0],intervals[interval_index][1],intervals[interval_index][2]).date()
            current_interval_end = datetime(intervals[interval_index][3],intervals[interval_index][4],intervals[interval_index][5]).date()
            

            #Make DataFrame of current interval and attach it to the DataFrame
            new_column_df = pd.DataFrame(data=hist_copy.loc[current_interval_start:current_interval_end][[self.value_to_retrieve,'Weekday']]).set_index('Weekday') 
            new_column_df.reset_index(inplace = True)
            if quarters == False:
                #If we want to change column header to month,year I dont think we need the get attr part
                #new_df[str(getattr(current_interval_start, method_name))] = new_column_df['Close']
                new_df[str(current_interval_start)+" - "+ str(current_interval_end)] = new_column_df[self.value_to_retrieve]
            else:
                new_df[self.get_quarter_for_datetime(current_interval_start)+", "+ str(current_interval_start.year) + " - " + self.get_quarter_for_datetime(current_interval_end)+ ", " +str(current_interval_end.year)] = new_column_df[self.value_to_retrieve]
            new_df.insert(1,'Weekday'+str(interval_index),new_column_df['Weekday'])
            

            #Essentially NaN handling. Makes sure weekdays always line up
            if quarters == False:
                #possible_columns_to_shift = [[next(iter(new_col)),'Weekday'],[str(getattr(current_interval_start, method_name)),'Weekday'+str(interval_index)]]
                possible_columns_to_shift = [[next(iter(new_col)),'Weekday'],[str(current_interval_start)+" - "+ str(current_interval_end),'Weekday'+str(interval_index)]]
            else:
                possible_columns_to_shift = [[next(iter(new_col)),'Weekday'],[self.get_quarter_for_datetime(current_interval_start)+ ", "+ str(current_interval_start.year) + " - " + self.get_quarter_for_datetime(current_interval_end)+ ", " +str(current_interval_end.year),'Weekday'+str(interval_index)]]
            new_df = self.shift_df(new_df,possible_columns_to_shift)
            new_df.drop('Weekday'+str(interval_index),axis=1,inplace = True)
        
        new_df.set_index('Weekday',inplace=True)
        #new_df.index = pd.Categorical(new_df.index, categories=pd.unique(new_df.index), ordered=True)
        super().__init__(new_df)


    def get_data_from_quarter (self,quarter,year,hist_df):
        """
        Helper function. Retrieves the close data from the specified quarter and year

        Parameters:
        quarter (int): Q1 = 0, Q2 = 1, Q3 = 2, Q4 = 3
        year (int): Specified year you want data from
        
        Returns:
        quarter_df (Pandas DataFrame): Dataframe with QX column and TBD index (Currently Date)
        """
        hist_df_copy = hist_df.copy()
        #hist_df_copy['Weekday'] = hist_df_copy.index.day_name()
        hist_df_copy.index = hist_df.index.date
        
        #Q1 = 0,Q2 =1, Q3 = 2, Q4 = 3
        quarters = {0:{'Start':{'Month':1,'Day':1},'End':{'Month':3,'Day':31}},1:{'Start':{'Month':4,'Day':1},'End':{'Month':6,'Day':30}},2:{'Start':{'Month':7,'Day':1},'End':{'Month':9,'Day':30}},3:{'Start':{'Month':10,'Day':1},'End':{'Month':12,'Day':31}}}
        qstart = datetime(year,quarters[quarter]['Start']['Month'],quarters[quarter]['Start']['Day']).date()
        qend= datetime(year,quarters[quarter]['End']['Month'],quarters[quarter]['End']['Day']).date()
        quarter_df = hist_df_copy.loc[qstart:qend]

        return quarter_df
    
    def update_index(self,column_df):
        """
        Helper function. Replaces the days index that has repetions with a new unique index. Used for retrieving quarters for quarters back.
        Since each quarter has 3 months the quarter df passed in will have its days index converted to 1a,2a,5a,... for the first month of the quarter,
        3b,4b,6b... for the 2nd month and c's for the 3rd month.

        Parameters: 
        column_df (Pandas DataFrame): A quarters df with the index as just days that are converted to integers.

        Returns: 
        new_column_df (Pandas DataFrame): New DataFrame with new unique indices as specified above. Can now be easily added to the final dataframe
        
        """

        new_index = []
        next_index_tracker = 1
        current_letter = 'a'
        for old_index in column_df.index:
            if old_index <= column_df.index[next_index_tracker]:
                new_index.append(str(old_index)+current_letter)
            else:
                new_index.append(str(old_index)+current_letter)
                current_letter = chr(ord(current_letter) + 1)
            if next_index_tracker < len(column_df)-1:
                next_index_tracker += 1
        new_column_df = column_df.copy()
        new_column_df['new_index'] = new_index
        new_column_df.set_index('new_index',inplace = True)
        return new_column_df
    

    def year_quarter_index(self,quarter):
        """
        Helper Function. Makes the index for the dataframe for retrieivng a specific quarter from each year
        
        Parameters:
        quarter (int): The quarter you are tring to retrieve frome. Q1 = 0,...,Q4=3

        Returns:
        date_index_list (list): List of what the final dataframes index should be. Month-Date format.
        """
        quarters = {0:{'Start':{'Month':1,'Day':1},'End':{'Month':3,'Day':31}},1:{'Start':{'Month':4,'Day':1},'End':{'Month':6,'Day':30}},2:{'Start':{'Month':7,'Day':1},'End':{'Month':9,'Day':30}},3:{'Start':{'Month':10,'Day':1},'End':{'Month':12,'Day':31}}}
        day_of_quarter = datetime(2023,quarters[quarter]['Start']['Month'],quarters[quarter]['Start']['Day'])
        end_of_quarter = datetime(2023,quarters[quarter]['End']['Month'],quarters[quarter]['End']['Day'])

        date_index_list = []

        while day_of_quarter != end_of_quarter + timedelta(days=1):
            date_index_list.append(day_of_quarter.date().strftime('%m-%d'))
            day_of_quarter = day_of_quarter + timedelta(days = 1)


        return date_index_list



    def year_day_index(self,start_date,end_date):
        """
        Helper function. Makes the index for the dataframe for retrieivng a specific interval of days for each year.
        
        Parameters:
        start_date (DateTime): Start date of the interval
        end_date (DateTime): End date of the interval

        Returns:
        date_index_list (list): List of what the final dataframes index should be. Month-Date format.
        """
        date_index_list = []

        while start_date != end_date + timedelta(days=1):
            date_index_list.append(start_date.date().strftime('%m-%d'))
            start_date = start_date + timedelta(days = 1)


        return date_index_list
    
    def get_previous_quarters_by_weekday(self,input_data,end_data,quarters_back):
        """
        Retrieves the interval given for every quarter back for as long as specified. 
        If you want data from December 14th, the 2nd Thursday of December which is the third month in Q4, to December 21st this will give you
        the 2nd Thursday from the third month of each quarter to 7 days after the 2nd Thursday for each month.

        Parameters:
        input_data (datetime): Start day of your interval
        end_data (datetime): End day of your interval
        months_back (int): How many quarters prior you would like to get data from

        Returns:
        intervals (list[list]): List of all of the intervals starting with the earliest month 
        Intervals of the form [startyear,startmonth,startday,endyear,endmonth,endday]
        """

        start_month,start_year = input_data.month,input_data.year
        new_weekday_counter = self.weekday_counter_func(input_data)
        days_between = end_data-input_data
        intervals = []

        for i in range(quarters_back):

            if i != 0 and ((start_month-3)%12 == 0 or (start_month-3)%12 > start_month):
                start_year = start_year-1
            if i != 0:
                start_month = (start_month - 3)%12 if (start_month -3)%12 != 0 else 12

            this_months_data = datetime(start_year,start_month,1)

            temp_weekday_counter = 0
            while temp_weekday_counter != new_weekday_counter:
                if input_data.weekday() == this_months_data.weekday():
                    temp_weekday_counter += 1
                this_months_data = this_months_data + timedelta(days = 1)
            #Once it has counted all of its days it is tacking on another one so need to over correct
            this_months_data = this_months_data - timedelta(days=1)   

            #month,year = (month-1%12,year) if month-1%12 != 0 else (12,year-1 if month== 1 else year) #I think this still accounts for case when first month is 12

            end_this_months_data = this_months_data + days_between #does this prevent us from going into different months? No it shouldnt since it is a datetime method
            intervals.append([this_months_data.year,this_months_data.month,this_months_data.day,end_this_months_data.year, end_this_months_data.month ,end_this_months_data.day])
        
        
        intervals.reverse()
        return intervals 


    def get_quarter_for_datetime(self,datetime_obj):
        """
        Used mainly for naming the column headers when creating the DataFrame. It gives you what fisical quarter a date is in

        Parameters:
        datetime_obj (datetime): Date you want to check quarter for

        Returns:
        (str): "Q1","Q2","Q3", or "Q4"
        
        """
        quarters = {0:{'Start':{'Month':1,'Day':1},'End':{'Month':3,'Day':31}},1:{'Start':{'Month':4,'Day':1},'End':{'Month':6,'Day':30}},2:{'Start':{'Month':7,'Day':1},'End':{'Month':9,'Day':30}},3:{'Start':{'Month':10,'Day':1},'End':{'Month':12,'Day':31}}}
        
        q1 = pd.date_range(start = datetime(2023,quarters[0]['Start']['Month'],quarters[0]['Start']['Day']),end = datetime(2023,quarters[0]['End']['Month'],quarters[0]['End']['Day']))
        q1 = pd.to_datetime(q1).strftime('%m-%d')

        q2 = pd.date_range(start = datetime(2023,quarters[1]['Start']['Month'],quarters[1]['Start']['Day']),end = datetime(2023,quarters[1]['End']['Month'],quarters[1]['End']['Day']))
        q2 = pd.to_datetime(q2).strftime('%m-%d')

        q3 = pd.date_range(start = datetime(2023,quarters[2]['Start']['Month'],quarters[2]['Start']['Day']),end = datetime(2023,quarters[2]['End']['Month'],quarters[2]['End']['Day']))
        q3 = pd.to_datetime(q3).strftime('%m-%d')

        q4 = pd.date_range(start = datetime(2023,quarters[3]['Start']['Month'],quarters[3]['Start']['Day']),end = datetime(2023,quarters[3]['End']['Month'],quarters[3]['End']['Day']))
        q4 = pd.to_datetime(q4).strftime('%m-%d')

        if datetime_obj.strftime('%m-%d') in list(q1):
            return "Q1"
        if datetime_obj.strftime('%m-%d') in list(q2):
            return "Q2"
        if datetime_obj.strftime('%m-%d') in list(q3):
            return "Q3"
        if datetime_obj.strftime('%m-%d') in list(q4):
            return "Q4"


    def weekday_counter_func(self,input_date):
        """
        Counts the number weekday in a month a specific day is. Say you want data from December 14th this will tell you that
        that is the 2nd Thursday of December.

        Parameters:
        input_date(datetime): The start day of your interval

        Returns:
        weekday_counter (int): Count of which number weekday that is

        """
        weekday_counter = 1
        new_day = datetime(input_date.year,input_date.month,1)
        #print(new_day.weekday())
        while input_date != new_day:
            if input_date.weekday() == new_day.weekday():
                weekday_counter +=1
                #print(new_day.weekday())
            #print('hey')
            #print(new_day)
            new_day = new_day + timedelta(days = 1)
        return weekday_counter




    def get_previous_months_by_weekday(self,input_data,end_data,months_back):
        """
        Retrieves the interval given for every month back for as long as specified. 
        If you want data from December 14th, the 2nd Thursday of December, to December 21st this will give you
        the 2nd Thursday from each month to 7 days after the 2nd Thursday for each month.

        Parameters:
        input_data (datetime): Start day of your interval
        end_data (datetime): End day of your interval
        months_back (int): How many months prior you would like to get data from

        Returns:
        intervals (list[list]): List of all of the intervals starting with the earliest month i.e. 10 months back would start at February. 
        Intervals of the form [startyear,startmonth,startday,endyear,endmonth,endday]
        """
    
        month,year = input_data.month,input_data.year
        new_weekday_counter = self.weekday_counter_func(input_data)
        days_between = end_data-input_data
        intervals = []

        for i in range(months_back):
            this_months_data = datetime(year,month,1)

            temp_weekday_counter = 0
            while temp_weekday_counter != new_weekday_counter:
                if input_data.weekday() == this_months_data.weekday():
                    temp_weekday_counter += 1
                this_months_data = this_months_data + timedelta(days = 1)
            #Once it has counted all of its days it is tacking on another one so need to over correct
            this_months_data = this_months_data - timedelta(days=1)   

            month,year = (month-1%12,year) if month-1%12 != 0 else (12,year-1 if month== 1 else year) #I think this still accounts for case when first month is 12

            end_this_months_data = this_months_data + days_between #does this prevent us from going into different months? No it shouldnt since it is a datetime method
            intervals.append([this_months_data.year,this_months_data.month,this_months_data.day,end_this_months_data.year, end_this_months_data.month ,end_this_months_data.day])
        
        
        intervals.reverse()
        return intervals 
    

    def get_intervals_by_weekday_year(self,start_datetime,end_datetime,years_back,weekday_buffer = 1,intervals = [],first_time = True):
    
        """
        Appends the interval for which you selected according to day of the week. i.e. if you selected the first Monday of November
        to the 3rd Friday of November you would get this back for each year

        Parameters:
        start_datetime (DateTime Obj): datetime(start_year,start_month,start_day), day interval will be starting from
        end_datetime (DateTime Obj): datetime(end_year,end_month,end_day), day interval will be ending from
        years_back (int): How many past years of this interval you would like (Maybe should make an option for monthly)
        weekday_buffer (int): Default 1. This keeps the weekdays aligned properly. Do not change, needed for recursive.
        intervals (list[list]): Do not input, needed for recursive.
        first_time (Bool): Default True. Do not input, checks if this is the first time this instance was being called, each iteration after False will be passed
        intervals was not being cleared from memory, this ensures it is


        Returns:
        intervals (list[list]): List of all of the intervals starting with the earliest year i.e. 10 years back would start at 2013. 
        Intervals of the form [startyear,startmonth,startday,endyear,endmonth,endday]
        
        """
        
        if first_time == True:
            intervals.clear()
        
        
        if years_back !=0:
            
            intervals.append([start_datetime.year,start_datetime.month,start_datetime.day,end_datetime.year,end_datetime.month,end_datetime.day])

            weekday_buffer +=1 #To make sure pulling the correct day of week each time
            days_to_subtract = 364 if weekday_buffer%7 != 0 else 364 + 7
        
            start_datetime = start_datetime - timedelta(days=days_to_subtract)
            end_datetime = end_datetime - timedelta(days=days_to_subtract)

            self.get_intervals_by_weekday_year(start_datetime,end_datetime,years_back-1,weekday_buffer,intervals,first_time = False)
    
        #Because when using recursion the previous functions still have to to be called so technically the first function called is the last one returned
        if first_time == True:
            intervals.reverse()
            return intervals
        



    def shift_df(self,new_df,possible_columns_to_shift, i = 0):
        """
        Sometimes these intervals contain days that are not trading days, for example Labor Day. This causes for NaN values 
        which leads to indexing errors. This method checks which Column is wrong and shifts it accordingly. Currently I believe it only accounts
        for 1 consecutive trading days being off, I will have to check if it can handle multiple in a row. It can handle multiple in an interval
        I am just unsure if it handles consecutive days in an interval. Definietly cannot handle two consecutive days but I dont think that ever happens

        Parameters:
        new_df (Pandas DataFrame): The new dataframe the close prices will be added to, this should be passed in with only the first interval's data
        possible_columns_to_shift (list[list]): This is the first intervals column name along with its Weekday Column and the new_column,new_columns_weekday
        you are checking it against. Should look like [['interval1_col_name','interval1_weekday'],['new_col_name','new_weekday']]
        i (int): Default: 0. Used for recursion, stops once reached end of the the data frame

        Returns:
        new_df (Pandas DataFrame): With the columns asked to check properly aligned by Weekday
        """
        
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        if i< len(new_df):
            if new_df.values[i][0] != new_df.values[i][1]:
                #print(days_of_week.index(new_df.values[i][0]))
                if i != 0:
                    #If first column (og index) is out of place
                    if days_of_week.index(new_df.values[i][0]) != (days_of_week.index(new_df.values[i-1][0])+1)%len(days_of_week):
                        #print(days_of_week.index(new_df.values[i][0]),(days_of_week.index(new_df.values[i-1][0])+1)%len(days_of_week))
                        #need to check which column is wrong
                        #This shifts the first column and start data
                        new_df.loc[i:, possible_columns_to_shift[0]] = new_df.loc[i:, possible_columns_to_shift[0]].shift()
                        #But if the first column is wrong then it will have a NaN in it from the shift and that NaN will keep being checked against other weekdays
                        #So if the first column is wrong we fill the NaN with the correct day
                        #Have to make first column of weekdays correct, as long as it is not the first row this will work
                        new_df.at[i,possible_columns_to_shift[0][1]] = days_of_week[(days_of_week.index(new_df.values[i-1][0])+1)%len(days_of_week)]                
                    else:
                        #This shifts the new data
                        new_df.loc[i:, possible_columns_to_shift[1]] = new_df.loc[i:, possible_columns_to_shift[1]].shift()
                #Case for when first row is out of place:
                else:
                    if (days_of_week.index(new_df.values[i][0])+1)%len(days_of_week) == days_of_week.index(new_df.values[i][1]): #First col is correct because this day comes before 2nd col in the week
                        #So shift 2nd column
                        new_df.loc[i:, possible_columns_to_shift[1]] = new_df.loc[i:, possible_columns_to_shift[1]].shift()
                    else:
                        #Same Logic as before for when shifting first row
                        new_df.loc[i:, possible_columns_to_shift[0]] = new_df.loc[i:, possible_columns_to_shift[0]].shift()
                        #If it is the first row this will work
                        new_df.at[i,possible_columns_to_shift[0][1]] = days_of_week[(days_of_week.index(new_df.values[i+1][0])-1)%len(days_of_week)]


            self.shift_df(new_df,possible_columns_to_shift, i+1)

        return new_df 


    def choose_interval(self,interval_str,intervals_back, year = None, quarter = None, month = None,start_datetime = None, end_datetime = None):
        """
        Will be perform the deisred function based on a string and the normal inputs, just make sure you set them correctly.
        interval_str of the type yearly_year,...
        """
        if interval_str == 'yearly_year':
            self.by_year_year(year,intervals_back)
        elif interval_str == 'yearly_quarter':
            self.by_year_quarter(quarter, year, intervals_back)
        elif interval_str == 'yearly_month':
            self.by_year_month(month,year,intervals_back)
        elif interval_str == 'yearly_week':
            self.weekday_intervals_df(start_datetime,end_datetime,intervals_back,months_or_years=False)
        elif interval_str == 'yearly_day':
            self.by_year_day(start_datetime,end_datetime,intervals_back)
        elif interval_str =='quarterly_quarter':
            self.by_quarter_quarter(quarter,year,intervals_back)
        elif interval_str == 'quarterly_month':
            self.by_quarter_month(month,year,intervals_back)
        elif interval_str == 'quarterly_week':
            self.weekday_intervals_df(start_datetime,end_datetime,intervals_back,quarters=True)
        elif interval_str == 'quarterly_day':
            self.by_quarter_day(start_datetime,end_datetime,intervals_back)
        elif interval_str == 'monthly_month':
            self.by_month_month(month,year,intervals_back)
        elif interval_str == 'monthly_week':
            self.weekday_intervals_df(start_datetime,end_datetime,intervals_back,months_or_years=True)
        elif interval_str == 'monthly_day':
            self.by_month_day(start_datetime,end_datetime,intervals_back)

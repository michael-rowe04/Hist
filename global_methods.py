import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import mpld3
import plotly.io as pio
import plotly.tools as tls
import io
import base64
import matplotlib.ticker as xticker



class global_methods():
    def __init__(self,df):
        self.df = df

    def return_df(self):
        return self.df
    
    def print_df(self):
        print(self.df)

    def norm_interpolate_line(self,line):
        """
        Normalizes the input line to y-values between 0 and 1, then interpolates it so that NaNs become points on the straight line that connect the existing numerical values around them

        Parameters:
        Line (Panda Series): Column from Data Frame

        Returns:
        Normalized Interpolated Line (Numpy Array): Numpy Array between 0 and 1 with NaNs interpolated
        """
        #Switch to Numpy Array so source data is not changed
        my_line = np.array(line)

        # Find indices of non-NaN values
        indices = np.arange(len(my_line))
        non_nan_indices = indices[~np.isnan(my_line)]


        # Take care of cases where data starts with NaNs, just replaces them with first numerical value
        for i in range(non_nan_indices[0]):
            my_line[i] = my_line[non_nan_indices[0]]

        new_non_nan_indices = indices[~np.isnan(my_line)]

        # Use numpy.interp to perform linear interpolation
        interpolated_line = np.interp(indices, new_non_nan_indices, my_line[new_non_nan_indices])

        min_y = min(interpolated_line)
        max_y = max(interpolated_line)
        interp_normalized_line = np.array([(y - min_y) / (max_y - min_y) for y in interpolated_line])


        return interp_normalized_line
    

    def chopper(self,line1):
        """
        Helper to the_score method. Chops off extra NaNs of the line that is being compared with all the other lines
        Should be used before normalizing and interpolating the data

        Parameters:
        Line1 (Panda Series): Column that you want to get the index off for where to start chopping off NaNs

        Returns:
        i (int): The index of where to start chopping. Should be used as Line1 = Line1[:-i] and Line2 = Line2[:-i]
        None: None is returned if i<= 0.
        
        """

        line1 = np.array(line1)

        i = 1
        this = True
        while this == True:
            if np.isnan(line1[-i]):
                i += 1
            else: 
                this = False
        #i undershoots by one so have to adjust this manually with i = i-1
        i -= 1
        if i>0:
            return i
        else:
            return None
        

    def the_score(self,line1,line2,score):
        """
        Normalizes and Interpolates the columns makes, removes NaN's at the ends of lines, Returns the specified similarity score between two lines

        Parameters:
        Line1 (Panda Series): Column that every other column is being compared to
        Line2 (Panda Series): Line that will have similarity score calculated between line 1
        score (str): What type of score you want calculated. Options: "cos_score",

        Returns:
        Score (Float): Score between 0 and 1 of cosine similarity between the two lines

        """

        #Interpolated lines that start with NaNs or end with NaNs are all replaced by the closest numeric value to these NaNs
        #Might want to at least figure out a way to drop NaNs and calculate the similarity between line1[:line1start_of_nan],line2[:line1start_of_nan]

        #This is all for chopping off the extra NaN values at the end, if any.
        line1 = np.array(line1)
        line2 = np.array(line2)

        i = self.chopper(line1)
        if i != None:
            line1 = line1[:-i]
            line2 = line2[:-i]

        #Here is where the score is calculated, eventually there will be more options
        if score == "cos_score":
            #Normalized and Interpolated Numpy Array reshaped to (1,-1).
            try:
                my_col = self.norm_interpolate_line(line1).reshape(1,-1)
                current_col = self.norm_interpolate_line(line2).reshape(1,-1)
                similarity_score = cosine_similarity(my_col, current_col)
            except:
                #Since we are chopping NaNs first in very few cases it is possible that for the amount NaNs
                #We are chopping from Line1 this in turn chops all the data for Line2
                #This causes an error when it is trying to add in data for NaNs at the start
                #Honestly in cases like this we simply just do not have enough data so it is for the best that we just drop these cases
                #When we get more measurements maybe throw them all in this try catch
                return "Not Enough Data"

            return similarity_score[0][0]
        

    def plotter(self,cols,col,i):
        """
        Unfinished, still needs some clean up/neatness

        Parameters:
        df (Pandas DataFrame): DataFrame that is plotted column by column

        Returns:
        None: Shows each Columns plots one on top of another

        """
        #I feel like we are wasting a lot of space. Maybe cut borders/margins. Also anyway to keep them together in a for loop?
        #Set figure size, consistent for each sub plot
        plt.figure(figsize=(20,30))
        #Create new subplot, num rows, num cols, which number subplot (first at top)
        plt.subplot(len(cols),1,i,frameon= True)
        #Need to find a way to change color
        #Plots with NaN breaks as solid line and marker points
        plt.plot(self.df.index,self.df[col],marker = 'o',color = 'blue',lw=1.5)
        #Plots same line as dotted but connects NaN breaks
        sns.lineplot(x=self.df.index, y=self.df[col], data=self.df , linestyle = '--',c = 'blue')
        plt.xticks(self.df.index)
        plt.tight_layout()    
        #plt.show()
        #return self.fig_to_base64_string(plt)
        #return plt
        plt.show()


    def mini_app(self,score):
        """
        Mini app to plot each column and their similarity score with present column

        Parameters:
        Score (str): Similarity score to be calculated between current plot and each of the other plots. Options: "cos_score",
        
        Return:
        None: Prints plots and similarity scores
        """
        cols = list(self.df.columns.values)
        i = 1
        for col in cols:
            self.plotter(cols,col,i)
            print(score, ':', self.the_score(self.df[2023],self.df[col],score))
            i+=1

    def first_nonnan(self,col):
        for val in col:
            if ~(np.isnan(val)):
                return val
            
    def last_nonnan(self,col):      
        for val in reversed(list(col)):
            if ~(np.isnan(val)):
                new_value = val
                return new_value
            
    def pct_change(self,old_value,new_value):
        return ((new_value-old_value)/abs(old_value))*100

    def dol_change(self,old_value,new_value):
        return new_value - old_value

    def html_plotter(self,vol_df,y_label):
        """
        Plots each Column of DataFrame in the same fig object one below another

        Parameters:
        vol_df (Pandas DataFrame): Made from making a ByDates('Volume') instance so that the volume can be plotted under the line
        y_label (Str): The Value being pulled in, i.e. close, volume, high, etc. (so use the datatype)

        Returns:
        html_string: HTML embedding of the fig object
        """

        #This part reverses the columns of the dataframes so that it is plotted from most recent to oldest
        self.df = self.df[self.df.columns[::-1]]
        if (vol_df is not None):
            vol_df = vol_df[vol_df.columns[::-1]]

        cols = list(self.df.columns.values)
        fig, ax = plt.subplots(len(cols),1,figsize = (8,3.5*len(cols))) #(width,height)
        fig.set_facecolor('none')

        if len(cols) <= 1:
            ax = [ax]


        for i in range(len(cols)):
            if self.last_nonnan(self.df[cols[i]]) > self.first_nonnan(self.df[cols[i]]):
                plt_color = 'green'
                vol_color= 'mediumseagreen'
                line_color = 'darkgreen'
                #r,g,b = 0,255,0
            else:
                plt_color = 'red'
                vol_color='lightcoral'
                line_color = 'red'
                #r,g,b = 255,0,0

            if len(self.df) >= 40:
                ax[i].plot(list(range(len(self.df.index))),pd.Series(self.df[cols[i]]).interpolate(method='linear'),color = plt_color,lw=2)
                ax[i].axhline(y=self.first_nonnan(self.df[cols[i]]), color=line_color, linestyle='dashed', lw = 1.5)
            else:
                ax[i].plot(list(range(len(self.df.index))),self.df[cols[i]], color=plt_color,marker='o', markersize = 3,  lw=2)
                ax[i].plot(list(range(len(self.df.index))),pd.Series(self.df[cols[i]]).interpolate(method='linear'),linestyle = 'dashed',color = plt_color,lw=2) # mask=~np.isnan(self.df[cols[i]])
                ax[i].axhline(y=self.first_nonnan(self.df[cols[i]]), color=line_color, linestyle='dashed', lw = 1.5)
                
            if (y_label != 'Volume' and vol_df is not None):
                for t in range(len(self.df.index) - 1):
                    #ax[i].fill_between(list(range(len(df.index)))[t:t+2], 0, list(df[df.columns[i]].iloc[t:t+2].values), color=vol_color, alpha=(vol_df[vol_df.columns[i]].iloc[t]/ max(vol_df[vol_df.columns[i]])) if ~(np.isnan(vol_df[vol_df.columns[i]].iloc[t])) else 0,edgecolor = None)
                    alpha=(vol_df[vol_df.columns[i]].iloc[t]/ np.nanmax(vol_df[vol_df.columns[i]])) if ~(np.isnan(vol_df[vol_df.columns[i]].iloc[t])) else 0
                    x = list(range(len(self.df.index)))[t:t+2]
                    y1 = [np.nanmin(list(self.df[self.df.columns[i]]))/1.2,np.nanmin(list(self.df[self.df.columns[i]]))/1.2]
                    y2 = [(np.nanmin(list(self.df[self.df.columns[i]]))/10)* (vol_df[vol_df.columns[i]].iloc[t]/ np.nanmax(vol_df[vol_df.columns[i]]))+np.nanmin(list(self.df[self.df.columns[i]]))/1.2,(np.nanmin(list(self.df[self.df.columns[i]]))/10)* (vol_df[vol_df.columns[i]].iloc[t]/ np.nanmax(vol_df[vol_df.columns[i]]))+np.nanmin(list(self.df[self.df.columns[i]]))/1.2]
                    
                    ax[i].fill_between(x=x, y1 = y1, y2 = y2, color=vol_color, alpha=alpha,label = "Volume (Not to Scale)" if t ==len(self.df.index)-2 else None)

            if type(list(self.df.index)[0]) == str:
                ax[i].set_xticks(list(range(len(self.df.index))),labels = self.df.index,rotation = 60,fontsize = 8)
            else:
                ax[i].set_xticks(list(range(len(self.df.index))),labels = self.df.index,fontsize = 8)
            if len(self.df) >= 40:
                ax[i].xaxis.set_major_locator(xticker.MaxNLocator(min_n_ticks = 20,prune='both'))
                # Set the x-axis locator to AutoLocator for minor ticks
                ax[i].xaxis.set_minor_locator(xticker.MultipleLocator(1))

            ax[i].yaxis.tick_right()
            ax[i].spines['top'].set_visible(False)
            ax[i].spines['left'].set_visible(False)
            
            ax[i].grid(axis='y', color='gainsboro', linestyle='-', linewidth=0.5)
            ax[i].set_facecolor('none')
            ax[i].set_xlabel('Days',color = 'white')
            ax[i].set_ylabel(y_label,fontsize = 14,color = 'white')
            ax[i].set_title(cols[i],loc = 'left',color = 'white')

            old_value = self.first_nonnan(self.df[cols[i]])
            new_value = self.last_nonnan(self.df[cols[i]])

            perc_change = round(self.pct_change(old_value,new_value),2)
            doll_change = round(self.dol_change(old_value,new_value),2)

            the_title = "Percent Change: " + str(perc_change) + '% ' + ' Dollar Change: ' + '$' + str(doll_change)
            ax[i].set_title(the_title,loc = 'right',fontsize = 8, color = 'white')

            ax[i].spines['right'].set_color('white')
            ax[i].spines['bottom'].set_color('white')

            ax[i].tick_params(axis='x', colors='white')
            ax[i].tick_params(axis='y', colors='white')   

            
            #ax[i].legend()

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

    # Convert the image to a Base64-encoded string
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        return image_base64

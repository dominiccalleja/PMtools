
# Tools to build a set of tasks from a xlsx file 

from activity import Activity

from datetime import date, timedelta
import pandas as pd
import numpy as np 


class Builder():
    """
    
    """
    activity = {}
    def __init__(self, file_name):
        self.file_name = file_name

    def pass_file(self, **kwargs):
        # Iterate over the rows of the file 
        df = pd.read_excel(self.file_name, **kwargs)
        df = df.reset_index(drop=True)
        self._conv_ = df['id']
        for i in df.index:
            self.activity[i] = Activity(**df.loc[i].to_dict())   

    def gen_activities(self):
        # Generate an activity for each row
        # Process the dependancy 
        pass

    def id2num(self, id):
        return self._conv_.index[self._conv_['id'] == id]

    def num2id(self, i):
        return self._conv_.loc[i]

class Scheduler():
    """
    
    """
    def __init__(self):
        pass 

    def __weekend_check__(self):
        pass

    def __condition_checker__(self):
        pass 

    def isdependent(self):
        pass

    def isparallel(self):
        pass 

    def isdependent_onend(self):
        pass

    def isdependent_onstart(self):
        pass

    

if __name__ == '__main__':

    B = Builder('example/GCP-onboarding-ActivitiesPlan-v2.xlsx')
    B.pass_file(index_col=[0])
    
    B.activity[0].parent
    

    gant = pd.read_excel('example/GCP-onboarding-ActivitiesPlan-v2.xlsx', index_col=[0])
    gant.loc[np.isnan(gant['Duration L']),'Duration L'] = 1 
    gant = gant.reset_index(drop=True)

    gant.to_excel(
            'example/GCP-onboarding-ActivitiesPlan-v2.xlsx')




    
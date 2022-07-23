
# Tools to build a set of tasks from a xlsx file 

from activity import Activity
from methods import *


class Builder():
    """
    
    """
    activity = {}
    def __init__(self, file_name, start_date):
        self.file_name = file_name
        self.start_date = start_date
    def pass_file(self, **kwargs):
        # Iterate over the rows of the file 
        df = pd.read_excel(self.file_name, **kwargs)
        df = df.reset_index(drop=True)
        self._conv_ = df['id']
        self.df = df

    def process(self,  upper_bound = True):
        self.df, self.dep = compute_dependency_date(self.df, self.start_date, upper_bound = upper_bound)
         
        for i in self.df.index:
            self.activity[i] = Activity(**self.df.loc[i].to_dict())

    def id2num(self, id):
        return self._conv_.index[self._conv_['id'] == id]

    def num2id(self, i):
        return self._conv_.loc[i]

    def plot(self, save_address=None):
        plot_gant(self.df, self.dep, figsize=(60, 30),
                  save_address=save_address, labelsize='20')

    def __repr__(self):
        return '\n'.join([v.__repr__() for k, v in self.activity.items()])

# class Scheduler():
#     """
    
#     """
#     def __init__(self, cls, start_date):
#         self.start_date = start_date
#         self.__date = self.start_date
#         self.builder = cls
#         # schedule = 
#         # calendar = 

#     def process(self):


#     def __interator__(self, activity):
#         DR = date_range(self.__date, 2 * activity.duration)
#         c = 0
#         for d in DR:
#             if not is_workday(d):
#                 activity.duration = activity.duration + 1
#             else:
#                 c += 1
#             if c == activity.duration:
#                 activity.start_date = self.__date
#                 activity.comp_missing()

                


#     # def __weekend_check__(self):
#     #     pass

#     def __process__(self):
        
    
#     # def __condition_checker__(self):
#     #     pass 

#     # def isdependent(self):
#     #     pass

#     # def isparallel(self):
#     #     pass 

#     # def isdependent_onend(self):
#     #     pass

#     # def isdependent_onstart(self):
#     #     pass


if __name__ == '__main__':

    B = Builder(
        'example/GCP-onboarding-ActivitiesPlan-V3.xlsx', date(2022,7,18))
    B.pass_file(index_col =[0])
    B.process(upper_bound=False)

    B.plot(save_address='example/GANTCHART-GCP-onboarding-ActivitiesPlan-V3-pessimistic.png')
    B.activity[len(B.activity)-1]

    # B.df.to_excel('example/GCP-onboarding-ActivitiesPlan-V4.xlsx')

    # C = Scheduler(B, date.today())

    # C.builder
    
    # B.activity[0].parent
    

    # gant = pd.read_excel('example/GCP-onboarding-ActivitiesPlan-v2.xlsx', index_col=[0])
    # gant.loc[np.isnan(gant['Duration L']),'Duration L'] = 1 
    # gant = gant.reset_index(drop=True)

    # gant.to_excel(
    #         'example/GCP-onboarding-ActivitiesPlan-v2.xlsx')




    
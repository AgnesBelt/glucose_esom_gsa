import prim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import glob
import pickle

import sys

#%%
# # Example from PRIM GitHub
# import numpy as np

# df = pd.DataFrame(np.random.rand(1000, 3), columns=["x1", "x2", "x3"])
# response = df["x1"]*df["x2"] + 0.2*df["x3"]
    
# p = prim.Prim(df, response, threshold=0.5, threshold_type=">")
    
# box = p.find_box()
# box.show_tradeoff()

# plt.show()

#%%
args = sys.argv[1:]
if len(args)!=2:
    #print('define set of SD solution space'')
    print("Usage: PRIM_analysis.py <FolderName_withResults> <Version_ofinterest>")
    exit(1)

folder = args[0] #input('Folder name: ')
version = args[1]

#%% locate folder with data
folder = 'GLUCOSE_withCB_221104'
myPath = Path(f'{folder}', 'results', '0')
tifCounter = len(glob.glob1(myPath,"*.ilp"))
print('Infeasible scenarios:', tifCounter)

myPath = Path(f'{folder}','results', '0')
n_replications = int(len(glob.glob1(myPath,"*.sol")))
print("Number of replications/runs:", n_replications)
replications = list(range(0,n_replications))

# favorite_color = pickle.load( open( 'save.p', 'rb' ) )

# output = 'GLUCOSE_LandUse'
# fp = open(f'{output}'+'.p', 'wb')
# my_path = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
# with my_path.open('wb') as fp:
#     pickle.dump(LandResources, fp)

#%% read input data
output = 'GLUCOSE_DataInputs'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
inputs_GLUCOSE = pickle.load(fp)

## AccumulatedAnnualDemand - Food
output = 'GLUCOSE_FoodDemand_VFOO'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
Demand_VFOO = pickle.load(fp)

output = 'GLUCOSE_FoodDemand_MFOO'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
Demand_MFOO = pickle.load(fp)

#%% read output data (results)
## PrimaryEnergy
output = 'GLUCOSE_PrimaryEnergy'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
PrimaryEnergy = pickle.load(fp)

output = 'GLUCOSE_PrimaryEnergy_RE'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
PrimaryEnergy_RE = pickle.load(fp)

output = 'GLUCOSE_PrimaryEnergy_NU'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
PrimaryEnergy_NU = pickle.load(fp)

## ElectricalCapacity
output = 'GLUCOSE_ElectricalCapacity'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
CapacityElc = pickle.load(fp)

### ElectricalCapacity RE
output = 'GLUCOSE_ElectricalCapacity_RE'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
RE_ElcCap = pickle.load(fp)

### ElectricalCapacity NU
output = 'GLUCOSE_ElectricalCapacity_NU'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
NU_ElcCap = pickle.load(fp)

### ElectricalCapacity CCS
output = 'GLUCOSE_ElectricalCapacity_CCS'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
CCS_ElcCap = pickle.load(fp)
print(CCS_ElcCap)

## LandUse
output = 'GLUCOSE_LandUse'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
LandUse = pickle.load(fp)

output = 'GLUCOSE_LandUse_LF'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
LandUse_LF = pickle.load(fp)

## AnnualEmissions, total
output = 'GLUCOSE_Emissions'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
Emissions = pickle.load(fp)
Emissions_GHG = Emissions['CO2EQ']
Emissions_GHG = Emissions_GHG.iloc[:,:-10]
Emissions_Water = Emissions['WATER']
Emissions_Water = Emissions_Water.iloc[:,:-10]

### Emissions, total 2020-2050
Emissions_GHG['Total, 2020-2050'] = Emissions_GHG.loc[:,2020:2050].sum(axis=1)

## DirectAirCapture emissions
output = 'GLUCOSE_Emissions_DAC'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
DAC_Emission = pickle.load(fp)
DAC_Emission = DAC_Emission.iloc[:,:-10]

## technologies growth rate
### TotalCapacityAnnual - Electrical Capacity, RENEWABLE
output = 'GLUCOSE_ElectricalCapacity_RE_diff'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
RE_ElcCap_diff = pickle.load(fp)
RE_ElcCap_diff['mean_value']= RE_ElcCap_diff.mean(axis=1)

### TotalCapacityAnnual - Electrical Capacity, NUCLEAR
output = 'GLUCOSE_ElectricalCapacity_NU_diff'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
NU_ElcCap_diff = pickle.load(fp)
NU_ElcCap_diff['mean_value']= NU_ElcCap_diff.mean(axis=1)

### TotalCapacityAnnual - Electrical Capacity, CCS
output = 'GLUCOSE_ElectricalCapacity_CCS_diff'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
CCS_ElcCap_diff = pickle.load(fp)
CCS_ElcCap_diff['mean_value']= CCS_ElcCap_diff.mean(axis=1)

### AnnualTechnologyEmission - CO2EQ, Direct Air Capture technologies
output = 'GLUCOSE_Emissions_DAC_diff'
myPath = Path(f'{folder}', 'GLUCOSE_DataProcessing', f'{output}'+'.p') 
fp = open(myPath, 'rb')
DAC_Emission_diff = pickle.load(fp)
DAC_Emission_diff['mean_value']= DAC_Emission_diff.mean(axis=1)
print(DAC_Emission_diff)

#%% define interest solution space for PRIM analysis, v1
#version = 'v3'
if version == 'v1':
    ofinterest1 = (Emissions_GHG[2050]<5)
    ofinterest2 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1)
    ofinterest2_reverse = (Emissions_GHG[2050]>5) + (Emissions_DAC[2050]<=-1)
    ofinterest3 = (Emissions_GHG[2050]<5) + (PrimaryEnergy_RE[2050]>=250)
    ofinterest4 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=250) + (Demand_MFOO[2050]<=Demand_MFOO[2025])
    ofinterest5 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=250) + (Demand_MFOO[2050]<=Demand_MFOO[2025]) + (LandUse_LF[2050]>=(LandUse_LF[2010])) #+(water<=(2*WATER_GLUCOSE[2025]))
    ofinterest6 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (Demand_MFOO[2050]<=Demand_MFOO[2025]) + (LandUse_LF[2050]>=(LandUse_LF[2010])) 
    ofinterest7 = (Emissions_GHG[2050]<5) + (PrimaryEnergy_RE[2050]>=250) + (PrimaryEnergy_NU[2050]<=PrimaryEnergy_NU[2025])
if version == 'v2':
    ofinterest1 = (Emissions_GHG['Total, 2020-2050']<=400)
    ofinterest2 = (Emissions_GHG['Total, 2020-2050']<=400) + (Emissions_DAC[2050]>=-1)
    ofinterest3 = (Emissions_GHG['Total, 2020-2050']<=400) + (PrimaryEnergy_RE[2050]>=250)
    ofinterest4 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=250) + (Demand_MFOO[2050]<=Demand_MFOO[2025])
    ofinterest5 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=250) + (Demand_MFOO[2050]<=Demand_MFOO[2025]) + (LandUse_LF[2050]>=(LandUse_LF[2010])) #+(water<=(2*WATER_GLUCOSE[2025]))
    ofinterest6 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (Demand_MFOO[2050]<=Demand_MFOO[2025]) + (LandUse_LF[2050]>=(LandUse_LF[2010])) 
    ofinterest7 = (Emissions_GHG['Total, 2020-2050']<=400) + (PrimaryEnergy_RE[2050]>=250) + (PrimaryEnergy_NU[2050]<=PrimaryEnergy_NU[2025])
if version == 'v3':
    # ofinterest1 = (RE_ElcCap_diff['mean_value']<=(1+0.05)*(RE_ElcCap_diff['mean_value'].min()))
    # ofinterest2 = (NU_ElcCap_diff['mean_value']<=(1+0.05)*(NU_ElcCap_diff['mean_value'].min()))
    # ofinterest3 = (CCS_ElcCap_diff['mean_value']<=(1+0.05)*(CCS_ElcCap_diff['mean_value'].min()))
    # ofinterest4 = (DAC_Emission_diff['mean_value']>=(1+0.05)*(DAC_Emission_diff['mean_value'].max()))
    # ofinterest5 = (RE_ElcCap_diff['mean_value']<=(1+0.1)*(RE_ElcCap_diff['mean_value'].min()))+(NU_ElcCap_diff['mean_value']<=(1+0.05)*(NU_ElcCap_diff['mean_value'].min()))
    # ofinterest6 = (RE_ElcCap_diff['mean_value']<=(1+0.05)*(RE_ElcCap_diff['mean_value'].min()))+(CCS_ElcCap_diff['mean_value']<=(1+0.05)*(CCS_ElcCap_diff['mean_value'].min()))
    # ofinterest7 = (NU_ElcCap_diff['mean_value']<=(1+0.05)*(NU_ElcCap_diff['mean_value'].min()))+(CCS_ElcCap_diff['mean_value']<=(1+0.05)*(CCS_ElcCap_diff['mean_value'].min()))
    # ofinterest8 = NU_ElcCap[2050]<=((1+0.05)*NU_ElcCap[2050].min())
    # ofinterest9 = NU_ElcCap[2050]<=((1+0.05)*NU_ElcCap[2050].min())+(RE_ElcCap_diff['mean_value']<=(1+0.05)*(RE_ElcCap_diff['mean_value'].min()))
    # ofinterest9 = NU_ElcCap[2050]<=((1+0.05)*NU_ElcCap[2050].min())+(DAC_Emission[2050]<=((1+0.05)*DAC_Emission[2050].min()))
    ofinterest1 = (RE_ElcCap_diff['mean_value']<=(1+0.05)*(RE_ElcCap_diff['mean_value'].min()))+(DAC_Emission[2050]>=((1+0.05)*DAC_Emission[2050].max())) #+(CCS_ElcCap[2050]<=(1+0.05)*(CCS_ElcCap[2050].min()))
    ofinterest1_runs = pd.Series(ofinterest1[ofinterest1].index.values, )
    ofinterest1_runs = ofinterest1_runs.astype(int)
    myPath = Path(f'{folder}', 'ofinterest1_runs.csv')
    ofinterest1_runs.to_csv(myPath, header='runs', index=False)
    
    ofinterest2 = (CCS_ElcCap[2050]<=(1+0.2)*(CCS_ElcCap[2050].min()))
    ofinterest3 = (RE_ElcCap_diff['mean_value']<=(1+0.05)*(RE_ElcCap_diff['mean_value'].min()))+(CCS_ElcCap[2050]<=(1+0.2)*(CCS_ElcCap[2050].min()))
    ofinterest4 = (DAC_Emission[2050]<=((1+0.05)*DAC_Emission[2050].min()))+(CCS_ElcCap[2050]<=(1+0.05)*(CCS_ElcCap[2050].min()))

    
    

#%% apply PRIM package to generate interactive graphs
# ofinterest1 = (Emissions_GHG[2050]<5)
p1 = prim.Prim(inputs_GLUCOSE, ofinterest1, threshold=0.8, threshold_type=">")  
print(p1)
box = p1.find_box()
print(box)
box.show_tradeoff()

plt.title('ofinterest1')
plt.show()
#myPath = Path(f'{folder}', 'img', f'{version}'+'_ofinterest1.png')
#plt.savefig(myPath)

#%% apply PRIM package to generate interactive graphs
# ofinterest2 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1)
p2 = prim.Prim(inputs_GLUCOSE, ofinterest2, threshold=0.8, threshold_type=">")  
box = p2.find_box()
box.show_tradeoff()

plt.title('ofinterest2')
plt.show()

#%% apply PRIM package to generate interactive graphs
# ofinterest2_reverse = (Emissions_GHG[2050]>5) + (Emissions_DAC[2050]<=-1)
# p2_rev = prim.Prim(inputs_GLUCOSE, ofinterest2_reverse, threshold=0.8, threshold_type=">")  
# box = p2_rev.find_box()
# box.show_tradeoff()

# plt.title('High Emissions_GHG + DAC')
# plt.show()
#%% apply PRIM package to generate interactive graphs
# ofinterest3 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=150)
p3 = prim.Prim(inputs_GLUCOSE, ofinterest3, threshold=0.8, threshold_type=">")  
box = p3.find_box()
box.show_tradeoff()

plt.title('ofinterest3')
plt.show()

#%%
p4 = prim.Prim(inputs_GLUCOSE, ofinterest4, threshold=0.8, threshold_type=">")  
box = p4.find_box()
box.show_tradeoff()

plt.title('ofinterest4')
plt.show()

#%%
p5 = prim.Prim(inputs_GLUCOSE, ofinterest5, threshold=0.8, threshold_type=">")  
box = p5.find_box()
box.show_tradeoff()

plt.title('ofinterest5')
plt.show()

#%%
p6 = prim.Prim(inputs_GLUCOSE, ofinterest6, threshold=0.8, threshold_type=">")  
box = p5.find_box()
box.show_tradeoff()

plt.title('ofinterest6')
plt.show()

#%% apply PRIM package to generate interactive graphs
# ofinterest7 = (Emissions_GHG[2050]<5) + (Emissions_DAC[2050]>=-1) + (PrimaryEnergy_RE[2050]>=250) + (PrimaryEnergy_NU[2050]<=PrimaryEnergy_NU[2025])
p7 = prim.Prim(inputs_GLUCOSE, ofinterest7, threshold=0.8, threshold_type=">")  
box = p7.find_box()
box.show_tradeoff()

plt.title('ofinterest7')
plt.show()

#%%
p8 = prim.Prim(inputs_GLUCOSE, ofinterest8, threshold=0.8, threshold_type=">")  
box = p8.find_box()
box.show_tradeoff()

plt.title('ofinterest8')
plt.show()
#%%
p9 = prim.Prim(inputs_GLUCOSE, ofinterest9, threshold=0.8, threshold_type=">")  
box = p9.find_box()
box.show_tradeoff()

plt.title('ofinterest9')
plt.show()
# %%

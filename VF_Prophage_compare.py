from Bio import SeqIO
from Bio import GenBank as GB
import pandas as pd
import argparse
import os
import glob

VF = "C:\\Users\\DeepThought\\Documents\\SchmitzLab\\VF_UPEC.csv"
Prophagefile = "C:\\Users\\DeepThought\\Documents\\SchmitzLab\\VF_prophage\\Prophage_regions.csv"
MGEdirectory="C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\filestotest\\"
MGEfile="C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGEALL.csv"
Abx='C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Resfinder\\VUTIs\\allAMR_withcontigs2.tsv'

def MGEtodf(directory):
    for file in glob.glob(directory + "*.csv"):  # for resfinder data
        name = os.path.splitext(os.path.basename(file))[0]

        df = pd.read_csv(file, sep=",", usecols=['name', 'contig', 'start', 'end'], skiprows=5)
        df['contig'] = df['contig'].str.replace(r'Contig_', '')  # get only the contig number, remove the word Contig
        df['contig'] = df['contig'].str.replace(r'contig_', '')
        df['sample']=name
        print(df)
        file = open('C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGEALL.csv', "a")
        df.to_csv(file, mode='a', index=False, header=False)

def VFMGE(VF, MGElist):

    VFDict = {}


    MGEdf = pd.read_csv(MGElist, sep=",", usecols=['Sample', 'MGE','Contig', 'Start', 'Stop'])

    VFdf=pd.read_csv(VF, sep=",", usecols=['Sample', 'VF','Contig', 'Start', 'Stop'])


    samples=VFdf['Sample'].tolist()
    samples=list(set(samples))
    for i in range(len(samples)):
        df=VFdf[VFdf['Sample']== samples[i]]
        VFDict[samples[i]] = df


    for i in range(len(MGEdf)):
        #get df of VF for the sample
        value=VFDict[(MGEdf.iloc[i,0])]
        # sampprophage=prophagedf[prophagedf['Sample']==VFDict[prophagedf.iloc[i,0]]]

        for j in range(len(value)):
             x = range(MGEdf.iloc[i, 3], MGEdf.iloc[i, 4])
             xs = set(x)
             y = range(int(value.iloc[j, 3]), int(value.iloc[j, 4]))
             ys=set(y)
             if MGEdf.iloc[i,2] == int(value.iloc[j, 2]):
                 if (xs & ys):
                    file = open('C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGE_VFout.txt', "a")
                    file.write( str(MGEdf.iloc[i,0]) + "\t" + str(value.iloc[j,1]) + '\t'+str(MGEdf.iloc[i,1]) +'\t'+ str(value.iloc[j,2])+ '\t'+ str(MGEdf.iloc[i,3])+ '\t'+ str(MGEdf.iloc[i,4])+ '\t' + str(value.iloc[j,3])+'\t' + str(value.iloc[j,4])+"\n")
                    file.close()
             else:
                 file = open('C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGE_VFout.txt', "a")
                 file.write(str(MGEdf.iloc[i,0]) + "\t"+ str(value.iloc[j,1]) +"\t"+ "No VF overlap" + "\n")
                 print(str(MGEdf.iloc[i,0]) + str(value.iloc[j,1]) + "No VF overlap")
def AbxMGE(Abxfile, MGElist):
    print("no")
    AbxDict={}
    MGEdf = pd.read_csv(MGElist, sep=",", usecols=['Sample', 'MGE','Contig', 'Start', 'Stop'])
    Abxdf=  pd.read_csv(Abxfile, sep="\t", usecols=['AMR', 'Contig', 'Start', 'Stop', 'Function', 'Sample'])
    samples = MGEdf['Sample'].tolist()
    samples = list(set(samples))
    for i in range(len(samples)):
        df = Abxdf[Abxdf['Sample'] == samples[i]]
        AbxDict[samples[i]] = df

    for i in range(len(MGEdf)):
        #get df of VF for the sample
        value=AbxDict[(MGEdf.iloc[i,0])]
        # sampprophage=prophagedf[prophagedf['Sample']==VFDict[prophagedf.iloc[i,0]]]

        for j in range(len(value)):
             x = range(MGEdf.iloc[i, 3], MGEdf.iloc[i, 4])
             xs = set(x)
             y = range(int(value.iloc[j, 2]), int(value.iloc[j, 3]))
             ys=set(y)
             if MGEdf.iloc[i,2] == int(value.iloc[j, 1]):
                 if (xs & ys):
                    file = open('C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGE_Abxout.txt', "a")
                    file.write( str(MGEdf.iloc[i,0]) + "\t" + str(value.iloc[j,0]) +str(MGEdf.iloc[i,1]) + '\t'+ str(MGEdf.iloc[i,2]) + '\t'+ str(MGEdf.iloc[i,3])+ '\t'+ str(MGEdf.iloc[i,4])+ '\t' + str(value.iloc[j,2])+'\t' + str(value.iloc[j,3])+ '\t'+str(value.iloc[j,4])+ "\n")
                    file.close()
             else:
                 file = open('C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\MGE_Abxout.txt', "a")
                 file.write(str(MGEdf.iloc[i,0]) + "\t"+ str(value.iloc[j,0]) +"\t"+ "No abx overlap" + "\n")
                 print(str(MGEdf.iloc[i,0]) + str(value.iloc[j,0]) + "No abx overlap")

if __name__ == '__main__':
    AbxMGE(Abx, MGEfile)
    # VFMGE(VF, MGEfile)
    # MGEtodf(MGEdirectory)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

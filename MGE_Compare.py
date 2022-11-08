
import pandas as pd
import os
import glob
import sys
alldatatsv = "C:\\Users\\DeepThought\\Documents\\SchmitzLab\\MEFinder\\allAMR_withcontigs.tsv"
mge= "C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\filestotest\\"
outputMGE= "C:\\Users\\DeepThought\\Documents\\SchmitzLab\\Pythoncode\\AMR_MGE_overlap.txt"

def makedata (dir):

    VFdict={}

    for filepath in glob.iglob(dir + 'allAMR.tsv'):

        name=os.path.splitext(os.path.basename(filepath))[0]


        df=pd.read_csv(filepath,sep='\t', usecols=['Gene','Contig','Position in contig'])

        df['Contig']= df['Contig'].str.replace(r'Contig_','') #get only the contig number, remove the word Contig
        df['Contig'] = df['Contig'].str.replace(r'contig_', '') #get only the contig number, remove the word Contig
        startlist = []
        endlist = []
        for i in range(len(df)):
            start = df.iloc[i, [2]].str.split(".")
            startreal = int(start[0][0])
            end = int(start[0][2])
            startlist.append(startreal)
            endlist.append(end)

        startseries = pd.Series(startlist)
        endseries = pd.Series(endlist)
        df['Start'] = startseries
        df['Stop'] = endseries

        VFdict[name] = df  # create a dictionary where the lookup value is the sample and the key is a dataframe containing antibiotic resistance gene information.

    return VFdict
# def makemge (mgedir):
#     for file in glob.iglob(mgedir + '*.csv'):
#         df=pd.read_csv(file, sep=',', usecols=['name', 'type', 'contig', 'start', 'end', 'end'])
#
#     return df

def comparemge (mgedir, VFdict, output):
    for file in glob.iglob(mgedir + '*.csv'):

        mgefiledf=pd.read_csv(file, skiprows=5, sep=',', usecols=['name', 'type', 'contig', 'start', 'end'])
        mgefiledf['contig'] = mgefiledf['contig'].str.replace(r'Contig_', '')  # get only the contig number, remove the word Contig
        mgefiledf['contig'] = mgefiledf['contig'].str.replace(r'contig_', '')  # get only the contig number, remove the word Contig
        for i in range(3): #use number of samples -1
            namenoextension=os.path.splitext(os.path.basename(file))[0]
            onlyname=namenoextension.strip(".fasta")
            onlynumber=onlyname.strip("VUTI")


            value = VFdict[onlynumber]
            for j in range(len(value)):
                smallx= mgefiledf.iloc[i, 3] - 31000
                bigx=mgefiledf.iloc[i,4] +31000
                x = range(smallx, bigx)
                xs = set(x)

                y = range(value.iloc[j, 3], value.iloc[j, 4])


                if mgefiledf.iloc[i, 2] == value.iloc[j, 1]:
                    print (namenoextension + str(mgefiledf.iloc[i,0])  +str(mgefiledf.iloc[i,2] + '' + value.iloc[j, 0]))
                    if xs.intersection(y):
                        print(xs.intersection(y))
                        f = open(output, "a")  # arg parse 3rd value, path to text file to output to.
                        f.write(onlyname + '\t' + str(mgefiledf.iloc[i, 0]) + '\t'+str(mgefiledf.iloc[i, 1]) +'\t' + str(value.iloc[j, 0]) + "\t" + str(mgefiledf.iloc[i, 2]) +"\n")


                        f.close()


if __name__== '__main__':
    OutVFdict= makedata(alldatatsv)

    comparemge(mge, OutVFdict, outputMGE)


import pandas as pd
import os
import glob
import sys

def makedata (dirtsv):

    VFdict={}

    for filepath in glob.iglob(dirtsv + '*.txt'):
        name=os.path.splitext(os.path.basename(filepath))[0]
        print(name)
        df=pd.read_csv(filepath,sep='\t', usecols=['Resistance gene','Contig','Position in contig', 'Phenotype'])

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
def makeprophage (prophagefile):
    df=pd.read_csv(prophagefile, sep=',', usecols=['Sample', 'Closest phage', 'Complete?', 'Contig', 'Start', 'End'])

    return df

def compareprophage (prophagefiledf, VFdict, output):

    for i in range(len(prophagefiledf)):
        value = VFdict[str(prophagefiledf.iloc[i, 0])]
        for j in range(len(value)):
            x = range(prophagefiledf.iloc[i, 4], prophagefiledf.iloc[i, 5])
            xs = set(x)
            y = range(value.iloc[j, 4], value.iloc[j, 5])
            ys = set(y)
            if prophagefiledf.iloc[i, 3] == value.iloc[j, 4]:
                print (str(prophagefiledf.iloc[i,0]))
                if xs and ys:

                    f = open(output, "a")  # arg parse 3rd value, path to text file to output to.
                    f.write(str(prophagefiledf.iloc[i, 0]) + '\t'+str(prophagefiledf.iloc[i, 1]) + '\t'+ str(prophagefiledf.iloc[i, 2]) + ":" + str(value.iloc[j, 0]) + ";" + str(value.iloc[j, 3]) + "\n")


                    f.close()


if __name__== '__main__':
    OutVFdict= makedata(sys.argv[1])
    OutProphagedf=makeprophage(sys.argv[2])
    compareprophage(OutProphagedf, OutVFdict, sys.argv[3])

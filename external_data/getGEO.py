import GEOparse
import pandas as pd
# in vitro: GSE151189
# ex vivo: GSE59098

# in vitro
gse = GEOparse.get_GEO(geo="GSE151189", destdir="./") # PMID: 33483501

# platform gse.gpls
assert len(gse.gpls) == 1, "Platform more than 1!"

# platform name and platform table
gpl_name, gpl = list(gse.gpls.items())[0]

print("Platform name:", gpl_name)
print("Platform table:", gpl.table)

# platform in pandas dataframe format
plt = gpl.table

# samples gse.gsms

all_title = []
all_exp = []
all_label = []  # resistance, 1 for  resistant, 0 for non-resistant
for gsm_name, gsm in gse.gsms.items():
    '''
    # GSE151189
    '''
    t = gsm.metadata['title'][0] # Dd2_[WT|R539T|C580Y|]_[0|3|6|16|24|48]h_rep[1|2|3] , Cam3II_[revWT|R539T|]_[0|8|16|24|32|40|48]h_rep[1|2|3]
    print(t)
    '''
    strain:
        Dd2: lab strain
        Cam3II: isolate from patients
    mutation:
        R539T: resistant ++
        C580Y: resistant +
        WT: resistant -
        *for resistance we denote both mutant as 1 and WT as 0
    0-48h:
        hours after DHA treatment
    rep1-3:
        biological replicates
    '''
    exp =gsm.table.rename(columns = {'ID_REF':'ID'})
    # map probe to gene by left join
    new_exp = exp.merge(plt, on='ID', how =  'left')[['ID', 'ORF', 'VALUE']].groupby('ORF').mean()[['VALUE']].T
    if t.split('_')[1] in ['R539T', 'C580Y']:
        all_label.append(1)
    else:
        all_label.append(0)
    all_title.append(t)
    all_exp.append(new_exp)

df_exp= pd.concat(all_exp).reset_index(drop = True)
df_exp.insert(loc=0, column='sample', value=all_title)
df_exp['label'] = all_label
df_exp.to_csv('in_vitro_GSE151189.csv', index=False)


# ex vivo
# from the same isolates in Mok et al's paper in in vivo training set
# The samples with <=5 hours of clearance half life are labeled as  “Fast” in terms of clearance rate, and considered as non-ART-resistant samples
ref = pd.read_csv('./mok_supplementary/Table3.Clearance_rate.csv')

gse = GEOparse.get_GEO(geo="GSE59098", destdir="./") # PMID: 21810278

# platform gse.gpls
assert len(gse.gpls) == 1, "Platform more than 1!"

# platform name and platform table
gpl_name, gpl = list(gse.gpls.items())[0]

print("Platform name:", gpl_name)
print("Platform table:", gpl.table)

# platform in pandas dataframe format
plt = gpl.table

# samples gse.gsms

all_title = []
all_exp = []
all_label = []  # resistance, 1 for  resistant, 0 for non-resistant

for gsm_name, gsm in gse.gsms.items():
    t = gsm.metadata['title'][0] # KH004-068-0h-312918
    print(t)
    '''
    all ex vivo datasets; 19 isolates collected from Pailin, Cambodia
    [0-48]h: the time duration of growing ex vivo
    '''
    pid ='-'.join(t.split('-')[:2])
    try:
        clr = ref.loc[ref['Patient Code']==pid, 'parasite clearance halflife (h)'].to_list()[0]
        print(clr)
        if clr >=5:
            all_label.append(1)
        else:
            all_label.append(0)
        exp =gsm.table.rename(columns = {'ID_REF':'ID'})
        # map probe to gene by left join
        new_exp = exp.merge(plt, on='ID', how =  'left')[['ID', 'ORF', 'VALUE']].groupby('ORF').mean()[['VALUE']].T
        all_title.append(t)
        all_exp.append(new_exp)
    except:
        print(pid)

df_exp= pd.concat(all_exp).reset_index(drop = True)
df_exp.insert(loc=0, column='sample', value=all_title)
df_exp['label'] = all_label
df_exp.to_csv('ex_vivo_GSE59098.csv', index=False)

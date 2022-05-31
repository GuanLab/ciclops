# Tutorial for using Ciclops

This document will go through the steps to run Ciclops on your local machine, using small gene expression datasets obtained from GEO as mock data. All commands below should be run in your terminal. Note that this program was created and tested on a Linux machine.

## Create environment

In your terminal, create a new conda environment:

```
conda create --name ciclops_env python=3.8
```

And activate the environment:

```
conda activate ciclops_env
```

## Installation

Install this package via pip:

```
pip install ciclops
```

Ensure all the dependencies have been correctly installed.

## Download datasets

In order to download the mock data, install GEOparse:

```
pip install GEOparse
```

Then, assuming you are working from this tutorial directory, download the data using the script provided:

```
python3 ../external_data/getGEO.py
```

The following csv files should now be in your directory:

```
tutorial/
|___ in_vitro_GSE151189.csv
|___ ex_vivo_GSE59098.csv
```

We will be using the in vitro data as the training set and the ex vivo data as the test/validation set. The files will look something like this (taking a look at ```in_vitro_GSE151189.csv```):

```
sample          PF3D7_0100100       PF3D7_0100200 ... label
Dd2_WT_0h_rep1  0.15349706433333332 -0.402726618  ...   0
Dd2_WT_3h_rep1  0.40127333975       -0.468004195  ...   0
...
```

## Train model

Run Ciclops using the following command:

```
ciclops --train_path ./in_vitro_GSE151189.csv --valid_path ./ex_vivo_GSE59098.csv --shap
```

The other arguments are optional and don't need to be passed, unless you want to change from the default settings. The above command will perform imputation, quantile normalization, train the LightGBM model using 10-fold cross-validation, and evaluate the model performance on the test data. Additionally, because the ```--shap``` flag was used, Ciclops will perform SHAP analysis.

## Evaluate results

Your directory should now contain the following subdirectories:

```
tutorial/
|___ in_vitro_GSE151189.csv
|___ ex_vivo_GSE59098.csv
|___ training/
      |___ fold_*/
            |___ Test.csv
            |___ Train.csv
|___ validation/
      |___ results.csv
      |___ Test.csv
|___ params/
      |___ fold_*_model.sav
|___ performance/
      |___ *confidence.csv
      |___ *results.csv
|___ SHAP/
      |___ training/
      |___ validation/
      |___ intersection_list_top_n_genes.txt
      |___ intersection_venn_top_n_genes.pdf
```

## References

* External data for testing/example purposes:
  * Shaw, P.J. et al. (2015) ‘Plasmodium parasites mount an arrest response to dihydroartemisinin, as revealed by whole transcriptome shotgun sequencing (RNA-seq) and microarray study’, BMC Genomics. doi:10.1186/s12864-015-2040-0.
  * GSE59098
  * GSE151189

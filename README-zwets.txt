Zwets installation notes (on Turing src/hpc/gtdb/gtdbtk)

Documentation is here: https://ecogenomics.github.io/GTDBTk/installing/index.html

First installation (1.0.7) likely was conda plus pip.

Installation of 2.1.0 straight from Conda should be 

    conda create -n gtdbtk-2.1.0 -c conda-forge -c bioconda gtdbtk=2.1.0

But didn't work (release not there yet), so installed from source,
and same for upgrade to 2.1.1 (2022-07-15), and 2.2.0 and later:

    VER=2.2.3
    mamba create --quiet -n gtdbtk-$VER -c conda-forge -c bioconda python \
        dendropy numpy tqdm prodigal hmmer pplacer fastani fasttree mash \
        pydantic

Before running setup.py, comment out the requirement (we did that already):

    sed -i -Ee 's/^( *)install_requires=/\1#install_requires=/' setup.py

Now install

    conda activate gtdbtk-$VER
    python setup.py install

Set GTDBTK_DATA_PATH

    conda activate gtdbtk-$VER
    conda env config vars set GTDBTK_DATA_PATH=/data/genomics/gtdbtk/release207_v2

Add to HPC user-scripts

    See the repo https://git.kcri.it/hpc/user-scripts

Check

    gtdbtk check_install



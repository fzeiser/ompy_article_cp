# Supplementary material for OMpy article
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fzeiser/ompy_article_data/master)

# OMpy

`ompy` is the Oslo method implementation in python. It contains all the functionality needed to go from a raw coincidence matrix, via unfolding and the first-generation method, to fitting a level density and gamma-ray strength function. It also supports uncertainty propagation by Monte Carlo. The repository for `ompy` can be found [here](https://github.com/oslocyclotronlab/ompy) and is included as a [submodule](https://www.atlassian.com/git/tutorials/git-submodule) in this repository.

**Here we provide the notebooks used for the analysis in the article introducing OMpy.** A list of the files follows below.

Link to article: [add when published]

If you want to try the package before installation, you may simply [click here](https://mybinder.org/v2/gh/oslocyclotronlab/ompy/master?filepath=ompy%2Fnotebooks%2Fgetting_started.ipynb) to launch it on Binder. Note the cpu limitations probably will restrict to what extend you can rerun the analysis online. However, the attached `Dockerfile` can be used to easily set up the analysis on any machine.

**Original Runtime**:  approx 5 min on 51 vCPUs (type `N1` from the google cloud)

### Files:

- `analysis.ipynb`: Notebook used for the analysis
- `Dockerfile`: File that can be used by `Docker` to automatically build an images ("installation") with this notebook and ompy. Used eg. by MyBinder to run this notebook online. If you use this yourself, make sure to include also the `hooks`
- `figs`: Save folder for figures used in the article.
- `hooks`: Needed to this from `Dockerfile` due to the submodule ompy for MyBinder
- `misc_data`: External data for comparison (see Nyhus, H. T. *et al.* (2010). DOI: [10.1103/physrevc.81.024325](https://doi.org/10.1103/PhysRevC.81.024325)
and is reanalyzed in Renstrøm, T. *et al.* (2018). DOI: [10.1103/physrevc.98.054310](https://doi.org/10.1103/PhysRevC.98.054310))
- `myplots.py`: small convenience script for plotting the ensemble
- `ompy`: OMpy as a submodule. Including it as a [submodule](https://www.atlassian.com/git/tutorials/git-submodule) ensures that we use a specific version, even if you might have another version installed on your machine, too.
- `RAINIER_164Dy`: Files to generate the synthetic data with `RAINIER`
- `saved_run`: Persistency folder. With the `regernerate` flag in the notebook we can adjust whether or not we read the saved files from disk. E.g., we might just want to change some plots, not rerun all calculations.

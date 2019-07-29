import numpy as np
import numpy.ma as ma
import pandas as pd
from sklearn.decomposition import pca
from sklearn import linear_model
from sklearn.preprocessing import Imputer
import warnings
from operators import ens_mean, frac_grid_area


def ens_to_eof(ens_arr, explained_variance=0.95):
    """Perform EOF/PCA dimensionality reduction
    on ensemble array
    --------------------------------
    Args:
        ens_arr (numpy.ndarray): reshaped 2-d array
            into number of cells x ensemble size
        explained_variance (float): fraction of total
            variance that the reductions account for
    Returns:
        eofs (sklearn.decomposition.pca.PCA): fitted
            principal compoenent sklearn object
    """


    skpca = pca.PCA(explained_variance)
    eofs = skpca.fit(ens_arr)

    return eofs

def regress_eof(eofs, obs):
    """Perform a linear regression between
    EOFs and observations
    --------------------------------
    Args:
        eofs (numpy.ndarray): EOF transformed
            ens_arr containing same grid cells
            sample as observations
        obs (numpy.ndarray): Gridded observations
            either from pseudo or real observations
    Returns:
        model (scikit-learn model obj): fitted
            model object to eofs and obs
    """


    lm = linear_model.LinearRegression()
    model = lm.fit(eofs, obs)
    print("Regressed model score:", model.score(eofs, obs))
    return model


def predict_dv(model, eofs_of_model):
    """Reconstruct design value field from
    full EOF sample
    --------------------------------
    Args:
        model (scikit-learn model): model of regressed obs
            and models
        eofs_of_model (numpy.ndarray): EOF transformed
            ens_arr
    Returns:
        (numpy.ndarray): predicted design
            value field
    """


    return model.predict(eofs_of_model)
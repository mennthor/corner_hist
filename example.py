# coding: utf8

"""
Example usage of corner_hist, with a 4D data sample.
"""

import numpy as np
import matplotlib.pyplot as plt
import corner_hist


# Generate a sample of 4D data:
#   a1, a2 is a correlated gaussian
#   a3 is a poisson distribution with mean from |a1|
#   a4 is uniform in [0, 1]
ndata = 1000
mean = [5., 10.]
cov = [[1., 0.7], [0.7, 1.]]
a1, a2 = np.random.multivariate_normal(mean=mean, cov=cov, size=ndata).T
a3 = np.random.poisson(lam=np.abs(a1))
a4 = np.random.uniform(low=0.0, high=1., size=ndata)

# Create the 4D histogram.
sample = np.vstack((a1, a2, a3, a4)).T
h, bins = np.histogramdd(sample, bins=[20, 20, 30, 5])

# Make the corner plot.
# In reality the histogram is assumed to be the only thing available.
# If we had the sample we could just use the way better corner module.
label = ["a1", "a2", "a3", "a4"]
hist_args = {"color": "r"}
hist2D_args = {"cmap": "jet"}

fig, ax = corner_hist.corner_hist(h, bins=bins, label=label,
                                  hist_args=hist_args,
                                  hist2D_args=hist2D_args)

plt.savefig("corner_hist_demo.png", dpi=200)

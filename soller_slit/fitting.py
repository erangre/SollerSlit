import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('test.dat')

x = data[0, :]
y = data[1, :]

from lmfit import CompositeModel, Model
from lmfit.lineshapes import gaussian, linear


def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp / (np.sqrt(2 * np.pi) * wid)) * np.exp(-(x - cen) ** 2 / (2 * wid ** 2))


def line(x, slope, intercept):
    "line"
    return slope * x + intercept


def fit_gaussian(x, y):
    model = Model(gaussian) + Model(line)
    pars = model.make_params(amp=3500, cen=x[np.argmax(y)], wid=0.03, slope=0, intercept=0)

    result = model.fit(y, pars, x=x)
    print(result.fit_report())

    return result.best_fit, result.params['cen'].value, result.params['wid'].value, result.params['amp'].value

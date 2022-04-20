from scipy.stats import kurtosis, entropy
import numpy as np
import pywt
data = np.array([[1, 2, 3], [4, 5, 6], [4, 5, 6]])
coeffs = pywt.dwt2(data, 'haar')
cA, (cH, cV, cD) = coeffs

var = np.var(cA)

rows, cols = cA.shape
top, bottom = np.array_split(cA, 2)
diff = np.absolute(top-bottom)
asym = np.sum(diff)

kurt = np.sum(kurtosis(cA))

ent = sum(entropy(cA))
print(ent)

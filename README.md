# A Machine Learning Pipeline for Gravitational Waves

On this work, we present how machine learning can be used to classify voilent
events recorded in the gravitational inferemoters.

We will regard the gravitaional "events" provided by GW Open Science Collaboration
(GWOSC) as our positive labels which we will compare against baseline strains that
are recorded at other times of the O3a run.

On [1], we download 91 of these events from H1(LIGO Hanford) and L1(LIGO Livingston)
interferometers at 4096 Hz and trim them to [-16s, 16s] around their timestamp. On
[2], we will collect strains of same duration at random times of the O3a run. Then,
finally on [3], we will build a machine learning pipeline involving signal processing,
feature extraction, *nxk* cross-validation, sliding windows, and different classifier
algorithms. Finally, we will evaluate the performance of each of these algorithms.


Author: Damodar Dahal <damodar.dahal@selu.edu>

LIGO Strain Data provided by GWOSC (https://gw-openscience.org)
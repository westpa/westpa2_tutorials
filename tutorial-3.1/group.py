import westpa
import logging
from sklearn import cluster
import numpy

log = logging.getLogger(__name__)
log.debug('loading module %r' % __name__)

def kmeans(coords, n_clusters, splitting, **kwargs):
    X = numpy.array(coords)
    if X.shape[0] == 1:
        X = X.reshape(-1,1)
    km = cluster.KMeans(n_clusters=n_clusters).fit(X)   
    cluster_centers_indices = km.cluster_centers_
    labels = km.labels_
    if splitting:
        print("cluster centers:", numpy.sort(cluster_centers_indices))
    return labels

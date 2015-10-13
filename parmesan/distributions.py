import math
import theano.tensor as T


c = - 0.5 * math.log(2*math.pi)
def log_normal(x, mean, sd):
    """
    Compute log pdf of a Gaussian distribution with digonal covariance, at values x.

        .. math:: \log p(x) = \log \mathcal{N}(x; \mu, I\sigma^2)
    
    Parameters
    ----------
    x : Theano tensor
        Values at which to evaluate pdf.
    mean : Theano tensor
        Mean of the Gaussian distribution.
    sd : Theano tensor
        Standard deviation of the diagonal covariance Gaussian.

    Returns
    -------
    Theano tensor
        Element-wise log probability, this has to be summed for multi-variate distributions.
    """
    return c - T.log(T.abs_(sd)) - (x - mean)**2 / (2 * sd**2)

def log_normal2(x, mean, logvar):
    """
    Compute log pdf of a Gaussian distribution with digonal covariance, at values x.
    Here variance is parameterized in the log domain, which ensures :math:`\sigma > 0`.

        .. math:: \log p(x) = \log \mathcal{N}(x; \mu, I\sigma^2)
    
    Parameters
    ----------
    x : Theano tensor
        Values at which to evaluate pdf.
    mean : Theano tensor
        Mean of the Gaussian distribution.
    logvar : Theano tensor
        Log variance of the diagonal covariance Gaussian.

    Returns
    -------
    Theano tensor
        Element-wise log probability, this has to be summed for multi-variate distributions.
    """
    return c - logvar/2 - (x - mean)**2 / (2 * T.exp(logvar))

def log_stdnormal(x):
    """
    Compute log pdf of a standard Gaussian distribution with zero mean and unit variance, at values x.

        .. math:: \log p(x) = \log \mathcal{N}(x; 0, I)
    
    Parameters
    ----------
    x : Theano tensor
        Values at which to evaluate pdf.

    Returns
    -------
    Theano tensor
        Element-wise log probability, this has to be summed for multi-variate distributions.
    """
    return c - x**2 / 2

def log_bernoulli(x, p):
    """
    Compute log pdf of a Bernoulli distribution with success probability p, at values x.

        .. math:: \log p(x; p) = \log \mathcal{B}(x; p)

    Parameters
    ----------
    x : Theano tensor
        Values at which to evaluate pdf.
    p : Theano tensor
        Success probability :math:`p(x=1)`, which is also the mean of the Bernoulli distribution.

    Returns
    -------
    Theano tensor
        Element-wise log probability, this has to be summed for multi-variate distributions.
    """
    return -T.nnet.binary_crossentropy(p, x)

def kl_normal2_stdnormal(mean, logvar):
    """
    Compute analytically integrated KL-divergence between a diagonal covariance Gaussian and 
    a standard Gaussian.

    In the setting of the variational auto-encoder, when a Gaussian prior and diagonal Gaussian 
    approximate posterior is used, this analytically integrated KL-divergence term yields a lower variance 
    estimate of the likelihood lower bound compared to computing the term by Monte Carlo approxmation.

        .. math:: D_{KL}[q_{\phi}(z|x) || p_{\theta}(z)]

    See appendix D of [KINGMA]_ for details.

    Parameters
    ----------
    mean : Theano tensor
        Mean of the diagonal covariance Gaussian.
    logvar : Theano tensor
        Log variance of the diagonal covariance Gaussian.

    Returns
    -------
    Theano tensor
        Element-wise KL-divergence, this has to be summed when the Gaussian distributions are multi-variate.

    References
    ----------
        ..  [KINGMA] Kingma, Diederik P., and Max Welling.
            "Auto-encoding variational bayes."
            arXiv preprint arXiv:1312.6114 (2013).

    """
    return -0.5*(1 + logvar - mean**2 - T.exp(logvar))

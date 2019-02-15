import scipy.stats as sp
from jax import lax
from jax.numpy.lax_numpy import _promote_args
import jax.numpy as np


class jax_continuous(sp.rv_continuous):
    def rvs(self, *args, **kwargs):
        rng = kwargs.pop('random_state')
        size = kwargs.get('size', None)
        args = list(args)
        scale = kwargs.get('scale', args.pop())
        loc = kwargs.get('loc', args.pop())
        loc, scale, *args = _promote_args(self.rvs, loc, scale, *args)
        if not size:
            shapes = [np.shape(arg) for arg in args] + [np.shape(loc), np.shape(scale)]
            size = lax.broadcast_shapes(*shapes)
        else:
            args = [np.reshape(arg, size) for arg in args]
            loc = np.reshape(loc, size)
            scale = np.reshape(scale, size)
        self._random_state = rng
        self._size = size
        vals = self._rvs(*args)
        return vals * scale + loc

    def logpdf(self, x, *args, **kwargs):
        args = list(args)
        scale = kwargs.get('scale', args.pop())
        loc = kwargs.get('loc', args.pop())
        loc, scale, *args = np._promote_args_like(loc, scale, *args)
        x = (x - loc) / scale
        return self._logpdf(x) - np.log(scale)

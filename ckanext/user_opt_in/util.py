# encoding: utf-8
try:
    try:
        import packaging # direct use
    except ImportError:
        # v39.0 and above.
        try:
            from setuptools.extern import packaging
        except ImportError:
            # Before v39.0
            from pkg_resources.extern import packaging
    version = packaging.version
except ImportError:
    raise RuntimeError("The 'packaging' library is missing.")

__all__ = ['version']

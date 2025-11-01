"""MMRotate package bootstrap with soft compatibility checks.

This repo is co-located with multiple OpenMMLab libs. Older MMRotate
releases (e.g. 0.3.x) hard-assert on exact mmcv/mmdet ranges and eagerly
import all subpackages on import, which breaks unrelated workflows when the
package is present but not actually used.

To improve interoperability in this monorepo:
 - Replace hard version asserts with warnings.
 - Avoid eager imports of heavy subpackages. Users can import
   ``mmrotate.core``/``mmrotate.models`` explicitly in compatible envs.
"""

from .version import __version__, short_version

import warnings

try:  # soft import, only for version checks
    import mmcv  # type: ignore
    import mmdet  # type: ignore
except Exception as _e:  # pragma: no cover
    warnings.warn(
        f'mmrotate: failed to import mmcv/mmdet for version check: {_e}. '
        'Proceeding without validation; mmrotate features may be unavailable.'
    )
    mmcv = None  # type: ignore
    mmdet = None  # type: ignore


def digit_version(version_str):
    """Parse version string to comparable list of ints.

    Examples:
        '1.7.0' -> [1, 7, 0]
        '2.0.0rc1' -> [1, 9, 1, 1] (treat rc as pre-release)
    """
    dv = []
    for x in str(version_str).split('.'):
        if x.isdigit():
            dv.append(int(x))
        elif 'rc' in x:
            base, rc = x.split('rc', 1)
            dv.append(max(int(base) - 1, 0))
            if rc.isdigit():
                dv.append(int(rc))
    return dv


def _soft_compat_check():  # pragma: no cover
    try:
        if mmcv is not None:
            mmcv_min, mmcv_max = '1.5.3', '1.8.0'
            cur = digit_version(getattr(mmcv, '__version__', '0.0.0'))
            ok = digit_version(mmcv_min) <= cur and cur <= digit_version(mmcv_max)
            if not ok:
                warnings.warn(
                    f'MMRotate {__version__} detected MMCV {getattr(mmcv, "__version__", "?")}. '
                    f'Expected in [{mmcv_min}, {mmcv_max}]. Proceeding anyway.'
                )
        if mmdet is not None:
            mmdet_min, mmdet_max = '2.25.1', '3.0.0'
            cur = digit_version(getattr(mmdet, '__version__', '0.0.0'))
            ok = digit_version(mmdet_min) <= cur and cur < digit_version(mmdet_max)
            if not ok:
                warnings.warn(
                    f'MMRotate {__version__} detected MMDetection {getattr(mmdet, "__version__", "?")}. '
                    f'Expected in [{mmdet_min}, {mmdet_max}). Proceeding anyway.'
                )
    except Exception as e:
        warnings.warn(f'mmrotate: compatibility check failed: {e}')


_soft_compat_check()

# Do NOT eagerly import heavy subpackages to avoid pulling incompatible code
# when mmrotate is present but not used. Import explicitly where needed.

__all__ = ['__version__', 'short_version']

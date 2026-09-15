#!/bin/sh
set -eu

python -m pip install --disable-pip-version-check \
  /deps/semantic_projection_core-0.11.1-py3-none-any.whl \
  /wheel/astrowoof_natal_authoring-0.4.63-py3-none-any.whl
python -m pip check

mkdir -p /tmp/installed-tests
cp /repo/astrowoof_natal/tests/test_editorial_review_runtime.py /tmp/installed-tests/
cp /repo/astrowoof_natal/tests/test_editorial_runtime_capture_diagnostics.py /tmp/installed-tests/

cd /tmp
python -c "import importlib.metadata as m, astrowoof_natal_authoring as a; print('version', m.version('astrowoof-natal-authoring')); print('module', a.__file__); assert m.version('astrowoof-natal-authoring') == '0.4.63'; assert 'site-packages' in a.__file__"
astrowoof-release-smoke --require-installed
astrowoof-lifecycle-smoke
astrowoof-editorial-review-qa
python -m unittest discover -s /tmp/installed-tests -p 'test_*.py'

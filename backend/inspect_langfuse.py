import importlib, pkgutil, inspect, sys
import langfuse

print('langfuse.__file__ =', getattr(langfuse, '__file__', 'unknown'))
print('langfuse.__version__ =', getattr(langfuse, '__version__', 'unknown'))

print('\nTop-level packages/modules inside langfuse:')
try:
    for info in pkgutil.iter_modules(langfuse.__path__):
        print('  -', info.name)
except Exception as e:
    print('  (could not list submodules):', e)

candidates = [
    'langfuse.client',
    'langfuse.client.client',
    'langfuse.stateful',
    'langfuse.trace',
    'langfuse.client_sdk',
    'langfuse.sdk',
    'langfuse._client',
]

print('\nTrying common candidate modules for StatefulClient:')
for mod in candidates:
    try:
        m = importlib.import_module(mod)
        names = [n for n, _ in inspect.getmembers(m) if 'Stateful' in n]
        print(f'  Imported {mod!s}: found names ->', names)
    except Exception as e:
        print(f'  Cannot import {mod!s}:', e)

print('\nSearching entire langfuse package for symbols named StatefulClient (this may be slow):')
found = False
for importer, name, ispkg in pkgutil.walk_packages(langfuse.__path__, prefix='langfuse.'):
    try:
        m = importlib.import_module(name)
        for n, obj in inspect.getmembers(m):
            if n == 'StatefulClient' or 'StatefulClient' in n:
                print('  Found', n, 'in', name)
                found = True
    except Exception:
        pass

if not found:
    print('  StatefulClient not found in the installed langfuse package.')

# Also print top-level attributes
print('\nTop-level attributes of langfuse module:')
for n in sorted(name for name in dir(langfuse) if not n.startswith('_'))[:50]:
    print(' ', n)

# Exit with success
sys.exit(0)

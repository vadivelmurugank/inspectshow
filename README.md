# "inspectshow" module

*inspectshow* module lists all the module internals in a tree format. The
lists contains the SubPackages, Submodules, Classes, Functions, Methods and
Descriptors. The module also lists the global variables, mutable and immutable
sequences as part of module.

"inspectshow" uses functions of "inspect" module to iterate over the various
object types to list in tree format. The module also lists all the python
modules in the python path.

The primary users for "inspectshow" is for python programmers and for reverse engineering python module internals.

## inspectshow module usage

```bash
    As script:
        # Inspect show for given module
        python -m inspectshow <module/package>

        # Inspect show for all the modules in python path
        python -m inspectshow
```

```python
    As python module:
        import inspectshow
        show = inspectshow.tree()

        # inspectshow for given module/package
        show(<module/package>)

        # inspectshow for all modules
        show()
```

## inspectshow tree format
```
<Module>
 |-- <Module Name>
     :::: " os : OS routines for NT or Posix depending on what system we're on. "
 |-- [SUBPACKAGES]
 |-- [SUBMODULES ]
 |-- [CLASS   <mro>]
 |--   :::: - Classes and Method Resolution Order
 |-- [ FUNCTION  ]
 |--   ::::  - Function including "lambda" anonymous functions
 |-- [ROUTINE  ] - user-defined or built-in function or method
 |-- [ METHOD ]
 |--   :::::   - bound method
 |-- [ GENERATOR ]
 |--   ::::   - object is a generator with "yield" expressions
 |-- [ GENERATOR FUNCTION ]
 |--   ::::     - object is a generator function
 |-- [ TRACEBACK ]
 |--   ::::  - Traceback object
 |-- [ FRAME ]
 |--   :::: - Frame Object
 |-- [ CODE ]
 |--   :::: - Code Object
 |-- [ BUILTIN ]
 |--   :::: - built-in function or bound built-in method
 |-- [ ABSTRACT ]
 |--   :::: - object is abstract base class
     |-- MutableMapping
 |-- [ METHOD DESCRIPTOR ]
 |--   ::::  - Object has __get__ attribute but NOT __set__ attribute
 |-- [ DATA DESCRIPTOR ]
 |--   ::::  - Object has __get__, __set__, __delete__ attributes
 |-- [ GETSET DESCRIPTOR ]
 |-- [ MEMBER DESCRIPTOR ]
 |-- [ VARIABLES ]
     |-- [ GLOBALS ]
         |-- [ bool ]
         |-- [ int ]
         |-- [ float ]
         |-- [ complex ]
     |-- [ IMMUTABLE SEQUENCES ]
         |-- [ str ]
         |-- [ slice ]
         |-- [ tuple ]
         |-- [ frozenset ]
     |-- [ MUTABLE SEQUENCES ]
         |-- [ list ]
         |-- [ bytearray ]
         |-- [ set ]
     |-- [ MAPPING ]
         |-- [ dict ]
```


## Examples

###  inspectshow of 'os' module

```bash
#>python -m inspectshow os

os
 |-- os
 |-- ===> C:\WinPython-64bit-3.4.3.4\python-3.4.3.amd64\lib\os.py
     :::: " os : OS routines for NT or Posix depending on what system we're on. "
 |-- [SUBPACKAGES]
 |-- [SUBMODULES ]
     |-- os
         |-- errno
         |-- path
             |-- genericpath
                 |-- os
                     |-- errno
                     |-- path
                     |-- st
                     |-- sys
                 |-- stat
             |-- os
             |-- stat
             |-- sys
         |-- st
         |-- sys
 |-- [CLASS   <mro>]
 |--   :::: - Classes and Method Resolution Order
     |-- MutableMapping
             |-- <class 'collections.abc.MutableMapping'>
             |-- <class 'collections.abc.Mapping'>
             |-- <class 'collections.abc.Sized'>
             |-- <class 'collections.abc.Iterable'>
             |-- <class 'collections.abc.Container'>
             |-- <class 'object'>
     |-- _Environ
             |-- <class 'os._Environ'>
             |-- <class 'collections.abc.MutableMapping'>
             |-- <class 'collections.abc.Mapping'>
             |-- <class 'collections.abc.Sized'>
             |-- <class 'collections.abc.Iterable'>
             |-- <class 'collections.abc.Container'>
             |-- <class 'object'>
     |-- _wrap_close
             |-- <class 'os._wrap_close'>
             |-- <class 'object'>
     |-- error
             |-- <class 'OSError'>
             |-- <class 'Exception'>
             |-- <class 'BaseException'>
             |-- <class 'object'>
     |-- stat_result
             |-- <class 'os.stat_result'>
             |-- <class 'tuple'>
             |-- <class 'object'>
     |-- statvfs_result
             |-- <class 'os.statvfs_result'>
             |-- <class 'tuple'>
             |-- <class 'object'>
     |-- terminal_size
             |-- <class 'os.terminal_size'>
             |-- <class 'tuple'>
             |-- <class 'object'>
     |-- times_result
             |-- <class 'nt.times_result'>
             |-- <class 'tuple'>
             |-- <class 'object'>
     |-- uname_result
             |-- <class 'nt.uname_result'>
             |-- <class 'tuple'>
             |-- <class 'object'>
 |-- [ FUNCTION  ]
 |--   ::::  - Function including "lambda" anonymous functions
     |-- _execvpe (['file', 'args', 'env'])
     |-- _exists (['name'])
     |-- _get_exports_list (['module'])
     |-- _unsetenv (['key'])
     |-- execl (['file'])
     |-- execle (['file'])
     |-- execlp (['file'])
     |-- execlpe (['file'])
     |-- execvp (['file', 'args'])
     |-- execvpe (['file', 'args', 'env'])
     |-- fdopen (['fd'])
     |-- fsdecode (['filename'])
     |-- fsencode (['filename'])
     |-- get_exec_path (['env'])
     |-- getenv (['key', 'default'])
     |-- makedirs (['name', 'mode', 'exist_ok'])
     |-- popen (['cmd', 'mode', 'buffering'])
     |-- removedirs (['name'])
     |-- renames (['old', 'new'])
     |-- spawnl (['mode', 'file'])
     |-- spawnle (['mode', 'file'])
     |-- walk (['top', 'topdown', 'onerror', 'followlinks'])
 |-- [ROUTINE  ] - user-defined or built-in function or method
     |-- _execvpe (['file', 'args', 'env'])
     |-- _exists (['name'])
     |-- _get_exports_list (['module'])
     |-- _unsetenv (['key'])
     |-- execl (['file'])
     |-- execle (['file'])
     |-- execlp (['file'])
     |-- execlpe (['file'])
     |-- execvp (['file', 'args'])
     |-- execvpe (['file', 'args', 'env'])
     |-- fdopen (['fd'])
     |-- fsdecode (['filename'])
     |-- fsencode (['filename'])
     |-- get_exec_path (['env'])
     |-- getenv (['key', 'default'])
     |-- makedirs (['name', 'mode', 'exist_ok'])
     |-- popen (['cmd', 'mode', 'buffering'])
     |-- removedirs (['name'])
     |-- renames (['old', 'new'])
     |-- spawnl (['mode', 'file'])
     |-- spawnle (['mode', 'file'])
     |-- walk (['top', 'topdown', 'onerror', 'followlinks'])
 |-- [ METHOD ]
 |--   :::::   - bound method
 |-- [ GENERATOR ]
 |--   ::::   - object is a generator with "yield" expressions
 |-- [ GENERATOR FUNCTION ]
 |--   ::::     - object is a generator function
     |-- walk (['top', 'topdown', 'onerror', 'followlinks'])
 |-- [ TRACEBACK ]
 |--   ::::  - Traceback object
 |-- [ FRAME ]
 |--   :::: - Frame Object
 |-- [ CODE ]
 |--   :::: - Code Object
 |-- [ BUILTIN ]
 |--   :::: - built-in function or bound built-in method
 |-- [ ABSTRACT ]
 |--   :::: - object is abstract base class
     |-- MutableMapping
 |-- [ METHOD DESCRIPTOR ]
 |--   ::::  - Object has __get__ attribute but NOT __set__ attribute
 |-- [ DATA DESCRIPTOR ]
 |--   ::::  - Object has __get__, __set__, __delete__ attributes
 |-- [ GETSET DESCRIPTOR ]
 |-- [ MEMBER DESCRIPTOR ]
 |-- [ VARIABLES ]
     |-- [ GLOBALS ]
         |-- [ bool ]
                 |-- os.supports_bytes_environ
         |-- [ int ]
                 |-- os.F_OK
                 |-- os.O_APPEND
                 |-- os.O_BINARY
                 |-- os.O_CREAT
                 |-- os.O_EXCL
                 |-- os.O_NOINHERIT
                 |-- os.O_RANDOM
                 |-- os.O_RDONLY
                 |-- os.O_RDWR
                 |-- os.O_SEQUENTIAL
                 |-- os.O_SHORT_LIVED
                 |-- os.O_TEMPORARY
                 |-- os.O_TEXT
                 |-- os.O_TRUNC
                 |-- os.O_WRONLY
                 |-- os.P_DETACH
                 |-- os.P_NOWAIT
                 |-- os.P_NOWAITO
                 |-- os.P_OVERLAY
                 |-- os.P_WAIT
                 |-- os.R_OK
                 |-- os.SEEK_CUR
                 |-- os.SEEK_END
                 |-- os.SEEK_SET
                 |-- os.TMP_MAX
                 |-- os.W_OK
                 |-- os.X_OK
         |-- [ float ]
         |-- [ complex ]
     |-- [ IMMUTABLE SEQUENCES ]
         |-- [ str ]
                 |-- os.altsep
                 |-- os.curdir
                 |-- os.defpath
                 |-- os.devnull
                 |-- os.extsep
                 |-- os.linesep
                 |-- os.name
                 |-- os.pardir
                 |-- os.pathsep
                 |-- os.sep
         |-- [ slice ]
         |-- [ tuple ]
         |-- [ frozenset ]
     |-- [ MUTABLE SEQUENCES ]
         |-- [ list ]
                 |-- os.__all__
         |-- [ bytearray ]
         |-- [ set ]
                 |-- os.supports_dir_fd
                 |-- os.supports_effective_ids
                 |-- os.supports_fd
                 |-- os.supports_follow_symlinks
     |-- [ MAPPING ]
         |-- [ dict ]
```


###  inspectshow of 'math' module

```bash
 
#>python inspectshow.py math

math
 |-- math
 |-- ===> Builtin Module
     :::: " math : This module is always available.  It provides access to the "
 |-- [SUBPACKAGES]
 |-- [SUBMODULES ]
     |-- math
 |-- [CLASS   <mro>]
 |--   :::: - Classes and Method Resolution Order
     |-- __loader__
             |-- <class '_frozen_importlib.BuiltinImporter'>
             |-- <class 'object'>
 |-- [ FUNCTION  ]
 |--   ::::  - Function including "lambda" anonymous functions
 |-- [ROUTINE  ] - user-defined or built-in function or method
 |-- [ METHOD ]
 |--   :::::   - bound method
 |-- [ GENERATOR ]
 |--   ::::   - object is a generator with "yield" expressions
 |-- [ GENERATOR FUNCTION ]
 |--   ::::     - object is a generator function
 |-- [ TRACEBACK ]
 |--   ::::  - Traceback object
 |-- [ FRAME ]
 |--   :::: - Frame Object
 |-- [ CODE ]
 |--   :::: - Code Object
 |-- [ BUILTIN ]
 |--   :::: - built-in function or bound built-in method
 |-- [ ABSTRACT ]
 |--   :::: - object is abstract base class
 |-- [ METHOD DESCRIPTOR ]
 |--   ::::  - Object has __get__ attribute but NOT __set__ attribute
 |-- [ DATA DESCRIPTOR ]
 |--   ::::  - Object has __get__, __set__, __delete__ attributes
 |-- [ GETSET DESCRIPTOR ]
 |-- [ MEMBER DESCRIPTOR ]
 |-- [ VARIABLES ]
     |-- [ GLOBALS ]
         |-- [ bool ]
         |-- [ int ]
         |-- [ float ]
                 |-- math.e
                 |-- math.pi
         |-- [ complex ]
     |-- [ IMMUTABLE SEQUENCES ]
         |-- [ str ]
         |-- [ slice ]
         |-- [ tuple ]
         |-- [ frozenset ]
     |-- [ MUTABLE SEQUENCES ]
         |-- [ list ]
         |-- [ bytearray ]
         |-- [ set ]
     |-- [ MAPPING ]
         |-- [ dict ]
```

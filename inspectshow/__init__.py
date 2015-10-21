"""
Module wrapper to show submodules, classes, methods and functions in a tree like
display. This modules uses inspect module to display the internals of a module.
"""

# Release info
__author__ = 'Vadivel'
__versioninfo__ = (0, 1)
__version__ = '.'.join(map(str,__versioninfo__))
COPYRIGHT = """\
Copyright (C) 2014-2015 Vad
"""

import inspect
import imp,os, glob
import pkgutil
import pydoc
import argparse
import imp
import importlib
import os, sys, errno

class tree:
    def __init__(self):
        self.Indent = 0
        self.Modules = []
        self.module_list = []
        self.pattern_skip=[]
        self.module_skip=['pythoncom']

    def __del__(self):
        pass

    def __call__(self, *args, **kwargs):
        if not args:
            self.show_allmodules()
        for arg in args:
            self.show(arg)
    
    # INDENTATION FUNCTIONS
    def dprint(self, *args):
       """ Function to print lines indented according to level """
       print(' '*self.Indent,"|--", *args)

    def indent(self):
       """ Increase indentation """
       self.Indent += 4

    def dedent(self):
       """ Decrease indentation """
       self.Indent -= 4

    def show_doc(self, ObjMod):
        doc=ObjMod.__doc__
        if (doc and doc is not None):
            doc=doc.split('\n')
            if '' in doc: doc.remove('')
            self.indent()
            print(' '*self.Indent,"::::", "\"",ObjMod.__name__, ":", doc[0],"\"")
            self.dedent()

    def show_allmodules(self):
        s=sys.path
        print("Seaching Modules in the path :", s, "\n")
        self.dprint("[ MODULES ]")
        self.indent()
        #for im, mod, pkg in pkgutil.walk_packages(path=s, onerror=lambda x: None):
        for im, mod, pkg in pkgutil.iter_modules():
            skip=0
            if mod in self.module_skip:
                skip=1
            for skipstr in self.pattern_skip:
                if (mod.find(skipstr) > -1):
                    self.dprint("  + Skipped", mod)
                    skip=1
            if skip:
                continue

            print("\n", "="*60, "\n", "\t", mod, "\n", "="*60)
            self.show(mod)
        self.dedent()

    def show_submodules(self, modulestr):
        if modulestr in sys.builtin_module_names:
            return
        f, path, desc = imp.find_module(modulestr)
        if not (desc[2] == imp.C_BUILTIN):
            pkgpath=os.path.dirname(path)
            self.dprint("[ SUBMODULES ]")
            self.indent()
            for importer, modname, pkg in pkgutil.walk_packages(path=[pkgpath], prefix=modulestr+'.',onerror=lambda x: None):
                self.dprint(modname)
                try:
                    importlib.import_module(modname)
                except Exception as e:
                    self.dprint(" + Error", e.__doc__, ":", modname)
                    pass
            self.dedent()

    def show_classes(self, module):
        for name, data in inspect.getmembers(module, inspect.isclass):
            self.dprint ("%s" %name)
            cls=getattr(module, name)
            cltree=(inspect.getmro(cls))
            self.indent()
            self.indent()
            for indx in range(len(cltree)): self.dprint(cltree[indx])
            self.dedent()
            self.dedent()

    def show_function(self, module, name):
        fn=getattr(module, name)
        try:
            list=inspect.getargspec(fn)
            #self.dprint("%s (%s)" %(name, str(inspect.signature(fn))))
            self.dprint("%s (%s)" %(name, list[0]))
            #self.dprint(fn.__doc__)
            #self.dprint("(varargs) - %s" %list[1])
            #self.dprint("(keywords)- %s" %list[2])
            #self.dprint("(defaults)- %s" %list[3])
        except: pass

    def print_variable_type(self, objType):
        default_vars=["__builtins__", "__doc__","__path__", "__cached__", "__file__", "__name__", "__package__", "__version__"]
        self.dprint("[ %s ]" %objType.__name__)
        self.indent();self.indent()
        for ModObj in self.Modules:
            for name in dir(ModObj):
                obj = getattr(ModObj, name)
                #print(name, ":", type(obj))
                if not (inspect.isclass(obj) or
                    inspect.isfunction(obj)  or
                    inspect.isroutine(obj)  or
                    inspect.isfunction(obj)  or
                    inspect.isgeneratorfunction(obj)  or
                    inspect.isgenerator(obj)  or
                    inspect.istraceback(obj)  or
                    inspect.isframe(obj)      or
                    inspect.iscode(obj)       or
                    inspect.isabstract(obj)   or
                    inspect.ismethoddescriptor(obj)  or
                    inspect.isdatadescriptor(obj)    or
                    inspect.isgetsetdescriptor(obj)  or
                    inspect.ismemberdescriptor(obj)  or
                    inspect.isbuiltin(obj)):
                    if name not in default_vars:
                        if type(obj) is  objType:
                            ObjName = ModObj.__name__ + '.' + name
                            self.dprint("%s" %ObjName)
        self.dedent();self.dedent()

    def show_module(self, module):
        if module.__name__ in sys.builtin_module_names:
            return
        try:
            for name, data in inspect.getmembers(module, inspect.ismodule):
                self.indent()
                self.dprint ("%s" %name )
                if name not in self.module_list:
                    self.module_list.append(name)
                    obj=getattr(module,name)
                    self.show_module(obj)
                self.dedent()
        except Exception as e:
            print("Error:",e.__doc__,":", name)
            pass


    def show_subpackages(self, module):
        if module.__name__ in sys.builtin_module_names:
            return
        RootModule = [module.__name__]
        # Package dir name will be the root module name
        rootdir = os.path.basename(os.path.dirname(module.__file__))
        modname = module.__name__.split('.')[0]

        if (rootdir == modname) :
            for root, dir, files in os.walk( os.path.dirname(module.__file__), topdown=True):
                BaseModule = root
                for name in files:
                    if (name == ''.join(["__init__",".py"])):
                        if (os.path.basename(root) != module.__name__):
                            modlist=BaseModule.split(os.sep)
                            curr='.'.join(modlist[modlist.index(module.__name__.split('.')[0]):])
                            if curr not in RootModule:
                                RootModule.append(curr)
        #print(RootModule)
        for modname in RootModule:
            self.indent()
            try:
                mod=importlib.import_module(modname)
                if mod not in self.Modules:
                    self.Modules.append(mod)
                    self.dprint(modname)
                    show_doc(mod)
            except Exception as e:
                self.dprint(" + XXX Error", e.__doc__, ":", modname)
                pass
            self.dedent()

    def show(self, module):
        """ show the module object passed as argument
        including its classes and functions """
        self.Indent = 0
        module_name = module
        module_root = module_name.split('.')

        self.Modules=[]
        modname=''
        for module in module_root:
            module = (modname + '.' + module).strip('.')
            print(module)
            try:
                modobj = importlib.import_module(module)
                modname = modobj.__name__
                if modobj not in self.Modules:
                    self.Modules.append(modobj)
                    self.dprint(modobj.__name__)
                    if modobj.__name__ in sys.builtin_module_names:
                        self.dprint("===>", "Builtin Module")
                    else:
                        self.dprint("===>", modobj.__file__)
                    self.show_doc(modobj)
            except Exception as e:
                self.dprint(" + ==> Error", e.__doc__, ":", modname)
                pass
                return
            #print(modobj)

        if len(modname) == 0 :
            print("Module doesn't exist")
            return

        if (modname != module_name):
            self.dprint("Valid Module is:", modname)

        self.dprint ("[SUBPACKAGES]")
        for ModObj in self.Modules:
            if inspect.ismodule(ModObj):
                self.show_subpackages(ModObj)

        self.dprint ("[SUBMODULES ]")
        for ModObj in self.Modules:
            self.indent()
            self.dprint ("%s" %ModObj.__name__)
            self.module_list=[]
            self.show_module(ModObj)
            self.dedent()

        self.dprint ("[CLASS   <mro>]")
        self.dprint ("  :::: - Classes and Method Resolution Order")
        for ModObj in self.Modules:
            self.indent()
            self.show_classes(ModObj)
            self.dedent()

        self.dprint ("[ FUNCTION  ]")
        self.dprint ("  ::::  - Function including \"lambda\" anonymous functions")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isfunction):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[ROUTINE  ] - user-defined or built-in function or method")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isroutine):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[ METHOD ]")
        self.dprint ("  :::::   - bound method")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismethod):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[ GENERATOR ]")
        self.dprint ("  ::::   - object is a generator with \"yield\" expressions")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgenerator):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[ GENERATOR FUNCTION ]")
        self.dprint ("  ::::     - object is a generator function")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgeneratorfunction):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[ TRACEBACK ]")
        self.dprint ("  ::::  - Traceback object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.istraceback):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ FRAME ]")
        self.dprint ("  :::: - Frame Object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isframe):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ CODE ]")
        self.dprint ("  :::: - Code Object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.iscode):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ BUILTIN ]")
        self.dprint ("  :::: - built-in function or bound built-in method")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isbuiltin):
                self.show_function(ModObj, name)
        self.dedent()

        self.dprint ("[ ABSTRACT ]")
        self.dprint ("  :::: - object is abstract base class")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isabstract):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ METHOD DESCRIPTOR ]")
        self.dprint ("  ::::  - Object has __get__ attribute but NOT __set__ attribute")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismethoddescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ DATA DESCRIPTOR ]")
        self.dprint ("  ::::  - Object has __get__, __set__, __delete__ attributes")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isdatadescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ GETSET DESCRIPTOR ]")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgetsetdescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ MEMBER DESCRIPTOR ]")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismemberdescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[ VARIABLES ]")
        self.indent()
        self.dprint ("[ GLOBALS ]")
        self.indent()
        self.print_variable_type(bool)
        self.print_variable_type(int)
        self.print_variable_type(float)
        self.print_variable_type(complex)
        self.dedent()

        self.dprint ("[ IMMUTABLE SEQUENCES ]")
        self.indent()
        self.print_variable_type(str)
        self.print_variable_type(slice)
        #self.print_variable_type(bytes)
        self.print_variable_type(tuple)
        self.print_variable_type(frozenset)
        self.dedent()
        self.dprint ("[ MUTABLE SEQUENCES ]")
        self.indent()
        self.print_variable_type(list)
        self.print_variable_type(bytearray)
        self.print_variable_type(set)
        self.dedent()
        self.dprint ("[ MAPPING ]")
        self.indent()
        self.print_variable_type(dict)
        #self.print_variable_type(long)
        #self.print_variable_type(Ellipsis)
        #self.print_variable_type(buffer)
        self.dedent()
        self.dedent()

        #self.dedent()

    if 0:
        self.dprint("[ FRAMEINFO ]")
        self.indent()
        frame = inspect.currentframe()
        tb=inspect.getframeinfo(frame)
        self.dprint("function    : %s()" %tb.function)
        self.dprint("code_context: %s" %tb.code_context)
        self.dprint("filename    : %s" %tb.filename)
        self.dprint("lineno      : %s" %tb.lineno)

        #self.dprint(inspect.getouterframes(frame))
        #self.dprint(inspect.getargvalues(frame))
        self.dprint ("current frame %s" % inspect.currentframe())
        #self.dprint ("stack %s " % inspect.stack())
        stacklist=inspect.stack(5)
        for indx in range(len(stacklist)):
            val=stacklist[indx]
            self.indent()
            for indx in range(len(val)):
                self.dprint(val[indx])
            self.dedent()
        self.dprint ("trace %s " % inspect.trace())
        self.dedent()




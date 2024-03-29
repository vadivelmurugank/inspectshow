"""
Module wrapper to show submodules, classes, methods and functions in a tree like
display. This modules uses inspect module to display the internals of a module.
"""
from __future__ import print_function

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
import pdb
import modulefinder
import runpy
import types

class showtree:
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
            return
        for arg in args:
            # Check if it is a script file
            if (os.path.isfile(arg)):
                self.showFile(arg)
            else:
                self.show(arg)
    
    # INDENTATION FUNCTIONS
    def dprint(self, *args):
        """ Function to print lines indented according to level """
        if (type(list(args)[0]) == str):
            if '[@' in list(args)[0]:
                print("\n\n",' '*(self.Indent), ' '.join(str(astr) for astr in args))
                #print("\n\n",' '*(self.Indent),args)
                return
            if '@@doc' in list(args)[0]:
                print(' '*(self.Indent+4), ' '.join(str(astr) for astr in args))
                #print(' '*(self.Indent+4), args)
                return
        print(' '*self.Indent, "|-- ", ' '.join(str(astr) for astr in args))
        #print(' '*self.Indent, "|-- ", args)

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
            print(' '*self.Indent,"    @@doc :", "\"",ObjMod.__name__, ":", doc[0],"\"")
            self.dedent()

    def show_allmodules(self):
        s=sys.path
        print("Seaching Modules in the path :", s, "\n")
        self.dprint("[@ MODULES ]")
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
            self.dprint("[@ SUBMODULES ]")
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
            self.dprint ("[Class %s]" %name)
            self.indent()
            cls=getattr(module, name)
            cltree=(inspect.getmro(cls))
            self.indent()
            self.dprint("MRO - Class Member Resolution Order:")
            self.indent()
            self.indent()
            for indx in range(len(cltree)): self.dprint(cltree[indx])
            self.dedent()
            self.dedent()

            attrs = [attr for attr in dir(cls) if not attr.startswith("__")]
            objlist = set([ type(getattr(cls,attr)) for attr in attrs])
            for aobj in objlist: 
                self.dprint("[  %s  ]:" %(aobj.__name__))
                objmembers = [sstr for sstr in attrs if (isinstance(getattr(cls, sstr), aobj))]
                self.indent()
                self.indent()
                for memb in objmembers:
                    if inspect.isfunction(getattr(cls, memb)) is True:
                        try: 
                            self.dprint("%s (%s)" %(memb, inspect.getargspec(getattr(cls, memb))[0]))
                        except: pass
                    else:
                        self.dprint(memb)
                self.dedent()
                self.dedent()
            self.dedent()
            self.dedent()

    #def show_classmembers(self, module):

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
        self.dprint("[@ %s ]" %objType.__name__)
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
        try:
            RootModule = [module.__name__]
            # Package dir name will be the root module name
            modname = module.__name__.split('.')[0]
            rootdir = os.path.basename(os.path.dirname(module.__file__))
            #print("rootdir: ", rootdir , " modname : " , modname)

            for root, dir, files in os.walk( os.path.dirname(module.__file__), topdown=True):
                BaseModule = root
                for name in files:
                    if (name == ''.join(["__init__",".py"])):
                        modlist=BaseModule.split(os.sep)
                        #curr='.'.join(modlist[modlist.index(module.__name__.split('.')[0]):])
                        curr='.'.join(modlist[modlist.index(rootdir)+1:])
                        curr = modname + '.' + curr
                        #print("curr : ", curr , "root : ", root, " module.name: ", module.__name__, " modlist: ", modlist )
                        if curr not in RootModule:
                            RootModule.append(curr)
                            #print(RootModule)
                    else:
                        pyfile,extn = os.path.splitext(name)
                        if (extn[1:] == 'py'):
                            modlist=BaseModule.split(os.sep)
                            modfile = '.'.join(modlist[modlist.index(rootdir):])
                            modfile = modfile + "." + pyfile
                            #print("pyfile: ",pyfile,"mod: ",modfile)
                                #try:
                                # importlib.import_module(pyfile)
                                # if pyfile not in RootModule:
                                #   RootModule.append(pyfile)
                                #except Exception as e:
                                #pass

                            try:
                                importlib.import_module(modfile)
                                if modfile not in RootModule:
                                    RootModule.append(modfile)
                                    #printf("modfile:" , RootModule)
                            except Exception as e:
                                continue

        except Exception as e:
            pass

        for modname in RootModule:
            self.indent()
            try:
                #print("modname : ", modname)
                mod=importlib.import_module(modname)
                if mod not in self.Modules:
                    self.Modules.append(mod)
                    self.dprint(modname)
                    self.show_doc(mod)
            except Exception as e:
                #self.dprint(" + XXX Error", e.__doc__, ":", modname)
                try:
                    modroot = modname.split('.')[1:]
                    submod = '.'.join(modroot)
                    #print("submod :", submod)
                    mod=importlib.import_module(submod)
                    if mod not in self.Modules:
                        self.Modules.append(mod)
                        self.dprint(mod)
                        self.show_doc(mod)
                except Exception as e:
                    pass
            self.dedent()

    def showFile(self, file):
        """
        show the module, function, objects of a given python file
        """
        func=dict()
        mod=dict()
        builtin=dict()
        gen=dict()
        descrip=dict()
        cls=dict()
        strings=dict()
        ints=dict()
        dictn=list()
        if (sys.version_info < (3, 0)):
            fglobals = runpy.run_path(file)
        else:
            fglobals = runpy.run_path(file)
            #for kd, vd in fglobals.items():
            #    print(kd, ":::", type(vd), vd)
            
        for key, name in fglobals.items():
            #print(key, ":", type(name))
            #print(key, ":", name)
            func.update({key: name})      if inspect.isfunction(name) else None
            mod.update({key: name})       if inspect.ismodule(name) else None
            builtin.update({key: name})   if inspect.isbuiltin(name) else None
            gen.update({key: name})       if inspect.isgenerator(name) else None
            descrip.update({key: name})   if isinstance(name, types.GetSetDescriptorType) else None
            cls.update({key: name})       if inspect.isclass(name) else None
            strings.update({key: name})   if type(name) is str else None
            ints.update({key: name})      if type(name) is int else None
            dictn.append(name)     if (type(name) is dict) and (key != "__builtins__") else None

        def showfile_print(m):
            self.dprint(m[0])
            doc = m[1].__doc__
            if doc is not None:
                doc=doc.split('\n') 
                self.dprint("    :: ",doc[0])

        def showfile_print_function(m):
            fn = m[1]
            doc = m[1].__doc__
            try:
                list=inspect.getargspec(fn)
                self.dprint("%s (%s)" %(m[0], list[0]))
            except: pass

            if doc is not None:
                doc=doc.split('\n') 
                self.dprint("    :: ",doc[0])

        def showfile_print_class(m):
            self.dprint(m[0])
            cls = m[1]

            cltree=inspect.getmro(cls)
            self.indent()
            self.dprint("MRO - Class Member Resolution Order:")
            self.indent()
            self.indent()
            for indx in range(len(cltree)): self.dprint(cltree[indx])
            self.dedent()
            self.dedent()

            attrs = [attr for attr in dir(cls) if not attr.startswith("__")]
            objlist = set([ type(getattr(cls,attr)) for attr in attrs])
            for aobj in objlist: 
                self.dprint("[  %s  ]:" %(aobj.__name__))
                objmembers = [sstr for sstr in attrs if (isinstance(getattr(cls, sstr), aobj))]
                self.indent()
                self.indent()
                for memb in objmembers:
                    if inspect.isfunction(getattr(cls, memb)) is True:
                        try:
                            self.dprint("%s (%s)" %(memb, inspect.getargspec(getattr(cls, memb))[0]))
                        except: pass
                    else:
                        self.dprint(memb)
                self.dedent()
                self.dedent()
            self.dedent()

        self.dprint ("[@ IMPORTED MODULES  ]")
        self.indent()
        for m in mod.items():
            showfile_print(m)
        self.dedent()

        self.dprint ("[@ CLASSES  ]")
        self.indent()
        for c in cls.items():
            showfile_print_class(c)
        self.dedent()

        self.dprint ("[@ BUILTIN  ]")
        self.indent()
        for b in builtin.items():
            showfile_print(b)
        self.dedent()

        self.dprint ("[@ FUNCTION  ]")
        self.indent()
        for f in func.items():
            showfile_print_function(f)
        self.dedent()

        self.dprint ("[@ GENERATOR  ]")
        self.indent()
        for g in gen.items():
            showfile_print(g)
        self.dedent()

        self.dprint ("[@ DESCRIPTOR  ]")
        self.indent()
        for d in descrip.items():
            self.dprint(d[0])
        self.dedent()

        self.dprint ("[@ INTEGERS  ]")
        self.indent()
        for i in ints.items():
            self.dprint(i[0])
        self.dedent()

        self.dprint ("[@ STRINGS  ]")
        self.indent()
        for s in strings.items():
            self.dprint(s[0])
        self.dedent()

        self.dprint ("[@ DICTIONARY  ]")
        self.indent()
        for delem in dictn:
            for k, v in delem.items():
                self.dprint(k)
        self.dedent()

    def show_imported_modules(self, file):
        finder = modulefinder.ModuleFinder()
        a=finder.run_script(file)
        dir(a)

        print(' '*4,'Loaded modules')
        print('-'*50)
        for name, mod in finder.modules.items():
            print(' '*4, "|--", ' %s ' % name)
            print(' '*8, '   ', ','.join(mod.globalnames.keys()[:3]))

        print(' '*50)
        print(' '*4, 'Modules - NOT IMPORTED')
        print('-'*50)
        for name in finder.badmodules.iterkeys():
            print(' '*4, "|--", ' %s' % name)

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
                #return
            #print(modobj)

        if len(modname) == 0 :
            print("Module doesn't exist")
            return

        if (modname != module_name):
            self.dprint("Valid Module is:", modname)

        self.dprint ("[@SUBPACKAGES]")
        print(self.Modules)
        for modObj in self.Modules:
            if inspect.ismodule(modObj):
                self.show_subpackages(modObj)

        self.dprint ("[@SUBMODULES ]")
        for ModObj in self.Modules:
            self.indent()
            self.dprint ("%s" %ModObj.__name__)
            self.module_list=[]
            self.show_module(ModObj)
            self.dedent()

        self.dprint ("[@CLASS        ]")
        self.dprint (" @@doc : - Classes and Method Resolution Order")
        for ModObj in self.Modules:
            self.indent()
            self.show_classes(ModObj)
            self.dedent()

        self.dprint ("[@ FUNCTION  ]")
        self.dprint (" @@doc :  - Function including \"lambda\" anonymous functions")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isfunction):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[@ ROUTINE  ]")
        self.dprint (" @@doc :  user-defined or built-in function or method")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isroutine):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[@ METHOD ]")
        self.dprint (" @@doc ::   - bound method")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismethod):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[@ GENERATOR ]")
        self.dprint (" @@doc :   - object is a generator with \"yield\" expressions")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgenerator):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[@ GENERATOR FUNCTION ]")
        self.dprint (" @@doc :     - object is a generator function")
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgeneratorfunction):
                self.indent()
                self.show_function(ModObj, name)
                self.dedent()

        self.dprint ("[@ TRACEBACK ]")
        self.dprint (" @@doc :  - Traceback object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.istraceback):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ FRAME ]")
        self.dprint (" @@doc : - Frame Object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isframe):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ CODE ]")
        self.dprint (" @@doc : - Code Object")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.iscode):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ BUILTIN ]")
        self.dprint (" @@doc : - built-in function or bound built-in method")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isbuiltin):
                self.show_function(ModObj, name)
        self.dedent()

        self.dprint ("[@ ABSTRACT ]")
        self.dprint (" @@doc : - object is abstract base class")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isabstract):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ METHOD DESCRIPTOR ]")
        self.dprint (" @@doc :  - Object has __get__ attribute but NOT __set__ attribute")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismethoddescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ DATA DESCRIPTOR ]")
        self.dprint (" @@doc :  - Object has __get__, __set__, __delete__ attributes")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isdatadescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ GETSET DESCRIPTOR ]")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.isgetsetdescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ MEMBER DESCRIPTOR ]")
        self.indent()
        for ModObj in self.Modules:
            for name, data in inspect.getmembers(ModObj, inspect.ismemberdescriptor):
                self.dprint ("%s" %name )
        self.dedent()

        self.dprint ("[@ VARIABLES ]")
        self.indent()
        self.dprint ("[@ GLOBALS ]")
        self.indent()
        self.print_variable_type(bool)
        self.print_variable_type(int)
        self.print_variable_type(float)
        self.print_variable_type(complex)
        self.dedent()

        self.dprint ("[@ IMMUTABLE SEQUENCES ]")
        self.indent()
        self.print_variable_type(str)
        self.print_variable_type(slice)
        #self.print_variable_type(bytes)
        self.print_variable_type(tuple)
        self.print_variable_type(frozenset)
        self.dedent()
        self.dprint ("[@ MUTABLE SEQUENCES ]")
        self.indent()
        self.print_variable_type(list)
        self.print_variable_type(bytearray)
        self.print_variable_type(set)
        self.dedent()
        self.dprint ("[@ MAPPING ]")
        self.indent()
        self.print_variable_type(dict)
        #self.print_variable_type(long)
        #self.print_variable_type(Ellipsis)
        #self.print_variable_type(buffer)
        self.dedent()
        self.dedent()

        #self.dedent()

    if 0:
        self.dprint("[@ FRAMEINFO ]")
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

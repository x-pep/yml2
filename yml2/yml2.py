# YML 2.5.6 language definition

# written by VB.

import re
from pyPEG import keyword, _and, _not

# pyPEG:
#
#   basestring:     terminal symbol (characters)
#   keyword:        terminal symbol (keyword)
#   matchobj:       terminal symbols (regex, use for scanning symbols)
#   function:       named non-terminal symbol, recursive definition
#                   if you don't want naming in output, precede name with an underscore
#   tuple:          production sequence
#   integer:        count in production sequence:
#                    0: following element is optional
#                   -1: following element can be omitted or repeated endless
#                   -2: following element is required and can be repeated endless
#   list:           options, choose one of them
#   _not:           next element in production sequence is matched only if this would not
#   _and:           next element in production sequence is matched only if this would, too

newSyntax = True

def oldSyntax():
    global newSyntax
    newSyntax = False

def _if(cond, val):
    if cond:
        return val
    else:
        return ()

def listing(x):     return x, -1, (",", x)
r = re.compile

comment = [r(r"//.*"), r(r"/\*.*?\*/", re.S)]
_symbol = r"(?=\D)\w(\w|:)*"
symbol = r(_symbol, re.U)
pointer = r(r"\*" + _symbol, re.U)
ppointer = r(r"\*\*" + _symbol, re.U)
macro = r(r"\%" + _symbol, re.U)
reference = r(r"\&" + _symbol, re.U)

NameStartChar = ur''':|[A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]'''
NameChar = NameStartChar + ur'''|-|\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]'''

_xmlSymbol = u"(" + NameStartChar + u")(" + NameChar + u")*"
xmlSymbol = r(_xmlSymbol)
aliasSymbol = r(ur"-|(" + _xmlSymbol + ur")")

literal = [r(r'""".*?"""', re.S), r(r"'''.*?'''", re.S), r(r"""-?\d+\.\d*|-?\.\d+|-?\d+|".*?"|'.*?'""")]
filename = [("'", r(r"[^']*"), "'"), ('"', r(r'[^"]*'), '"'), r(r"[^\s;]+")]
ws = r(r"\s+", re.U)

def pyExp():        return "!", r(r"(!=|\\!|[^!])+"), "!"
value = [literal, pyExp]

def tagQuote():     return r(r"\].*|\<.*?\>")
def lineQuote():    return r(r"\|.*")
def quote():        return [r(r"\d*>.*"), (literal, 0, [";", "."])]
def parm():         return [([xmlSymbol, pyExp, pointer, macro], "=", [value, pointer, symbol]), value, pointer]
def parm_eq():      return [xmlSymbol, pyExp, pointer, macro], "=", [value, pointer, symbol]
parm_eq.__name__ = "parm"
_func = [symbol, ppointer, pointer, reference], _if(newSyntax, (-1, ("[", listing(parm), "]"))), 0, ("(", listing(parm), ")"), 0, listing(parm), -1, parm_eq
def pythonCall():   return keyword("python"), _func, [";", "."]
def declParm():     return [pointer, macro, xmlSymbol], 0, ("=", literal)
def alias():        return keyword("alias"), aliasSymbol
def descend():      return r(r"[+@*]" + _symbol, re.U)
def base():         return keyword("is"), symbol
def shape():        return symbol
def decl():         return symbol, 0, base, 0, ("<", listing(shape), ">"), -1, descend, _if(newSyntax, (-1, ("[", 0, listing(declParm), "]"))), 0, ("(", 0, listing(declParm), ")"), 0, alias, 0, content
def python():       return [r(r"!!.*?!!", re.S), r(r"!.*")]
def operator():     return 0, keyword("define"), keyword("operator"), literal, keyword("as"), r(r".*")
def constant():     return 0, keyword("define"), [pointer, symbol], "=", literal, 0, [";", "."]
def in_ns():        return keyword("in"), xmlSymbol, [_decl, ("{", -2, _decl, "}")]
_decl = keyword("decl"), listing(decl), [";", "."]
def textsection():  return r(r'(\|\|(\>*).*?\|\|(\>*))', re.S)
def textsectionu(): return r(r'(\>\>.*?\>\>)', re.S)
def include():      return keyword("include"), 0, reverse, 0, [ktext, kxml], filename, 0, [";", "."]
def func():         return _func, 0, content
def funclist():     return listing(func)
_cmd = funclist, 0, [";", "."]
_inner = [include, textsection, textsectionu, pythonCall, _cmd, quote, lineQuote, tagQuote, pyExp]
_cc = "{", -1, _inner, "}"
def content_plain(): return [ (_l, 0, _p, 0, _b, 0, _cc), (_p, 0, _b, 0, _cc), (_b, 0, _cc), _cc ]
content_plain.__name__ = "content"
def func_plain():   return _func, 0, content_plain
func_plain.__name__ = "func"
def flist_plain():  return -2, func_plain
flist_plain.__name__ = "funclist"
def xbase():        return flist_plain
def generic():      return flist_plain
def subscript():    return flist_plain
def parentheses():  return "(", 0, funclist, ")"
def fparm():        return flist_plain

_l = _if(newSyntax, ("<", listing(generic), ">"))
_p = _if(not newSyntax, parentheses), _if(newSyntax, ("(", 0, listing(fparm), ")"))
_b = (":", listing(xbase))
_c = [_inner, _cc]

def content():      return [ (_l, 0, _p, 0, _b, 0, _c), (_p, 0, _b, 0, _c), (_b, 0, _c), _c ]
def reverse():      return keyword("reverse")
def ktext():        return keyword("text")
def kxml():         return keyword("xml")
def ymlCStyle():    return -1, [_decl, in_ns, include, python, operator, constant, tagQuote, lineQuote, quote, _cmd]

from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from jsbachVisitor import jsbachVisitor
import sys
import os


_LILY_VERSION_ = "2.22.0"
_TEMPO_ = 120


class JSBachExceptions(Exception):

    def __init__(self, msgs, params):
        i = 1
        msg = msgs[0]
        for param in params:
            msg = msg + str(param) + " " + msgs[i] +  " "
            i = i + 1
        super().__init__(msg)


class EvalVisitor(jsbachVisitor):

    def __init__(self):

        self.arguments = {}
        self.methods = {}

        self.context = '__GLOBAL_VARIABLES__'
        self.variables = {}
        self.nivell_recursiu = {}

        self.initialMethod = None
        self.initialArguments = []

        self.reproducedNotes = []
        self.map_notes = {
            'A0': 0,
            'B0': 1,
            'C1': 2,
            'D1': 3,
            'E1': 4,
            'F1': 5,
            'G1': 6,
            'A1': 7,
            'B1': 8,
            'C2': 9,
            'D2': 10,
            'E2': 11,
            'F2': 12,
            'G2': 13,
            'A2': 14,
            'B2': 15,
            'C3': 16,
            'D3': 17,
            'E3': 18,
            'F3': 19,
            'G3': 20,
            'A3': 21,
            'B3': 22,
            'C4': 23,
            'D4': 24,
            'E4': 25,
            'F4': 26,
            'G4': 27,
            'A4': 28,
            'B4': 29,
            'C5': 30,
            'D5': 31,
            'E5': 32,
            'F5': 33,
            'G5': 34,
            'A5': 35,
            'B5': 36,
            'C6': 37,
            'D6': 38,
            'E6': 39,
            'F6': 40,
            'G6': 41,
            'A6': 42,
            'B6': 43,
            'C7': 44,
            'D7': 45,
            'E7': 46,
            'F7': 47,
            'G7': 48,
            'A7': 49,
            'B7': 50,
            'C8': 51,
            'C': 30,
            'D': 31,
            'E': 32,
            'F': 33,
            'G': 34,
            'A': 35,
            'B': 36
        }

    def setInitialMethod(self, method, args):
        self.initialMethod = method
        self.initialArguments = args

    def getProgramNotes(self):

        do_central = 4

        notes = []
        key_list = list(self.map_notes.keys())
        value_list = list(self.map_notes.values())
        for index, note in enumerate(self.reproducedNotes):
            note_not_parsed = key_list[value_list.index(note)]
            char_note = str(note_not_parsed[0]).lower()
            tempo_note = int(note_not_parsed[1])
            for i in range(do_central, tempo_note):
                char_note = char_note + "'"
            for i in range(tempo_note, do_central):
                char_note = char_note + ","
            notes.append(char_note)

        return notes

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        for el in l:
            self.visit(el)
        self.context = self.initialMethod
        self.omplirParams(self.context, self.context, self.initialArguments)
        for instr in self.methods[self.context]:
            self.visit(instr)

    def visitReproduirNota(self, ctx):
        l = list(ctx.getChildren())

        conjunt_notes = self.visit(l[1])

        if isinstance(conjunt_notes, list):
            for note in conjunt_notes:
                self.reproducedNotes.append(note)
        else:
            nota = self.visit(l[1])
            self.reproducedNotes.append(nota)

    def omplirParams(self, new_context, real_context, params):
        i = 0
        for p in params:
            self.variables[new_context][self.arguments[real_context][i]] = p
            i = i + 1

    def visitNota(self, ctx):
        l = list(ctx.getChildren())
        return self.map_notes[l[0].getText()]

    def visitAccedeixIessimArray(self, ctx):
        l = list(ctx.getChildren())
        index = self.visit(l[2])
        if isinstance(self.visit(l[0]), list):
            if index <= 0 or index > len(self.visit(l[0])):
                raise JSBachExceptions(
                    ["Index", "out of bounds."],
                    [index]
                )
                return None
            return self.visit(l[0])[index-1]

    def assignar(self, name_var, value_var):
        if self.context not in self.variables.keys():
            self.variables[self.context] = {}
        self.variables[self.context][name_var] = value_var

    def visitAfageixElementArray(self, ctx):
        l = list(ctx.getChildren())
        if isinstance(self.visit(l[0]), list):
            self.visit(l[0]).append(self.visit(l[2]))
        else:
            raise JSBachExceptions(
                ["Can't operate ", "as a array."], [l[0].getText()]
            )

    def visitSizeOfArray(self, ctx):
        l = list(ctx.getChildren())
        if not isinstance(self.visit(l[1]), list):
            raise JSBachExceptions(
                ["Can't operate ", "as a array."],
                [l[1].getText()]
            )
        else:
            return len(self.visit(l[1]))

    def visitEliminaIessimArray(self, ctx):
        l = list(ctx.getChildren())
        if not isinstance(self.visit(l[1]), list):
            raise JSBachExceptions(
                ["Can't operate ", "as an array."],
                [l[1].getText()]
            )
        else:
            index = self.visit(l[3])
            if index <= 0 or index > len(self.visit(l[1])):
                raise JSBachExceptions(
                    ["Index", "out of bounds."],
                    [index]
                )
                return None
            self.visit(l[1]).pop(index-1)

    def visitArray(self, ctx):
        l = list(ctx.getChildren())
        new_array = []
        for el in l[1:len(l)-1]:
            new_array.append(self.visit(el))
        return new_array

    def visitStringValue(self, ctx):
        return str(list(ctx.getChildren())[0]).replace('"', '')

    def visitConcatArray(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) + self.visit(l[2])

    def visitMultDiv(self, ctx):
        l = list(ctx.getChildren())
        if l[1].getText() == '*':
            return self.visit(l[0]) * self.visit(l[2])
        else:
            if self.visit(l[2]) == 0:
                raise JSBachExceptions(
                    ["Division by 0."],
                    []
                )
            return int(self.visit(l[0]) / self.visit(l[2]))

    def visitSuma(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) + self.visit(l[2])

    def visitResta(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) - self.visit(l[2])

    def visitMod(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) % self.visit(l[2])

    def visitValor(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitVar(self, ctx):
        l = list(ctx.getChildren())
        try:
            return self.variables[self.context][l[0].getText()]
        except:
            try:
                return self.variables['__GLOBAL_VARIABLES__'][l[0].getText()]
            except:
                raise JSBachExceptions(
                    ["Undefined variable ","."],
                    [l[0].getText()]
                )

    def visitBoolValue(self, ctx):
        l = list(ctx.getChildren())
        return l[0].getText() == 'true'

    def visitEscriu(self, ctx):
        l = list(ctx.getChildren())
        musicOutput = ""
        for el in l[1:len(l)]:
            musicOutput = musicOutput + str(self.visit(el))
        print(musicOutput)

    def visitIfStatement(self, ctx):
        l = list(ctx.getChildren())
        if not self.visit(l[1]):
            return False
        i = 3
        while i < len(l):
            if l[i].getText() == ':|':
                break
            self.visit(l[i])
            i = i + 1
        return i

    def visitIfElseStatement(self, ctx):
        l = list(ctx.getChildren())
        i = self.visitIfStatement(ctx)
        if not i:
            while l[i].getText() != 'else':
                i = i + 1
            while l[i+1].getText() != ':|':
                self.visit(l[i+1])
                i = i + 1

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        while self.visit(l[1]):
            for el in l[3:len(l)-1]:
                self.visit(el)

    def visitMethod(self, ctx):
        l = list(ctx.getChildren())
        local_variables = []
        method_instructions = []
        for i in range(1, len(l)):
            if l[i].getText() == '|:':
                break
            local_variables.append(l[i].getText())
        for i in range(i+1, len(l)-1):
            method_instructions.append(l[i].getText())
        self.methods[l[0].getText()] = (local_variables, method_instructions)

    def assigVector(self, source, value):
        value_Eval = self.visit(value)
        if source.getText() not in self.variables[self.context].keys() or self.variables[self.context][source.getText()] is None:
            self.variables[self.context][source.getText()] = value_Eval
        else:
            source_Eval = self.variables[self.context][source.getText()]
            while len(source_Eval) > 0:
                source_Eval.pop()
            for element in value_Eval:
                source_Eval.append(element)

    def visitAssig(self, ctx):
        l = list(ctx.getChildren())
        if self.context not in self.variables.keys():
            self.variables[self.context] = {}
        if isinstance(self.visit(l[2]), list):
            self.assigVector(l[0], l[2])
        else:
            self.variables[self.context][l[0].getText()] = self.visit(l[2])

    def visitLLegeix(self, ctx):
        l = list(ctx.getChildren())
        var = input()
        if var == 'true':
            var = True
        elif var == 'false':
            var = False
        else:
            var = int(var)
        if self.context not in self.variables.keys():
            self.variables[self.context] = {}
        self.variables[self.context][l[1].getText()] = var

    def visitDefMethod(self, ctx):
        l = list(ctx.getChildren())
        method_name = l[0].getText()
        if method_name in self.methods.keys():
            raise JSBachExceptions(
                ["Method ","already defined."],
                [method_name]
            )
            return None
        self.nivell_recursiu[method_name] = 0
        args = []
        i = 1
        while l[i].getText() != '|:':
            args.append(l[i].getText())
            i = i + 1
        self.variables[method_name] = {}
        self.arguments[method_name] = []
        self.methods[method_name] = []
        for arg in args:
            if arg in self.variables[method_name].keys():
                raise JSBachExceptions(
                    ["Parameter name ","repeated."],
                    [arg]
                )
            self.variables[method_name][arg] = None
            self.arguments[method_name].append(arg)
        i = i + 1
        while l[i].getText() != ':|':
            self.methods[method_name].append(l[i])
            i = i + 1

    def visitCallMethod(self, ctx):
        l = list(ctx.getChildren())
        if l[0].getText() not in self.methods.keys():
            raise JSBachExceptions(
                ["Undefined ", "method call."],
                [l[0].getText()]
            )
            return None
        if len(l)-1 != len(self.arguments[l[0].getText()]):
            raise JSBachExceptions(
                ["Number of parameters invalid on ", "call, were given", "needed","."],
                [l[0].getText(), len(l)-1, len(self.arguments[l[0].getText()])]
            )
            return None
        old_context = self.context
        real_context = l[0].getText()
        if self.nivell_recursiu[l[0].getText()] > 0:
            level = str(self.nivell_recursiu[l[0].getText()])
            new_context = l[0].getText() + "__rec__(" + level + ")"
            self.variables[new_context] = {}
            for variable in self.variables[old_context]:
                self.variables[new_context][variable] = None
        else:
            new_context = l[0].getText()
        new_level = self.nivell_recursiu[real_context]+1
        self.nivell_recursiu[real_context] = new_level
        params = []
        for element in l[1:len(l)]:
            params.append(self.visit(element))
        self.omplirParams(new_context, real_context, params)
        self.context = new_context
        instructions = self.methods[l[0].getText()]
        for instr in instructions:
            self.visit(instr)
        self.context = old_context
        self.variables.pop(new_context)

    def visitEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) == self.visit(l[2])

    def visitMore(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) > self.visit(l[2])

    def visitLess(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) < self.visit(l[2])

    def visitLessEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) <= self.visit(l[2])

    def visitGreaterEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) >= self.visit(l[2])

    def visitVarIf(self, ctx):
        l = list(ctx.getChildren())
        return self.visitVar(ctx)

    def visitDiff(self, ctx):
        l = list(ctx.getChildren())
        return not (self.visit(l[0]) == self.visit(l[2]))

    def visitEvalExprParentesis(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[1])


def generateMusic():
    notes = evaluator.getProgramNotes()
    if len(notes) == 0:
        print("No music generated...")
        return

    result = ""
    for note in notes:
        result = result + str(note) + " "
    result = '\n' + result
    fileData = ['\\version "'+_LILY_VERSION_+'"\n', "\\score {\n", "\\absolute {\n", "\\tempo 4 = "+str(_TEMPO_)+"\n", '}\n', "\\layout { }\n", "\\midi { }\n", '}']
    with open('musicOutput.lily', 'w') as f:
        code = ''
        i = 0
        for line in fileData:
            if i == 4:
                code = code + result + "\n}\n"
            else:
                code = code + line
            i = i + 1
        f.write(code)
    os.system("lilypond musicOutput.lily")
    os.system("timidity -Ow -o musicOutput.wav musicOutput.midi")
    os.system("ffmpeg -i musicOutput.wav -codec:a libmp3lame -qscale:a 2 musicOutput.mp3")

# SETTING LILY VERSION WITH -v
# SETTING LILY TEMPO WITH -t
i = 0

program_params = []
length_params = len(sys.argv)
ignore = False
for i in range(0, length_params):
    if ignore:
        ignore = False
        continue
    if sys.argv[i] == "-v":
        _LILY_VERSION_ = str(sys.argv[i+1])
        ignore = True
    elif sys.argv[i] == "-t":
        _TEMPO_ = str(sys.argv[i+1])
        ignore = True
    else:
        program_params.append(sys.argv[i])

input_stream = FileStream(program_params[1])
lexer = jsbachLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)
tree = parser.root()

evaluator = EvalVisitor()

if len(program_params) > 2:
    initial_params = program_params[3:len(program_params)]
    params = []
    for param in initial_params:
        try:
            params.append(int(param))
        except:
            params.append(str(param))
    evaluator.setInitialMethod(str(program_params[2]), params)
else:
    evaluator.setInitialMethod('Main', [])

evaluator.visit(tree)
print("\nProgram ended, press any key to generate the music...",end="")
input()
generateMusic()

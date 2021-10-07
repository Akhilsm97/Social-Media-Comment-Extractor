# def RemoveRedundentCharacters(comment):
#     comment = comment
#     processedcomment = comment[0]
#     for char in comment[1:]:
#         #if len(comment)>3:
#             if char != processedcomment[-1]: 
#                 processedcomment += char
#     print processedcomment
#     return processedcomment
class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)(\w)\2')
        self.repl = r'\1\2\3'

    def replace(self, word):
        repl_word = self.repeat_regexp.sub(self.repl, word)

        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word
import re
def RemoveRedundentCharacters(comment):
    comment=comment
    replacer = RepeatReplacer()
    pt = replacer.replace(comment)
    print(pt)
    return (pt)


   

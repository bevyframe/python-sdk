class widget_generators:
    def insides(inside):
        text = ''
        for part in inside: text = text + inside
        return text

def header1(inside, eclass, eid): return '<h1 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h1>'
def header2(inside, eclass, eid): return '<h2 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h2>'
def header3(inside, eclass, eid): return '<h3 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h3>'
def header4(inside, eclass, eid): return '<h4 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h4>'
def header5(inside, eclass, eid): return '<h5 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h5>'
def header6(inside, eclass, eid): return '<h6 class="'+eclass+'" id="'+eid+'">'+widget_generators.insides(inside)+'</h6>'
def link(inside, eclass, eid, ehref): return '<a class="'+eclass+'" id="'+eid+'" href="'+ehref+'">'+widget_generators.insides(inside)+'</a>'
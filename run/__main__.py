#+---------------------------------------------------------
#| Generates a SVG font from all svg files in ./svg
#| /usr/bin/python run
#|
#| Prerequisites: 
#| sudo apt-get install python-fontforge
#| pip2 install templite
#+---------------------------------------------------------

import fontforge, sys
from os import path, listdir
from templite import Templite

try:
   VERSION = sys.argv[1].strip()
except IndexError:
   sys.stderr.write('Usage: /usr/bin/python run VERSION\n')
   sys.exit(1)

font = fontforge.font()
font.encoding   = 'UnicodeFull'
font.version    = VERSION
font.weight     = 'Regular'
font.fontname   = 'octicons'
font.familyname = 'octicons'
font.fullname   = 'octicons'
font.em         = 96
font.ascent     = 84
font.descent    = 12

cwd        = path.dirname(__file__)
tpl        = Templite(open(path.join(cwd, 'template.css'), 'r').read())
glyphs     = []

# Get list of svg files
dirpath    = path.join(cwd, "svg")
files      = []

for filename in listdir(dirpath):
    filepath = path.join(dirpath, filename)

    if not path.isfile(filepath):
        continue

    (name, ext) = path.splitext(filename)
    if ext != '.svg':
        continue

    files.append((name, filepath))

# Generate svg font
base       = 61480
i          = 0

files.sort()
glyph = font.createChar(0, ".notdef")
glyph.importOutlines(path.join(cwd, ".notdef.svg"))

for name, filepath in files:
    glyph = font.createChar(base + i, name)
    glyph.importOutlines(filepath)

    glyphs.append((base + i, name))
    i += 1

font.generate(path.join(cwd, '..', 'octicons.svg'))  # Legacy iOS
font.generate(path.join(cwd, '..', 'octicons.ttf'))  # Safari, Android, iOS
font.generate(path.join(cwd, '..', 'octicons.woff')) # Modern Browsers

# Generate css
# templite doc : https://github.com/sametmax/templite
# template.css : https://cdnjs.cloudflare.com/ajax/libs/octicons/4.4.0/font/octicons.css
print tpl.render(
    version=VERSION,
    glyphs=glyphs,
    fontfaceStyles=True,
    iconsStyles=True,
    fontFamilyName='Octicons',
    classPrefix='octicon-',
    fontSrc1='', # url("octicons.eot")
    fontSrc2="""url("octicons.woff") format("woff"),
      url("octicons.ttf") format("truetype"),
      url("octicons.svg#octicons") format("svg")""",
)
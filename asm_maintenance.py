#!/usr/bin/python
#
# PERFORMANCES
# titles look like this:
# <title>ASM is Back (June 2, 2014) | Performances | Anti-Social Music</title>
# 
# Maintenance tasks follow:
#
# 1. replace:
# \t<meta http-equiv="X-UA-Compatible" content="IE=7" />
# with: 
# \t<meta http-equiv="X-UA-Compatible" content="IE=7" />
# \t<meta property="og:site_name" content="Anti-Social Music" />
# \t<meta property="og:url" content="http://www.antisocialmusic.org{path from root to filename}" />
# \t<meta property="og:title" content="{title}" /><------ from <title>, trim spaces, before |
# \t<meta property="og:image" content="http://www.antisocialmusic.org/ASM_social.jpg" />

import sys, re, errno


def ok(file):
    _file_types = [re.compile("^.*\.s?html$")]
    for found in _file_types:
        return found.match(file)


def do_check(path):
    try:
        os.makedirs(path, 755)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            exit(0)

# change process_file to do whatever maintenance tasks we want this time
def process_file(oldfile, newdir, start_dir, root):
    _title = re.compile("<title>([^\|]*) \|")
    _excess = re.compile(" *\(.+\) *")
    _found = ''
    _trimfile = oldfile.replace(start_dir, '', 1)
    _newfile = newdir + _trimfile
    _metafound = '\t<meta http-equiv="X-UA-Compatible" content="IE=7" />\n'
    # grrr
    do_check(newdir + root.replace(start_dir, '', 1))
    # let's get on with it
    with open(_newfile, 'w+') as n:
        with open(oldfile, 'r+') as o:
            for line in o:
                # see if we've found the title line yet
                if not _found:
                    # get the title out of it, if we are looking at the title line
                    for found in _title.finditer(line):
                        _found = found.group(1).strip()
                        if _found:
                            _found = re.sub(_excess, '', _found, 1)
                    # saved the title, so write the line
                    n.write(line)
                # we have the title
                else:
                    # operation 1: replace _metafound with block
                    if line == _metafound:
                        repl_template = """{line0}\t{line1}\n\t{line2}\n\t{line3}\n\t{line4}\n"""
                        repl_context = { "line0": _metafound,
                                         "line1": '<meta property="og:site_name" content="Anti-Social Music" />', 
                                         "line2": '<meta property="og:url" content="http://www.antisocialmusic.org%s" />' % _trimfile, 
                                         "line3": '<meta property="og:title" content="%s" />' % _found, 
                                         "line4": '<meta property="og:image" content="http://www.antisocialmusic.org/ASM_social.jpg" />'}
                        n.write(repl_template.format(**repl_context))
                    else:
                        n.write(line)
    return _found

# main
starting_directory = sys.argv[1]
newdir = starting_directory + '/../asm_maintenance' # a directory up so os.walk doesn't find it
os.mkdir(newdir)
for root,dirs,files in os.walk(starting_directory):
    for name in files:
#        print "%s\t%s\t%s" % (root, name, os.path.join(root, name))
        # get name, title (already have name)
        if ok(name):
            full_path=os.path.join(root,name)
            title=process_file(full_path,newdir,starting_directory,root)
            if title:
                print "%s:\t%s"%(full_path,title)
exit()

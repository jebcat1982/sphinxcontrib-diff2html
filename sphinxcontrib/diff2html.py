# -*- coding: utf-8 -*-
import codecs
import difflib
import hashlib
import os

from docutils import nodes
from sphinx.util import copyfile
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive


def builder_inited(app):
    scripts = app.builder.config.diff2html_scripts
    if scripts is not None:
        for script in scripts:
            app.add_javascript(script)
    else:
        app.add_javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/highlight.min.js')
        app.add_javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/languages/scala.min.js')

    if app.builder.config.diff2html_style is not None:
        app.add_stylesheet(app.builder.config.diff2html_style)
    else:
        app.add_stylesheet('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/styles/github.min.css')


def build_finished(app, exception):
    if exception is not None:
        return

    builder = app.builder

    # Get output _static folder.
    target_dir = os.path.join(builder.outdir, '_static', 'diff2html')
    # If targetDir is not exist, create it.
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    # copy resources to _static folder
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    html_resources = os.listdir(static_dir)
    for htmlResource in html_resources:
        copyfile(os.path.join(static_dir, htmlResource),
                 os.path.join(builder.outdir, '_static', 'diff2html', htmlResource))


class Diff2Html(nodes.General, nodes.Element):
    pass


class Diff2HtmlDirective(Directive):
    has_content = True
    option_spec = {'drawtype': directives.unchanged,
                   'showfiles': directives.flag,
                   'closeable': directives.flag}
    optional_arguments = 0

    def run(self):
        node = Diff2Html(self.block_text, **self.options)
        if self.content is not None or self.content is not '':
            node['content'] = self.content
        if 'drawtype' in self.options:
            node['drawtype'] = self.options['drawtype']
        if 'closeable' in self.options:
            node['closeable'] = True
        if 'showfiles' in self.options:
            node['showfiles'] = True

        return [node]


def get_diff_content(node):
    if 'content' in node and node['content'] is not None and node['content'] is not '':
        return node['content']
    elif 'fromfile' in node and 'tofile' in node:
        fromfile = os.path.abspath(node['fromfile'])
        tofile = os.path.abspath(node['tofile'])
        with codecs.open(fromfile, 'r', 'utf-8') as fromFileReader:
            fromfilelist = fromFileReader.readlines()
        with codecs.open(tofile, 'r', 'utf-8') as toFileReader:
            tofilelist = toFileReader.readlines()

        result = difflib.unified_diff(fromfilelist,
                                      tofilelist,
                                      fromfile=os.path.basename(fromfile),
                                      tofile=os.path.basename(tofile))
        return result
    else:
        return None


def get_div_id_key(content_list):
    content_str = ''
    for line in content_list:
        content_str += line
    return hashlib.md5(content_str.encode('utf-8')).hexdigest()


def html_visit_diff2html(self, node):
    content = get_diff_content(node)
    div_key = get_div_id_key(content)
    draw_type = None

    if 'drawtype' in node:
        draw_type = node['drawtype']

    show_files = 'false'
    if 'showfiles' in node:
        show_files = 'true'

    self.body.append('<div id="' + div_key + '" style="margin: 0; max-width: 100%;"></div>\n')
    self.body.append('<script>\n')
    self.body.append('var lineDiffExample = \n')
    for r in content:
        self.body.append(' + \'' + r.rstrip() + '\\n\'\n')
    self.body.append('$(document).ready(function()\n')
    self.body.append('{\n')
    self.body.append('  var\n')
    self.body.append('diff2htmlUi = new Diff2HtmlUI({diff: lineDiffExample});\n')
    if draw_type is None:
        self.body.append(
            'diff2htmlUi.draw(\'#' + div_key + '\', {inputFormat: \'json\', showFiles: ' + show_files +
            ', matching: \'words\'});\n')
    else:
        self.body.append(
            'diff2htmlUi.draw(\'#' + div_key + '\', {inputFormat: \'json\', showFiles: ' + show_files +
            ', matching: \'words\', outputFormat: \'side-by-side\'});\n')

    # closeable
    if 'closeable' in node:
        self.body.append('diff2htmlUi.fileListCloseable(\'#' + div_key + '\', false);\n')
    # HilightCode
    self.body.append('diff2htmlUi.highlightCode(\'#' + div_key + '\');\n')
    self.body.append('});\n')
    self.body.append('</script>')
    raise nodes.SkipNode


def setup(app):
    app.add_config_value('diff2html_scripts', None, 'html')
    app.add_config_value('diff2html_style', None, 'html')

    app.add_javascript('diff2html/diff2html.min.js')
    app.add_javascript('diff2html/diff2html-ui.min.js')
    app.add_stylesheet('diff2html/diff2html.min.css')
    app.add_node(Diff2Html, html=(html_visit_diff2html, None))
    app.add_directive('diff2html', Diff2HtmlDirective)
    app.connect('builder-inited', builder_inited)
    app.connect('build-finished', build_finished)

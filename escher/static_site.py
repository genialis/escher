from escher.plots import Builder

from os.path import join, dirname, realpath
from jinja2 import Environment, PackageLoader

# set up jinja2 template location
env = Environment(loader=PackageLoader('escher', 'templates'))

def generate_static_site():
    build_path = realpath(join(dirname(realpath(__file__)), '..'))
    print build_path

    # index file
    template = env.get_template('index.html')
    data = template.render(models=[],
                           maps=[],
                           web_version=True)
    with open(join(build_path, 'index.html'), 'w') as f:
        f.write(data)

    # viewer and builder
    for kind in ['viewer', 'builder']:
        for minified_js in [True, False]:
            js_source = 'web'
            enable_editing = (kind=='builder')

            # make the builder        
            builder = Builder(safe=True)
            
            filepath = join(build_path,
                            '%s%s.html' % (kind, '' if minified_js else '_not_minified'))
            html = builder.save_html(filepath=filepath,
                                     js_source=js_source,
                                     minified_js=minified_js,
                                     enable_editing=enable_editing,
                                     js_url_parse=True)
    
if __name__=='__main__':
    generate_static_site()

import plotly.express as px
from jinja2 import Template

# Opens a new brower tab
def sample_plot(x, y):
    fig = px.bar(x=x,y=y)
    fig.show()

def template_plot(data):
    print('here is the data',data[:10])
 #   fig = px.line(x=x,y=y)
    html_file = 'plots/chart.html'
    template = 'templates/plot.html'

#    jinja_data = {"fig": fig.to_html(full_html=False)}
#
#    with open(html_file,'w', encoding="utf-8") as fw:
#        with open(template,'r') as fr:
#            j2_template = Template(source=fr.read())
#           fw.write(j2_template.render(jinja_data))
#    return j2_template.render(jinja_data)
from bs4 import BeautifulSoup
from flask_cors import cross_origin
from supp import company_financials
from pretty_html_table import build_table
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        search_string = request.form['content'].replace(" ", "")
        content = company_financials(search_string)
        table = build_table(content, 'blue_light', font_size='small', font_family='Lucida Grande', text_align='right')
        financials = BeautifulSoup(table, 'html.parser')
        return render_template('main.html', tables=financials, company=search_string.upper())
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=8000, debug=True)

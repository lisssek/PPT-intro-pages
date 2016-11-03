from flask import Flask
from flask import render_template, request, flash
from MainFunction3 import clean_variables, translations, clean_variables2, translations2
from wtforms import Form, BooleanField, TextField, validators
from flask_cors import CORS, cross_origin
from flask import jsonify

app= Flask(__name__)
CORS(app)
app.secret_key = 'some_secret'

@app.route("/hello")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/post", methods=['POST'])
def postTest():
	results = []
	if request.method == 'POST':
		term = request.form['term'];
		results.append(term)
	return jsonify(results)

@app.route('/')
def index():
	return render_template("homepage.html")
@app.route('/projects_page1')
def projects_page_1():
	return render_template("projects_page1.html", methods=['GET', 'POST'])
@app.route('/projects_page2')
def projects_page_2():
	return render_template("projects_page2.html", methods=['GET', 'POST'])
@app.route('/projects_page3')
def projects_page_3():
	return render_template("projects_page3.html", methods=['GET', 'POST'])
@app.route('/projects_page4')
def projects_page_4():
	return render_template("projects_page4.html", methods=['GET', 'POST'])
@app.route('/data_standards_index')
def data_standards_index():
	return render_template("data_standards_index.html", methods=['GET', 'POST'])
@app.route('/translator')
def template_index():
	return render_template("translator2.html")
@app.route('/translator', methods=['POST'])
def input_dropdown():
		if request.method == 'POST':
			code=request.form['code']
			term = request.form['term']
			term=term.lower()
			code=code.upper()
			if term == '' and code=='':
				flash('Please input your search term or code')
				return render_template("translator2.html")
			if term !='':
				source=request.form['source']
				match=request.form['match']
				starting_classification=request.form['start']
				destination_classification=request.form['destination']
				results_in_list, DownloadUrl =clean_variables(source, match, term)
				translation=translations(results_in_list, source, starting_classification, destination_classification,)
				number_of_results=len(results_in_list)
				number_of_translations=len(translation)
				links=[]
 				for i in results_in_list:
 					a=i.split(':')
					uri=a[1]+':'+a[2]
					links.append(uri)
			if code !='':
				source=request.form['source']
				match=request.form['match']
				starting_classification=request.form['start']
				destination_classification=request.form['destination']
				if source=='er':
					flash('You forgot to choose your starting data standard!')
					return render_template("translator2.html")
				results_in_list, DownloadUrl =clean_variables2(source, match, code)
				translation=translations2(results_in_list, source, starting_classification, destination_classification)
				number_of_results=len(results_in_list)
				number_of_translations=len(translation)
 				links=[]
 				for i in results_in_list:
 					a=i.split(':')
  					if (a[0]=='Original code' or a[0]=='Translated code'):
   						links.append('')
  					else:
   						uri=a[1]+':'+a[2]
   						links.append(uri)

		return jsonify(no=number_of_results, no2=number_of_translations, trans=translation, DownloadXML=DownloadUrl, Links_and_Matches=zip(links,results_in_list), scroll='results')
if __name__=="__main__":
	app.run(debug=True)

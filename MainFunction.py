from xml.dom import minidom
from SPARQLWrapper import SPARQLWrapper, XML
from xml.etree.ElementTree import fromstring, ElementTree
import re

## Clean variables chosen by the user
def clean_variables(source, match, term):
	if source=="er":
	##call the right SPARQL endpoint
		URL1=[]
		URL2=[]
		URL3=[]
		baseURL1=URL1.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL1=URL1.append('Sectors')		
		sourceURL1=URL1.append('')
		sourceURL1=''.join(URL1)
		sourceURL1=str(sourceURL1)
		baseURL2=URL2.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL2=URL2.append('Surveys')		
		sourceURL2=URL2.append('')
		sourceURL2=''.join(URL2)
		sourceURL2=str(sourceURL2)
		print sourceURL2
		baseURL3=URL3.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL3=URL3.append('Indicators')		
		sourceURL3=URL3.append('')
		sourceURL3=''.join(URL3)
		sourceURL3=str(sourceURL3)
		print sourceURL3
	## build SPARQL query for use in Main.py
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?exactMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?closeMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?broadMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	# ## run SPARQLwrapper for all projects endpoints	
	## run search in SPARQL endpoint 1	
		sparql1 = SPARQLWrapper(sourceURL1, returnFormat=XML)
		setQuery1=sparql1.setQuery(QUERY)
		ret10 = sparql1.query()
		DownloadUrl=ret10.geturl()
	## run search in SPARQL endpoint 2	
		sparql2 = SPARQLWrapper(sourceURL2, returnFormat=XML)
		setQuery2=sparql2.setQuery(QUERY)
		ret20 = sparql2.query()
		DownloadUrl=ret20.geturl()
	## run search in SPARQL endpoint 3	
		sparql3 = SPARQLWrapper(sourceURL3, returnFormat=XML)
		setQuery3=sparql3.setQuery(QUERY)
		ret30 = sparql3.query()
		DownloadUrl=ret30.geturl()
	# ## use url to download results with <a href=url> in XML format	
		ret1 = sparql1.query()
		sparql1.setReturnFormat(XML)
		results1 = ret10.convert()
		ret11=results1.toxml('utf-8')

		ret2 = sparql2.query()
		sparql2.setReturnFormat(XML)
		results2 = ret20.convert()
		ret22=results2.toxml('utf-8')

		ret3 = sparql3.query()
		sparql3.setReturnFormat(XML)
		results3 = ret30.convert()
		ret33=results3.toxml('utf-8')

	# ## cleaning up xml results 
		root1=fromstring(ret11)
		root2=fromstring(ret22)
		root3=fromstring(ret33)
		ret300=[]
		results_clean=[]
		for result in root1.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root1.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Narrower match: ' + matchURI)
				if name=='prefLabel':
					prefLabel=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
		for result in root2.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root2.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Narrower match: ' + matchURI)
				if name=='prefLabel':
					prefLabel=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
		for result in root3.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root3.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret300.append('Narrower match: ' + matchURI)
				if name=='prefLabel':
					prefLabel=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
		results_clean_1 = ret300
		for i in results_clean_1:
		   if i not in results_clean:
			   results_clean.append(i)
	else:
		URL=[]
		baseURL=URL.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL=URL.append(source)
		sourceURL=URL.append('')
		sourceURL=''.join(URL)
		sourceURL=str(sourceURL)
		match=match.lower()
	## build SPARQL query for use in Main.py
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?exactMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?closeMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?broadMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	# ## run SPARQLwrapper	
		sparql = SPARQLWrapper(sourceURL, returnFormat=XML)
		setQuery=sparql.setQuery(QUERY)
		ret = sparql.query()
		DownloadUrl=ret.geturl()
	# ## use url to download results with <a href=url> in XML format	
		ret = sparql.query()
		sparql.setReturnFormat(XML)
		results = ret.convert()
		ret2=results.toxml('utf-8')
	# ## cleaning up xml results 
		root=fromstring(ret2)
		ret3=[]
		results_clean=[]
		for result in root.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Narrower match: ' + matchURI)
				if name=='prefLabel':
					prefLabel=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret3.append('Original concept name:' + prefLabel)	
		results_clean_1 = ret3
		for i in results_clean_1:
		   if i not in results_clean:
			   results_clean.append(i)
	
	return  results_clean, DownloadUrl
	
def translations(results_clean, source, starting_classification, destination_classification):	
	translations=[]
	for line in results_clean:
		if starting_classification !='er' or destination_classification !='er':
			a=line.split('/')
			bb=line.split(":")
			bbb=bb[1]+':'+bb[2]
			if a[3]=='Surveys':
				b=a[4]
				c=b.split('_')
				d=c[2]
				if d=='u5':
					d='mics5'
				if a[0]=='Original search term: http:':
					if starting_classification==d:
						translations.append(bbb)
				else:
					if destination_classification==d:
						translations.append(bbb)
			else:
				if a[0]=='Original search term: http:':
					if a[3]==source:
						if starting_classification==a[4]:
							translations.append(bbb)
				else:
					if destination_classification==a[4]:
						translations.append(bbb)
	translations_final=[]
	for i in translations:
		   if i not in translations_final:
			  translations_final.append(i)
	return translations_final
	
def clean_variables2(source, match, code):
	if source=="er": 
		URL4=[]
		URL5=[]
		URL6=[]
		baseURL4=URL4.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL4=URL4.append('Sectors')
		sourceURL4=URL4.append('')
		sourceURL4=''.join(URL4)
		sourceURL4=str(sourceURL4)
		baseURL5=URL5.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL5=URL5.append('Surveys')
		sourceURL5=URL5.append('')
		sourceURL5=''.join(URL5)
		sourceURL5=str(sourceURL5)
		baseURL6=URL6.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL6=URL6.append('Indicators')
		sourceURL6=URL6.append('')
		sourceURL6=''.join(URL6)
		sourceURL6=str(sourceURL6)
	## build SPARQL query for use in Main.py
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation), '"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?exactMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?closeMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?narrowMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?broadMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')	
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	# ## run SPARQLwrapper for endpoint A
		sparql5 = SPARQLWrapper(sourceURL5, returnFormat=XML)
		setQuery5=sparql5.setQuery(QUERY)
		ret50 = sparql5.query()
		DownloadUrl=ret50.geturl()
	# ## run SPARQLwrapper for endpoint B
		sparql6 = SPARQLWrapper(sourceURL6, returnFormat=XML)
		setQuery6=sparql6.setQuery(QUERY)
		ret60 = sparql6.query()
		DownloadUrl=ret60.geturl()
	# ## run SPARQLwrapper for endpoint C
		sparql4 = SPARQLWrapper(sourceURL4, returnFormat=XML)
		setQuery4=sparql4.setQuery(QUERY)
		ret40= sparql4.query()
		DownloadUrl=ret40.geturl()
	# # # ## use url to download results with <a href=url> in XML format	
		ret5= sparql5.query()
		sparql5.setReturnFormat(XML)
		results5 = ret5.convert()
		ret55=results5.toxml('utf-8')
		
		ret6= sparql6.query()
		sparql6.setReturnFormat(XML)
		results6 = ret6.convert()
		ret66=results6.toxml('utf-8')
		
		ret4= sparql4.query()
		sparql4.setReturnFormat(XML)
		results4= ret4.convert()
		ret44=results4.toxml('utf-8')
	# # # ## cleaning up xml results 
		root5=fromstring(ret55)
		root6=fromstring(ret66)
		root4=fromstring(ret44)
		ret800=[]
		results_clean=[]
		for result in root5.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root5.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Narrower match: ' + matchURI)
				if name=='notation':
					conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Original code: ' + conceptNotation)
				if name=='notation2':
					conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Translated code: ' + conceptNotation2)		
		for result in root6.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root6.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Narrower match: ' + matchURI)
				if name=='notation':
					conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Original code: ' + conceptNotation)
				if name=='notation2':
					conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Translated code: ' + conceptNotation2)	
		for result in root4.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root4.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret800.append('Narrower match: ' + matchURI)
				if name=='notation':
					conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Original code: ' + conceptNotation)
				if name=='notation2':
					conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret800.append('Translated code: ' + conceptNotation2)	
		results_clean_1 = ret800
		for i in results_clean_1:
		   if i not in results_clean:
			   results_clean.append(i)
	else:
		URL=[]
		baseURL=URL.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL=URL.append(source)
		sourceURL=URL.append('')
		sourceURL=''.join(URL)
		sourceURL=str(sourceURL)
	## build SPARQL query for use in Main.py
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation), '"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?exactMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?closeMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?narrowMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?broadMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')	
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	# ## run SPARQLwrapper
		sparql = SPARQLWrapper(sourceURL, returnFormat=XML)
		setQuery=sparql.setQuery(QUERY)
		ret = sparql.query()
		DownloadUrl=ret.geturl()
	# # # ## use url to download results with <a href=url> in XML format	
		ret = sparql.query()
		sparql.setReturnFormat(XML)
		results = ret.convert()
		ret2=results.toxml('utf-8')
	# # # ## cleaning up xml results 
		root=fromstring(ret2)
		ret3=[]
		results_clean=[]
		for result in root.iter('{http://www.w3.org/2005/sparql-results#}result'):
			for bindings in root.iter('{http://www.w3.org/2005/sparql-results#}binding'):
				name=bindings.get('name')
				if name=='Concept':
					conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Original search term: ' + conceptURI)
				if name=='exactMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Exact match: ' + matchURI)
				if name=='closeMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Closer match: ' + matchURI)
				if name=='broadMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Broader match: ' + matchURI)
				if name=='narrowMatch':
					matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
					ret3.append('Narrower match: ' + matchURI)
				if name=='notation':
					conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret3.append('Original code: ' + conceptNotation)
				if name=='notation2':
					conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
					ret3.append('Translated code: ' + conceptNotation2)			
		results_clean_1 = ret3
		for i in results_clean_1:
		   if i not in results_clean:
			   results_clean.append(i)
		  
	return  results_clean, DownloadUrl
	
def translations2(results_clean, source, starting_classification, destination_classification):	

	translations=[]
 	notations=[]
	prevLine = ""
	for line in results_clean:
		if starting_classification !='er' or destination_classification !='er':
			a=line.split(':')
			b=line.split('/')
			if a[0]=='Original search term':
				uri=a[1]+':'+a[2]
				if b[3]=='Surveys':
					c=b[4]
					c=c.split('_')
					d=c[2]
					if d=='u5':
						d='mics5'
					if starting_classification==d:
						translations.append(uri)
					prevLine=line.split(':')
				else:
					if b[3]==source:
						if starting_classification==b[4]:
							translations.append(uri)
					prevLine=line.split(':')
 			if prevLine[0]=='Original search term' and a[0]=='Exact match' or a[0]=='Closer match' or a[0]=='Broader match' or a[0]=='Narrower match':
   				uri=a[1]+':'+a[2] 				
  				if b[3]=='Surveys':
 					c=b[4]
 					c=c.split('_')
 					d=c[2]
 					if d=='u5':
 						d='mics5'
 					if destination_classification==b[4]:
 						translations.append(uri)
						prevLine=line.split(':')
 				else:
 					if b[3]==source:
 						if destination_classification==b[4]:
 							translations.append(uri)	
							prevLine=line.split(':')

			if a[0]=='Original code' and prevLine[0]=='Exact match' or prevLine[0]=='Closer match' or prevLine[0]=='Broader match' or prevLine[0]=='Narrower match':
				notation=a[1]
				translations.append(notation)
				prevLine=line.split(':')
				
			if a[0]=='Translated code' and prevLine[0]=='Original code':
				print line
				notation=a[1]
				translations.append(notation)

	translations_final=[]
	for i in translations:
	  translations_final.append(i)
	return translations_final

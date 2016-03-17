def init():
    build_html()

def build_html():
	html  = open( 'index.html', 'w+' )

	page  = create_html_skeleton()
	# static data block
	################# 
	# MUST BE FIXED #
	#################
	data  = [('@method', 'run'),
			 ('@author', 'ninjava'), 
			 ('@param',  'file_name:string')]

	table = assemble_table( data )

	i = page.index( '@insert' )
	page = ( page[:i] + table + page[i:] ).replace( '@insert', '' )
	
	html.write( page )
	html.close()

def assemble_table( doc_block ):
	components = [create_header(), create_body()]
	return build_table( components, doc_block )

def build_table( components, data ):
	table = '<table>'

	for component in components:
		table += assemble_content( component )
	table += '</table>' 

	# appends the documentation block to table
	rules = ['@name_block', '@content_block']
	for rule in rules:
		i = table.index( rule )
		table = ( table[:i] + ' CONTENT ' + '<hr />' + table[i:] ).replace( rule, '' )

	return table

def create_header():
	header = ['<thead>', '<tr>', '<th>@name_block']
	return generate_endings( header )

def create_body():
	body = ['<tbody>', '<tr>', '<td>@content_block']
	return generate_endings( body )

def generate_endings( tags ):
	"""
	generates the endings of html tags
	:param tags:list - list of tags
	:return basic html tags and html endings:zip
	"""
	endings = list()
	for tag in tags:
		ending = tag[:1] + '/' + tag[1:]
		endings.append( ending )

	# reverse list to get pairs in right order
	# Ex:
	# [( '<html>', '</p>'),
	#  ( '<head>', '</body>'),
	#  ( '<body>', '</head>'),
	#  ( '<p>',    '</html>')]
	endings = endings[::-1]

	return zip( tags, endings )

def create_html_skeleton():
	skeleton     = ['<html>', '<head>', '<body>', '<p>@insert']
	tags_list    = generate_endings( skeleton )
	html_content = assemble_content( tags_list )

	return html_content

def assemble_content( content_list ):
	content = ''
	for depth in range( 0, 2 ):
		for i in range( len( content_list ) ):
			content += content_list[i][depth]

	return content
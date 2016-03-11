import os
import webbrowser

# doc blocks in file
# you want to documented
block_counter  = 0
html_doc_block = {}

def run( file_name ):
    open_dist( file_name )     

def open_dist( file_name ):
    try:
        with open( file_name, 'r' ) as f:
            f_lines = list( f )
            detect_doc_block( f_lines )
    except IOError as e:
       print 'Unable to open file. File does not exist or no read permissions'
        
def detect_doc_block( f_content ):
    iterable_list = iter( f_content )
    doc_blocks    = list()
    
    for line in iterable_list:
        if line.startswith( '/*' ):
            l = line
            doc_blocks.append( format_output( l ) )
            while not l.startswith( '*/' ):
                l = next( iterable_list )
                doc_blocks.append( format_output( l ) )

            #get_doc_block( doc_blocks )
            detect_keywords( doc_blocks )
            doc_blocks = []
            
    fill_html_doc()
    
def format_output( content ):
    return content.split( '\n' )[0]

# debug method
#---------------------------------
def get_doc_block( doc_block ):
    for doc_line in doc_block:
        print doc_line
#---------------------------------
    
def detect_keywords( f_content ):
    # count of doc blocks in file
    global block_counter
    global html_doc_block
    doc_data_block = []
    block_counter  = block_counter + 1
    
    #doc_tags = ['@author', '@method', '@description', '@param']

    for line in f_content:
        doc_line_list = line.split()
        line_filter = filter( lambda s: s.startswith( '@' ), doc_line_list )
        if len( line_filter ):
            html_doc_block[block_counter] = doc_line_list
            doc_data_block.append( doc_line_list )
            
        html_doc_block[block_counter] = doc_data_block
        
def fill_html_doc():
    #print html_doc_block
    doc_name      = 'pydoc.html'
    html          = open( doc_name, 'w+' )
    html_doc_path = os.path.abspath( doc_name )

    # html doc
    raw_tags  = ["<html>", "<head>", "<body>", "<p>|"]
    full_tags = generate_endings( raw_tags )

    #doc_type, head, body, content = full_tags
    html_content = ''
    for depth in range( 0, 2 ):
        for index in range( len( full_tags ) ):
            html_content += full_tags[index][depth]

    # appends code block to html body
    html_doc_data = '<h2>Dir name:' + os.path.dirname( __file__ ) + '</h2>'
    for block_id, block in html_doc_block.iteritems():
        for doc in block:
            if '@description' in doc:
                doc[2] = ' '.join( doc[2:] )
                del doc[3:]

            # appends doc type
            html_doc_data += '<h3>' + doc[1] + '</h3>'

            # appends doc content
            html_doc_data += '<pre>' + doc[2] + '</pre>'
        html_doc_data += '<hr />'
        
    html_content = append_doc( html_doc_data, html_content )
    
    html.write( html_content )
    html.close()

    webbrowser.open_new_tab( html_doc_path )

def append_doc( doc, html_content ):
    i = html_content.index( '|' )
    return ( html_content[:i] + doc + html_content[i:] ).replace( '|', '' )

def generate_endings( tags ):
    endings = list()
    for tag in tags:
        ending = tag[:1] + '/' + tag[1:]
        endings.append( ending )

    # reverse list to get pairs in right order
    # [( '<html>', '</p>'),
    #  ( '<head>', '</body>'),
    #  ( '<body>', '</head>'),
    #  ( '<p>',    '</html>')]
    endings = endings[::-1]
    
    return zip( tags, endings )


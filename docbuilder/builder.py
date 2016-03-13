import os
import webbrowser

# doc blocks in file
# which will be documented
block_counter  = 0
html_doc_block = {}

def run( file_name ):
    """ main function that runs the module """
    if isinstance( file_name, str ):
        open_dist( file_name )
    else:
        print 'Unable to open file. String name required'

def open_dist( file_name ):
    """ opens file with the content,
        which will be documented """
    try:
        with open( file_name, 'r' ) as f:
            f_lines = list( f )
            detect_doc_block( f_lines, file_name )
    except IOError as e:
       print 'Unable to open file. File does not exist or no read permissions'
        
def detect_doc_block( f_content, f_name ):
    """ detects code block, which is surrounded
        with symbols /**/ and will be documented """
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
            
    fill_html_doc( f_name )
    
def detect_keywords( f_content ):
    """ detects keywords in code block, which is surrounded
        with symbols /**/ and will be documented """
    # count of doc blocks in file
    global block_counter
    global html_doc_block
    doc_data_block = []
    block_counter  = block_counter + 1

    for line in f_content:
        doc_line_list = line.split()
        line_filter = filter( lambda s: s.startswith( '@' ), doc_line_list )
        if len( line_filter ):
            html_doc_block[block_counter] = doc_line_list
            doc_data_block.append( doc_line_list )
            
        html_doc_block[block_counter] = doc_data_block
        
def fill_html_doc( f_doc_name ):
    """ generates html file with documented content """
    # creates directory with generated docs
    make_doc_dir()
    
    dest_doc      = f_doc_name.split( '.' )[0]   
    doc_name      = dest_doc + '_doc.html'
    html          = open( doc_name, 'w+' )
    html_doc_path = os.path.abspath( doc_name )

    # basic html tags
    raw_tags  = [ "<html>", "<head>", "<body>", "<p>|" ]
    full_tags = generate_endings( raw_tags )

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

    go_to_base_dir()
    
    webbrowser.open_new_tab( html_doc_path )

def append_doc( doc, html_content ):
    """ appends documented block to document's body """
    i = html_content.index( '|' )
    return ( html_content[:i] + doc + html_content[i:] ).replace( '|', '' )

def generate_endings( tags ):
    """ generates the endings of basic html tags """
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

    
def format_output( content ):
    """ returns formatted content string """
    return content.split( '\n' )[0]

def make_doc_dir():
    """ creates destination directory with generated docs """
    dir_path = os.path.dirname( __file__ ) + '/docs'
    
    if not os.path.exists( dir_path ):
        try:
            os.makedirs( dir_path )
            print 'Directory with generated docs has been successfully created.'
        except OSError as e:
            print 'Unable to create directory.'
    else:
        print 'Directory already exists. Changing path...'
    
    os.chdir( dir_path )

def go_to_base_dir():
    """ goes back to base directory """
    base_path = os.path.dirname( __file__ )
    os.chdir( base_path )
    

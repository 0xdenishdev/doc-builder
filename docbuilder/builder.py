import os
import webbrowser

# doc blocks in file
# which will be documented
block_counter  = 0
html_doc_block = {}

def run( file_name ):
    """
    main function that runs the module
    :param file_name:string
    """
    if isinstance( file_name, str ):
        open_dist( file_name )
    else:
        print 'Unable to open file. String name required'

def open_dist( file_name ):
    """
    opens the file with content,
    which will be documented
    :param file_name:string
    """
    try:
        with open( file_name, 'r' ) as f:
            f_lines = list( f )
            f_lines = map( lambda l: l.strip( ' \t\n\r' ), f_lines )
            detect_doc_block( f_lines, file_name )
    except IOError as e:
       print 'Unable to open file. File does not exist or no read permissions'

def detect_doc_block( f_content, f_name ):
    """
    detects the code block, which is surrounded
    with symbols \""" and will be documented
    :param f_content:list
    :param f_name:string - file name
    """
    global html_doc_block
    global block_counter

    indexes    = find_doc_block_indexes( f_content, '"""' )
    chunks     = get_chunks( indexes )

    for chunk in chunks:
        doc_line_list  = f_content[ chunk[0] + 1 : chunk[1] ]
        extracted_data = extract_by_keywords( doc_line_list )

        html_doc_block[ block_counter ] = extracted_data
        block_counter = block_counter + 1

    fill_html_doc( f_name )

def find_doc_block_indexes( content_list, item ):
    """
    finds the indexes' pairs occerred
    :param content_list:list
    :param item:string - occerred value
    :return the list of indexes
    """
    return [ i for i, x in enumerate( content_list ) if x == item ]

def get_chunks( content_list, chunk_size = 2 ):
    """
    returns the list of pairs indexes' occurred
    :param content_list:list
    :param chunk_size:int
    :return the list of indexes' pairs occurred
    """
    it = iter( content_list )
    return zip( *[it] * chunk_size )

def extract_by_keywords( line ):
    """
    returns the list with extracted keywords
    and values by keywords
    :param line:string
    :return formatted:list - formatted list of keywords
    """
    delim     = '|'
    key       = '@'
    formatted = list()

    for doc_data in line:
        if doc_data.count( key ) > 1:
            doc_data = doc_data.replace( key, '|@' ).split( delim )
            doc_data = filter( lambda l: l.startswith( key ), doc_data )

            for docs in doc_data:
                formatted.append( docs )
        else:
            formatted.append( doc_data )

    return formatted

def fill_html_doc( f_doc_name ):
    """
    generates html file with documented content
    :param f_doc_name:string - destination filename
    """
    # creates directory with generated docs
    create_doc_dir()

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
            doc_line_list = create_doc_line( doc )

            # appends doc type
            html_doc_data += '<h3>'  + doc_line_list[0] + '</h3>'
            # appends doc content
            html_doc_data += '<pre>' + doc_line_list[1] + '</pre>'
        html_doc_data += '<hr />'

    html_content = append_doc( html_doc_data, html_content )

    html.write( html_content )
    html.close()

    go_to_base_dir()

    webbrowser.open_new_tab( html_doc_path )

def create_doc_line( content ):
    """
    returns formatted doc line
    :param content:string
    :return content_list:list - formatted doc line
    """
    content_list    = content.split()
    content_list[1] = ' '.join( content_list[1:] )
    # removes all items after main content
    del content_list[2:]

    return content_list

def append_doc( doc, html_content ):
    """
    appends documented block to document's body
    :param doc:
    :param html_content:
    :return:
    """
    i = html_content.index( '|' )
    return ( html_content[:i] + doc + html_content[i:] ).replace( '|', '' )

def generate_endings( tags ):
    """
    generates the endings of basic html tags
    :param tags:list - list of basic html tags
    :return basic html tags and html endings:zip
    """
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
    """
    returns formatted content string
    :param content:string
    :return formatted content line:string
    """
    return content.strip().split( '\n' )[0]

def create_doc_dir():
    """
    creates destination directory with generated docs
    """
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
    """
    goes back to base directory
    """
    base_path = os.path.dirname( __file__ )
    os.chdir( base_path )
    

import markdown2


def convertMDfile_toHTML(file_name):
    
    with open(file_name+'.md', 'r') as f:
        text = f.read()
        html = markdown2.markdown(text)

    with open(file_name+'.html', 'w') as f:
        f.write(html)

    return True

def convertMDtoHTML(text):
    return  markdown2.markdown(text)


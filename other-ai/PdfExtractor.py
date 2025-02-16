from MyTimer import timer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from MyLogger import logger
@timer
def extract_text_from_pdf(filename,page_numbers=None,min_line_length=1):
    ''' 从PDF文件中(指定页码) 提取文字 '''
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页码
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # 按空行分隔，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' '+text) if not text.endswith(' ') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


@timer
def extract_text_from_pdf2(filename,page_numbers=None,min_line_length=1):
    ''' 从PDF文件中(指定页码) 提取文字 '''
    paragraphs = []
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页码
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text()
                if len(text) >= min_line_length:
                    paragraphs.append((' '+text) if not text.endswith(' ') else text.strip('-'))
                else:
                    paragraphs.append(text)                   
    
    '''
                #full_text += element.get_text() + '\n'
    # 按空行分隔，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' '+text) if not text.endswith(' ') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    '''

    
    logger.debug(f"paragraphs length:{len(paragraphs)}")
    return paragraphs 
if __name__ == "__main__":
    paragraphs1 = extract_text_from_pdf("./docs/财务业务中台项目概况.pdf",min_line_length=10)
    #paragraphs2 = extract_text_from_pdf2("SIGDIAL2023.pdf",min_line_length=10)

    logger.debug("paragraphs length: %s",len(paragraphs1))
    #print(len(paragraphs2))
    for para in paragraphs1[:4]:
        logger.debug(para)
 

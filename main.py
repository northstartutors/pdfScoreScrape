from PyPDF2 import PdfReader
import requests
import io
import re

### If not using dropbox links, this section will need to be replaced with file reading somehow, but you'll need to get a list to read sequentially

score_urls = ['https://www.dropbox.com/s/kvyrk20zcbbkw9o/2023_06_14%20Boots%2C%20Jack%20Practice%20SAT%20Score%20Report.pdf?dl=1']

### FOR LOOP TO PARSE ONE PDF AT A TIME -- EVERYTHING HERE GOES IN FOR LOOP

response = requests.get('https://www.dropbox.com/s/kvyrk20zcbbkw9o/2023_06_14%20Boots%2C%20Jack%20Practice%20SAT%20Score%20Report.pdf?dl=1')
with io.BytesIO(response.content) as f:
    pdf = PdfReader(f)
    page = pdf.pages[1]
    page_content = page.extract_text()
    
    ### AS SOON AS YOU'VE PULLED IN THE PDF, CHECK IF IT'S THE NEW VERSION OR THE OLD VERSION

    print(page_content)

    ### IF IT'S THE NEW VERSION:

    if re.search(r'Scores\sand\sHistory', page_content, flags=re.IGNORECASE):
        ### BASED ON THE TOTAL SCORE, IDENTIFY SAT VS ACT. SPLIT THOSE.
        match = re.search(r'Scores\sand\sHistory[\r\n\s]+([^\r\n]+)[\r\n\s]+([^\r\n]+)[\r\n\s]+([^\r\n]+)[\r\n\s]+([^\r\n]+)', page_content, flags=re.IGNORECASE)
        total = re.search(r'1600[\s]*(\d+)',match.group(1),flags=re.IGNORECASE)
        reading = re.search(r'400[\s]*(\d+)', match.group(2), flags=re.IGNORECASE)
        writing = re.search(r'400[\s]*(\d+)', match.group(3), flags=re.IGNORECASE)
        math = re.search(r'800[\s]*(\d+)', match.group(4), flags=re.IGNORECASE)
        ### MAKE SURE NAMES ARE STANDARDIZED IN THE DICTIONARIES FOR EACH CASE ALONG THE LINES OF BELOW:
        scores = {'reading': reading.group(1), 'writing': writing.group(1), 'math': math.group(1), 'total': total.group(1)}
        print(str(scores))

    ### IF IT'S THE OLD VERSION

import urllib2

if __name__ == '__main__':
    # The full path to the local machine's copy of the geographical locations file.
    LOCAL_FILE="c:\geolocations\geolocations.csv"

    # The Url of the geographical locations file available for download. 
    # This example uses 'en' (English). Supported locales are 'zh-Hant' (Traditional Chinese), 'en' (English), 'fr' (French), 
    # 'de' (German), 'it' (Italian), 'pt-BR' (Portuguese - Brazil), and 'es' (Spanish). 

    FILE_URL="https://api.bingads.microsoft.com/Api/SystemCodes/v1/en/GeoLocations.csv"

def output_status_message(message):
    print(message)

def get_last_e_tag():
    ''' 
    Returns an eTag if stored locally.
    '''
    file=None
    try:
        file=open("etag.txt")
        line=file.readline()
        file.close()
        return line if line else None
    except IOError:
        if file:
            file.close()
        return None

def save_e_tag(e_tag):
    ''' 
    Stores an eTag locally. 
    '''
    with open("etag.txt","w+") as file:
        file.write(e_tag)
        file.close()
    return None

def download_locations_file():
    CHUNK=16 * 1024
    with open(LOCAL_FILE, 'wb') as f:
        while True:
            chunk=response.read(CHUNK)
            if not chunk: break
            f.write(chunk)
            f.flush()

# Main execution
if __name__ == '__main__':    
    try:
        # You can set a request condition on either the last modified time or ETag of the file at the Url. 

        request=urllib2.Request(FILE_URL)
        request.add_header('If-None-Match', get_last_e_tag()) 
        response=urllib2.urlopen(request)
        
        save_e_tag(response.headers.get('ETag'))
        
        if response.getcode() == 200:
            download_locations_file()
            print("Downloaded the geographical locations to {0}.\n".format(LOCAL_FILE))
        
        output_status_message("Program execution completed")

    except urllib2.URLError as ex:
        if hasattr(ex, 'code'):
            if ex.code == 304:
                print("The locations file has not been modified since last download.\n")
            else:
                print("Error code: {0}".format(ex.code))
        elif hasattr(ex, 'reason'):
            print("Reason: {0}".format(ex.reason))
        
    except Exception as ex:
        output_status_message(ex)

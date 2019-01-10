from suds.plugin import MessagePlugin

class HeaderPlugin(MessagePlugin):
    def __init__(self):
        self.document = None

    def parsed(self, context):
        self.document = context.reply

    def get_response_header(self):
        result = {}
        envns = ('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
        soapenv = self.document.getChild('Envelope', envns)
        soapheaders = soapenv.getChild('Header', envns)
        SHeaderNodes = soapheaders.children

        for Node in SHeaderNodes:
            result[Node.name] = Node.text
        return result
from suds.plugin import MessagePlugin

class HeaderPlugin(MessagePlugin):
    def __init__(self):
        self.document = None

    def parsed(self, context):
        self.document = context.reply

    def get_headers(self, method):
        Result = {}
        method = method.method
        binding = method.binding.output
        SHeaderElem = binding.headpart_types(method, False)

        envns = ('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
        soapenv = self.document.getChild('Envelope', envns)
        soapheaders = soapenv.getChild('Header', envns)
        SHeaderNodes = soapheaders.children

        for Elem in SHeaderElem:
            for Node in SHeaderNodes:
                if(Node.name == Elem.name):
                    ElemRes = Elem.resolve(nobuiltin=True)
                    NodeRes = binding.unmarshaller().process(Node, ElemRes)
                    Result[Elem.name] = NodeRes
        return Result
    #
# -*- coding: utf-8 -*-

from cgi import escape

class BaseDocument:
    def __init__(self, block_klass):
        self.block_klass = block_klass
        self.blocks = None

    def parse(self, content):
	'''to be overridden'''	
	block_contents = list()
	return block_contents
        
    def transform(self, content):
	self.blocks = list()
        for i in self.parse(content):
            self.blocks.append(self.block_klass(i))
        def f(block):
            return block.assemble()
        return '\n'.join(map(f, self.blocks))
    
class BaseBlock:
    def __init__(self, content):
        self.content = content
        self.escaped_content = escape(content).replace("\n","<br/>") #escape and replace br
        self.cat = "default"
        self.subtype = None
    
    def get_category(self):
	'''to be overridden'''	
        self.cat = "default"
    
    def get_type(self):
	'''to be overridden'''	
        self.subtype = "default"
    
    def assemble(self):
        self.get_category()
        self.get_type()
        return BaseBlock.tag(self.cat, BaseBlock.tag(self.subtype, self.escaped_content))
        
    @staticmethod
    def tag(tag, content):
        if tag is not None:
            return "<p id=\"%s\">\n"%tag+content+"\n<p/>"
        else:
            return content

class SipBlock(BaseBlock):
    def get_category(self):
        return "sip"
    def get_type(self):
        return "legA"

if __name__=="__main__":
    msg='''aaa
    bbb
    ccc
    ddd
    eee'''
    def parser(content):
        return content.split('\n')
    d = Document(SipBlock, parser)
    print d.transform(msg)

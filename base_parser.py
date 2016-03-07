# -*- coding: utf-8 -*-

class BaseDocument:
    def __init__(self, block_klass):
        self.block_klass = block_klass

    def parse(self, content):
	'''to be overridden'''	
	block_contents = list()
	return block_contents
        
    def transform(self, content):
	blocks = list()
        for i in self.parse(content):
            blocks.append(self.block_klass(i))
        def f(block):
            return block.assemble()
        return ''.join(map(f, blocks))
    
class BaseBlock:
    def __init__(self, content):
        self.content = content
        self.cat = "default"
        self.subtype = None
    
    def get_category(self):
	'''to be overridden'''	
        self.cat = None
    
    def get_type(self):
	'''to be overridden'''	
        self.subtype = None
    
    def assemble(self):
        self.get_category()
        self.get_type()
        return BaseBlock.tag(self.cat, BaseBlock.tag(self.subtype, self.content.replace("\n","<br/>")))
        
    @staticmethod
    def tag(tag, content):
        if tag is not None:
            return "<%s>\n"%tag+content+"\n<%s/>"%tag
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

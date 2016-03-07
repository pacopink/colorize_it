#!/bin/env python
from base_parser import *

session_legs = None

class CtDocument(BaseDocument):
    '''override parse to parse ocg msg_trace file into blocks'''
    def parse(self, content):
	block_contents = list()
        block = ""
        flag = 0
        import re
        r = re.compile(r'.*->.*')
        for l in content.split("\n"):
            if l.find('write') == 0 or len(l) == 0:
                continue
            if r.match(l) is not None: #if meet '->' it is a begin of a block, save last block
                if len(block)>0:
                    #save last block and init a new block
                    block_contents.append(block)
                block = l+"\n"
            else:
                block += l+"\n"
        if len(block)>0:
            block_contents.append(block)
        global session_legs
        session_legs = list()#special handling, initial global variable here
	return block_contents


class CtBlock(BaseBlock):
    def get_category(self):
        if self.content.find("SoftSwitch")>=0 or self.content.find("MRS")>=0:
            self.cat = "sip"
        elif self.content.find("Diameter")>=0:
            self.cat = "dcc"
        elif self.content.find("SSP")>=0:
            self.cat = "ss7"
    
    def get_type(self):
        if self.cat != "sip":
            return
        import re
        r = re.compile(".*Call-ID\s*:\s*(.*?)\r\n", re.S|re.M)
        m = r.match(self.content, re.M)
        if m is None:
            return
        cid = m.groups()[0]
        while True:
            try:
                self.subtype = "leg_%d"%(session_legs.index(cid))
                break
            except:
                session_legs.append(cid)
                continue

if __name__=="__main__":
    f = open("./scf_0_11_1.ct", "r")
    doc=CtDocument(CtBlock)
    print doc.transform(f.read())
    f.close()

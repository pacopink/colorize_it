#!/bin/env python
from base_parser import *

class OcgDocument(BaseDocument):
    '''override parse to parse ocg msg_trace file into blocks'''
    def parse(self, content):
	block_contents = list()
        block = ""
        flag = 0
        import re
        r = re.compile(r'^-+$')
        for l in content.split("\n"):
            if r.match(l) is not None:
                if flag == 0: #meet first line of '---' begin of a block
                    flag = 1
                    if len(block)>0:
                        #save last block and init a new block
                        block_contents.append(block)
                    block = l+"\n"
                elif flag == 1: #meet the second line of '---' middle of block
                    flag = 0
                    block += l+"\n"
            else:
                block += l+"\n"
        if len(block)>0:
            block_contents.append(block)
	return block_contents
	

class OcgBlock(BaseBlock):
    def get_category(self):
        if self.content.find("SIP Message")>=0 or \
            self.content.find("Leg State Changed")>=0 or \
            self.content.find("ACK")>=0:
            self.cat = "sip"
        elif self.content.find("->SSP")>=0 or self.content.find("SSP->")>=0:
            self.cat = "ss7"
        elif self.content.find("DCC")>=0:
            self.cat = "dcc"
    
    def get_type(self):
        if self.cat != "sip":
            return
        import re
        r = re.compile(".*Leg\s+:\s+(\w).*", re.S|re.M)
        m = r.match(self.content, re.M)
        if m is not None:
            x = m.groups()[0]
            if x == "A":
                self.subtype = "leg_a"
            elif x == "B":
                self.subtype = "leg_b"
            elif x == "C":
                self.subtype = "leg_c"

if __name__=="__main__":
    f = open("./sample.msg", "r")
    doc=OcgDocument(OcgBlock)
    print doc.transform(f.read())
    f.close()



import json

class xfcontentAnalysis():
    def __init__(self,data):
        #self.dict = json.loads(data)
        #self.segid = self.dict["seg_id"]
        #cn = self.dict["cn"]
        #print(type(data))
        cn = data["cn"]
        st = cn['st']        
        self.type = st["type"]
        self.rt   = st['rt']
        #print(self.rt)
        
        

    def decode(self):
        result = ""
        #print(self.type)
        if self.type=="0":        
            for rtitem in self.rt:
                
                for wsitem in rtitem['ws']:
                    for witem in wsitem['cw']:
                        
                        result += witem["w"]
        return result
                        
                    
if __name__ ==  "__main__":
    xfc = xfcontentAnalysis("{\"seg_id\":28,\"cn\":{\"st\":{\"rt\":[{\"ws\":[{\"cw\":[{\"w\":\"，\",\"wp\":\"p\"}],\"wb\":25,\"we\":25},{\"cw\":[{\"w\":\"我们\",\"wp\":\"n\"}],\"wb\":25,\"we\":53},{\"cw\":[{\"w\":\"要\",\"wp\":\"n\"}],\"wb\":54,\"we\":68},{\"cw\":[{\"w\":\"吃\",\"wp\":\"n\"}],\"wb\":69,\"we\":114},{\"cw\":[{\"w\":\"大\",\"wp\":\"n\"}],\"wb\":115,\"we\":133},{\"cw\":[{\"w\":\"肉\",\"wp\":\"n\"}],\"wb\":134,\"we\":145},{\"cw\":[{\"w\":\"。\",\"wp\":\"p\"}],\"wb\":145,\"we\":145}]}],\"bg\":\"15880\",\"type\":\"0\",\"ed\":\"17280\"}}}")
    
    print(xfc.decode())
      
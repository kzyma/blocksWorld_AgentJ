
class knapsack():
    '''
        NEW BAG FUNCTIONALITY
    '''
    #Container - Simple Dictionary
    #How do I make this part of the agent?
    #http://docs.python.org/2/library/stdtypes.html#dict
    bag = {}
    
    #place(self,key,tag)
    #key is the name of the object in the bag
    #take the item out of the bag and put it down.
    def place(self,key):
        if(key in bag):
            item = bag[key]
            #item = bag[key]["obj"]
            self.state.addPropertyToLocation(key,item)
            del bag[key]
            return 0
        else:
            print("The bag doesn't contain am ",key)
            return 1

    #pick something up and store it
    def collect(self,key):
        t = self.state.getValueOfPropertyAtLocation(key)
        if t:
            bag[key] = t
            #bag[key]["obj"] = t
            #bag[key]["tags"] = type(t) + "Whatever you want to add as info, ex: executable, info, data, ect.."
            self.state.deletePropertyFromLocation(key)
            return bag[key]
        else:
            print("You're trying to pick up void.")
            return None

    #List the bags contents(keys)
    def bagContents():
        return bag.keys()
    
    #use something in the bag
    def use(key,removeOnUse=False):
        if( bag.has_key(key) ):
            value = bag[key]
            if( type(value)=="str" ):
                #print(key,": ",value)
                eval(bag[key])
            if( type(value).find('function') != -1 ):
                bag[key]()
            #I added this because, ya know, videogames, using an item that only 1 use is removed.
            #But it defaults to False, not to delete it. For obvious reasons.
            if( removeOnUse ):
                del bag[key]
            return value
        return 0
    #drop/destroy item in the bag
    #def
'''
"function_namewas"
"Name of Item" {
    type:"function"
    data:"source"
}
'''


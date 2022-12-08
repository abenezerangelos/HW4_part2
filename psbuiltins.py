# Name: Ebenezer Abate
# Collaborated with: Worked on it alone


from colors import *
from elements import StrConstant, DictConstant, CodeArray

class Stacks:
    def __init__(self,scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list############################although for this part dictstack has format [(0,{dict}),(staticlink,{dict})]
        self.staticlink=[]
        self.scope = scoperule
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if len(self.dictstack) > 0:
            x = self.dictstack[len(self.dictstack) - 1]
            self.dictstack.pop(len(self.dictstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):

            if len(self.dictstack) == 0:
                self.dictstack.append([0,{name: value}])
            else:
                diction=self.dictstack[-1][1]
                diction[name]=value



    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        name = "/" + name
        if self.scope=="static" and len(self.dictstack)!=0:
               end=len(self.dictstack)-1
               if name in self.dictstack[end][1]:
                   self.dictstack[-1][0]=end
                   return self.dictstack[end][1][name]
               else:


                   return self.lookuphelper(name, end)





        if self.scope=="dynamic":

           for i in reversed(range(len(self.dictstack))):
               if name in self.dictstack[i][1]:
                   return self.dictstack[i][1][name]
               elif name not in self.dictstack[i][1] and i==0:
                   return None
                   print("Error")
    def lookuphelper(self,name,index):
        pointer = self.dictstack[index][0]


        if name not in self.dictstack[index][1] and pointer != index:
            self.dictstack[index][0] = self.dictstack[index - 1][0]
            return self.lookuphelper(name, pointer)
        if name in self.dictstack[index][1]:
            self.dictstack[index][0] = index

            return self.dictstack[index][1][name]
        elif name not in self.dictstack[index][1] and pointer==index:
            self.dictstack[index][0]=self.dictstack[index-1][0]
            new=pointer

            return self.lookuphelper(name,new)#giving it a dynamic function| btw dont forget the tuplicity change to the code.



        return self.lookuphelper(name,pointer)


    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op2- op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op1 * op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, float)) and (isinstance(op2, int) or isinstance(op2, float)):
                self.opPush(op2 % op1)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of the StrConstant objects;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, bool)) and (isinstance(op2, int) or isinstance(op2, bool)):
               if op2 == op1:
                self.opPush(True)
               else:
                   self.opPush(False)
            elif (isinstance(op1, StrConstant) and isinstance(op2,StrConstant)):
                if op2.value == op1.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif (isinstance(op1,DictConstant)and isinstance(op2,DictConstant)):
                if id(op2)==id(op1):
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: add - one of the operands is not the proper type of value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, bool)) and (isinstance(op2, int) or isinstance(op2, bool)):
                if op2 < op1:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif (isinstance(op1, StrConstant) and isinstance(op2, StrConstant)):
                if op2.value < op1.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif (isinstance(op1, DictConstant) and isinstance(op2, DictConstant)):
                if id(op2) < id(op1):
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: add - one of the operands is not the proper type of value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):

        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1, int) or isinstance(op1, bool)) and (isinstance(op2, int) or isinstance(op2, bool)):
                if op2 > op1:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif (isinstance(op1, StrConstant) and isinstance(op2, StrConstant)):
                if op2.value > op1.value:
                    self.opPush(True)
                else:
                    self.opPush(False)
            elif (isinstance(op1, DictConstant) and isinstance(op2, DictConstant)):
                if id(op2) > id(op1):
                    self.opPush(True)
                else:
                    self.opPush(False)
            else:
                print("Error: add - one of the operands is not the proper type of value")
                self.opPush(op1)
                self.opPush(op2)
        else:
            print("Error: add expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        dictcounter=-1
        print(OKGREEN+"===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print("================="+CEND+"\n\n")
        print(RED+"===**dictstack**===")
        for item in reversed(self.dictstack):


            dictcounter += 1
            if (len(self.dictstack)-1)-dictcounter == item[0] and item[0]!=0:

                print(f"----{(len(self.dictstack)-1)-dictcounter}----{0}")
            else:
                print(f"----{(len(self.dictstack) - 1) - dictcounter}----{item[0]}")
            for (k,v) in item[1].items():
                    print(k,"    ",v)

        print("================="+ CEND)


    """
       Copies the top element in opstack.
    """

    def dup(self):
        if len(self.opstack) > 0:
            op1 = self.opPop()
            self.opPush(op1)
            self.opPush(op1)
            # print(opstack)
        else:
            print("Empty list cannot be duplicated")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
         if isinstance(self.opstack[len(self.opstack)-1],int):
             i=self.opPop()
             length=len(self.opstack)
             num=length-i
             while i>0:
                 self.opPush(self.opstack[num])
                 i-=1
                 num+=1
         else:
             print("ERROR: opstack doesn't have integer count")












    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
         self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        for i in range(len(self.opstack)):
            self.opPop()
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack)>1:
            op1=self.opPop()
            op2=self.opPop()
            self.opPush(op1)
            self.opPush(op2)
        else:
            raise ArithmeticError

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        x=""
        num_array= self.opPop()
        for i in range(num_array):
            x+="\x00"
        string= StrConstant(f'({x})')
        self.opPush(string)
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        self.opPop()
        self.opPush(DictConstant({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictConstant and StrConstant values.
    """
    def length(self):
        name=self.opPop()

        if isinstance(name,StrConstant):

            self.opPush(name.length())
        elif isinstance(name,DictConstant):


            self.opPush(name.length())

        else:
            print("Error: Please reuse a different method this is not the method for the right type")


    """ Pops either:
         -  "A (zero-based) index and an StrConstant value" from opstack OR 
         -  "A `name` (i.e., a key) and DictConstant value" from opstack.  
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictConstant, gets the value for the given `name` from DictConstant's dictionary value and pushes it onto the opstack
    """
    def get(self):
        num_name= self.opPop()
        obj= self.opPop()

        if isinstance(obj, StrConstant):
            fin=ord(obj.value[num_name+1])
            self.opPush(fin)

        elif isinstance(obj, DictConstant):
            self.opPush(obj.value[num_name])
        else:
            raise TypeError

   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StrConstant value from  opstack", OR
    - "An `item`, a `name`, and a DictConstant value from  opstack". 
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an DictConstant, adds (or updates) "name:item" in DictConstant's dictionary `value`.
    """
    def put(self):
       value= self.opPop()
       index= self.opPop()
       obj=self.opPop()
       if isinstance(obj, StrConstant):
           str=''
           for i in range(len(obj.value)):
               if i== index+1:
                str+=chr(value)
               else:
                str+=obj.value[i]

           obj.value=str



       elif isinstance(obj, DictConstant):
           obj.value[index]=value

       else:
           raise TypeError
    """
    getinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a `count`, a (zero-based) `index`, and an StrConstant value from  opstack, and 
    extracts a substring of length count from the `value` of StrConstant starting from `index`,
    pushes the substring back to opstack as a StrConstant value. 
    """ 
    def getinterval(self):
        count=self.opPop()
        index=self.opPop()
        string=self.opPop()
        new=string.value
        if isinstance(count,int) and isinstance(index,int) and isinstance(new,str):
            updated="("+new[index+1:count+index+1]+")"
            self.opPush(StrConstant(updated))




    """
    putinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a StrConstant value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StrConstant's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        string2= self.opPop()
        index=self.opPop()

        string1=self.opPop()

        if isinstance(string1, StrConstant) and isinstance(string2, StrConstant):

            string = string1.value
            d=string2.value
            if isinstance(d,str) and isinstance(index, int) and isinstance(string,str):
                d=d.strip("(").strip(")")
                x=(string[(index+1):(index+len(d)+1)])

                new=string.replace(x,d)
                string1.value=new
            else:
                raise TypeError
        else:
            raise TypeError




    """
    search is a string only operator, i.e., works only with StrConstant values. 
    Pops two StrConstant values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StrConstant values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
       seek=self.opPop()
       string=self.opPop()

       if isinstance(string, StrConstant) and isinstance(seek, StrConstant):
           string1 = string.value
           seek1 = seek.value
           string2=string1.strip("(").strip(")")
           seek2=seek1.strip("(").strip(")")
           if seek2 in string2:
               b=string2.split(seek2,1)
               for i in reversed(range(len(b))):
                   self.opPush(StrConstant("("+b[i]+")"))

                   if i==1:
                       self.opPush(StrConstant("("+seek2+")"))

               self.opPush(True)
           else:
               self.opPush(string)
               self.opPush(False)
               print("Error:String is not in the second string that is provided")





    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictConstant value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        #hence the name opdictionary because the opstack contains a dictionary and we are sending that dictionary to the dictstack
        opdictionary=self.opPop()
        if isinstance(opdictionary, DictConstant):
            self.dictPush(opdictionary.value)

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        if len(self.dictstack)>0:
            self.dictPop()
        else:
            raise TypeError
        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        value=self.opPop()
        name=self.opPop()


        self.define(name, value)




    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a Block and a boolean value, if the value is True, executes the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        block=self.opPop()
        boolean=self.opPop()
        if boolean==True and isinstance(block, CodeArray):
            block.apply(self)


    """ ifelse operator
        Pops two Blocks and a boolean value, if the value is True, executes the bottom Block otherwise executes the top Block.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        block2 =self.opPop()
        block1 = self.opPop()
        boolean = self.opPop()
        if boolean == True and isinstance(block2, CodeArray):
            block1.apply(self)
        else:
            block2.apply(self)


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a Block, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the Block. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
        block=self.opPop()
        end=self.opPop()
        inc=self.opPop()
        begin=self.opPop()
        if inc<0:
            while begin>=end:
                self.opPush(begin)
                block.apply(self)
                begin += inc
        if inc>0:
            while begin<=end:
                self.opPush(begin)
                block.apply(self)
                begin += inc


    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

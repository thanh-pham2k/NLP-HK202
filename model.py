
from util import raw_database, categorize_database


def retrieve_result(semantics):
    """
    Retrieve result list from procedure semantics
    ---------------------------------------------
    Args:
        semantics: dictionary created from nlp_parser.parse_to_procedure()
    """

    procedure_semantics = semantics#Chính là ngữ nghĩa thủ tục
    raw_database_=[raw.replace(':','') for raw in raw_database] 
    # print(raw_database_)#Dựa vào cơ sở raw

    database = categorize_database(raw_database_)
    # print(database['runtime'])
    procedure_semantics['arrival_time']=procedure_semantics['arrival_time'].replace(':','')
    procedure_semantics['departure_time']=procedure_semantics['departure_time'].replace(':','')
    # print(procedure_semantics)
    #remove unknown args: ?t ?f ?s
    query =  procedure_semantics['query']#'?r2'
    # print(query)             
    result_type = 'bus'
    
    for arg in list(procedure_semantics.keys()):
        print(arg)
        if '?' in procedure_semantics[arg] and procedure_semantics[arg] != query:
            procedure_semantics[arg] = ''
        elif procedure_semantics[arg] == query and arg != 'query':
            procedure_semantics[arg] = ''
            result_type = arg
    # print(result_type)             
    #Iterate after bus, ATIME and DTIME to have result
    bus_check_result=[]
    if (procedure_semantics['busname']!=''):#B3
        bus_check_result=procedure_semantics['busname']
    else:
        bus_check_result = [f.split()[1] for f in database['bus'] if procedure_semantics['bus'] in f]

    
    # print([a.split() for a in database['arrival']])

    arrival_bus_result = [a.split()[1] for a in database['arrival']
                            if procedure_semantics['arrival_location'] in a
                            and procedure_semantics['arrival_time'] in a
                            and a.split()[1] in bus_check_result]
    
    departure_bus_result = [d.split()[1] for d in database['departure'] 
                              if procedure_semantics['departure_location'] in d
                              and procedure_semantics['departure_time'] in d
                              and d.split()[1] in arrival_bus_result]

    runtime_bus_result = [d.split()[4] for d in database['runtime'] 
                          if procedure_semantics['departure_location'] in d.split()[2]
                          and procedure_semantics['arrival_location'] in d.split()[3]
                          and d.split()[1] in arrival_bus_result
                          and d.split()[1] in departure_bus_result]    

    if result_type == 'bus':
        result = departure_bus_result
    elif result_type == 'arrival_time':
        result = [a.split()[1] for a in database['arrival'] if a.split()[1] in departure_bus_result]
    elif result_type == 'departure_time':
        result = [d.split()[1] for d in database['departure'] if d.split()[1] in departure_bus_result]
    else:
        result = runtime_bus_result
    return result



file_name = ["output_a.txt","output_b.txt","output_c.txt","output_d.txt","output_e.txt","output_f.txt"]


def write_file(question_number,content):
    with open(file_name[question_number-1],"w",encoding="utf-8")as f:
        f.write(content)
    
import nltk
from nltk import grammar, parse
import argparse
from nltk.draw.tree import draw_trees
import spacy
from nltk import Tree
from spacy import displacy


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_,tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

def nltk_spacy_tree_visualize(sent,nlp):
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    doc = nlp(sent)
    displacy.serve(doc, style="dep")


def spacy_viet(inputText,visualSwitch):
    nlp = spacy.load('vi_spacy_model')
    token_def="Token def."
    token_def+='\n'
    token_def+='a. token.text, b. token.lemma_, c. token.pos_, d. token.tag_, e. token.dep_, f.token.shape_, g. token.is_alpha, h. token.is_stop'
    # print(token_def)
    token_def+='\n'
    doc = nlp(inputText)
    for index,token in enumerate(doc):
        temp="{}. a.{}, b.{}, c.{}, d.{}, e.{}, f.{}, g.{}, h.{}".format(index,token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
        # print(temp)
        token_def+=temp+'\n'
    
    print('\nNLTK spaCy Parse Tree')
    #-----------------Nghịch với tree -> in ra hình dáng đẹp hơn.
    result = [to_nltk_tree(sent.root) for sent in doc.sents]
    [root.pretty_print() for root in result]
    if visualSwitch=='on':
        nltk_spacy_tree_visualize(inputText,nlp)

    return (result,token_def,doc)


#--------------------------CODE FEATURE STRUCTURES

from nltk.featstruct import FeatStruct
from nltk.sem.logic import Variable, VariableExpression, Expression

def subtree_matcher(doc,dep,text=''): 
    #doc: Thời_gian xe bus B1 từ Hồ_Chí_Minh đến Huế  (đã được tách thành các token)
    #dep: mối quan hệ (det -> đại diện cho từ nào)
    #text: nào
    y = [] 
    # iterate through all the tokens in the input sentence 
    for tok in doc: 
        # extract subject
        if text=='': 
            if tok.dep_.endswith(dep): 
                y.append(tok.text)
        else:
            if tok.dep_.endswith(dep) and tok.text==text:
                y=tok.text
                break
    return y #trả về từ (vd: đến, nào)

def checkHead(doc,text):
    y=''
    for tok in doc: 
        # extract subject
        if text==tok.text:
            y=tok.head.text
    return y
def searchChild(doc,tag):
    y=''
    for tok in doc: 
        # extract subject
        if str(tok.dep_)==tag:
            y=tok.children
            return y
    return y

def parserGSVfeature(doc):
    """ Parsing doc -> structure {
            gap, 
            sem, 
            var
        }
    """
    departFlag=False
    departVpFlag=False
    arriveFlag=False
    sourceVpFlag=False
    destVpFlag=False
    busNameNpFlag=False
    destNpFlag=False
    d=''
    t=''
    a=''
    time=''
    nameDepart=''
    nameArrive=''
    bVar=''
    h_BusName=''
    busName=''
    timeDepart=''
    cityTokenText=['Hồ_Chí_Minh','Hà_Nội','Huế','Đà_nẵng','Đà_Nẵng']
    busTokenText=['B1','B2','B3','B4','B5','B6']
    cityTokenDep=['compound','nmod','obl']

    (f,typeWh)=('f2','WHICH1') if (subtree_matcher(doc,'det',text='nào') !=[]) else ('h1','HOWLONG1')
    
    if (typeWh=='WHICH1'):
        gap=f
    else:
        #Runtime (HOWLONG1 case)
        gap='r2'

    if (gap=='f2'):
        if subtree_matcher(doc,'case',text='đến')!=[] or subtree_matcher(doc,'ccomp',text='đến')!=[]:
            arriveFlag=True
            a='a3'
            try:
                time=[i.text for i in searchChild(doc,'ROOT') if 'HR' in i.text][0]
            except:
                time=''
            if time!='':    
                t='t2'
            else:
                t='?t'
            ################################################
            if subtree_matcher(doc,'ROOT',text='đi')!=[]:
                departFlag=True
                d='d3'
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)#Xét với thành phố HCM
                        tempHead=checkHead(doc,temp)
                        try:
                            tempChild=[i.text for i in searchChild(doc,cD)]
                        except:
                            tempChild=''
                            
                        if (temp !=[]) and (tempHead!='đi'):
                            destVpFlag=True
                            nameArrive= temp
                        elif (temp !=[]) and (tempHead=='đi') and ('từ' in tempChild):
                            sourceVpFlag=True
                            nameDepart= temp
                        elif (temp !=[]) and (tempHead=='đi') and ('đến' in tempChild):
                            destVpFlag=True
                            nameArrive= temp                                          
            else:
                for cT in cityTokenText:
                    for cD in cityTokenDep:
                        temp=subtree_matcher(doc,cD,cT)#Xét với Hà nội
                        if temp !=[]:
                            destNpFlag=True
                            nameArrive= temp
                            break
                    else:
                        # Continue if the inner loop wasn't broken.
                        continue
                        # Inner loop was broken, break the outer.
                    break
        elif subtree_matcher(doc,'ROOT',text='xuất_phát')!=[]:
            departFlag=True
            d='d3'
            for cT in cityTokenText:
                for cD in cityTokenDep:
                    temp=subtree_matcher(doc,cD,cT)
                    tempHead=checkHead(doc,temp)

                    if (temp !=[]) and (tempHead!='xuất_phát'):
                        departVpFlag=True
                        nameDepart= temp

    elif (gap=='r2'):
        if (subtree_matcher(doc,'ROOT',text='đến'))!=[]:
            arriveFlag=True 
            a='a3'
            time='?time'
            t='?t'
            nameArrive=subtree_matcher(doc,'obj')[0] if (len(subtree_matcher(doc,'obj'))==1) else subtree_matcher(doc,'obj')
            if type(nameArrive)==list:#duyệt danh sách (B1,Huế) -> vì 2 phần tử
                for obj in nameArrive:
                    if obj in cityTokenText:
                        nameArrive=obj
                        break
                
            if nameArrive!='':    
                h='h4'
                destVpFlag=True
            else:
                h='?h'

            if subtree_matcher(doc,'case',text='từ')!=[]:
                d='d3'    
                nameDepart=checkHead(doc,'từ')#'Hồ_Chí_Minh'
                if (nameDepart!=''):
                    sourceVpFlag
            listObj=subtree_matcher(doc,'obj')#['B1', 'Huế']
            listCompound=subtree_matcher(doc,'compound')#empty

            for sub in listObj:#B1 -> B1 trong busTokenText
                if sub in busTokenText:
                    busName=sub

            if busName=='':
                for sub in listCompound :
                    if sub in busTokenText:
                        busName=sub

            if busName!='':#Xe bus B1
                busNameNpFlag=True
                bVar='f2'
                h_BusName='h3'

    if arriveFlag and not(destVpFlag) and not(sourceVpFlag):                
        vp=FeatStruct(
            arrive=FeatStruct(a=a,f=f,t=FeatStruct(t_var=t,time_var=time))
            )
    elif departFlag and departVpFlag:
        vp=FeatStruct(
            depart=FeatStruct(d='d3',f='f1',t=FeatStruct(t_var=t,time_var=time)),
            source=FeatStruct(bus='h3',sourceName=FeatStruct(f=Variable('?h'),name=nameDepart))
        )
    else:
        vp=FeatStruct(
            depart=FeatStruct(d='d3',f='f1',t=FeatStruct(t_var=t,time_var=time)),
            source=FeatStruct(bus='h4',sourceName=FeatStruct(f=Variable('?h'),name=nameDepart)),
            arrive=FeatStruct(a='a3',f='f2',t=FeatStruct(t_var=t,time_var=time)),
            dest=FeatStruct(destName=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h6',name=nameArrive)))
        )

    if destNpFlag and not(busNameNpFlag):
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h='h3',name=nameArrive))))
    else:
        np=FeatStruct(the=FeatStruct(bus=bVar,busname=FeatStruct(h=h_BusName,name=busName)))
        
    wh=FeatStruct(whType=FeatStruct(f=f,type=typeWh))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    result=featStruct(gap,sem,var,arriveFlag=arriveFlag,destVpFlag=destVpFlag,sourceVpFlag=sourceVpFlag,busNameNpFlag=busNameNpFlag,destNpFlag=destNpFlag,departFlag=departFlag,departVpFlag=departVpFlag)
    print(result)    
    # draw_trees(result)
    return result     
            
def featStruct(gapUp,semUp,varUp,arriveFlag=False,destVpFlag=False,sourceVpFlag=False,busNameNpFlag=False,destNpFlag=False,departFlag=False,departVpFlag=False):
    gap=Variable('?gap')


    if arriveFlag and not(destVpFlag) and not(sourceVpFlag):                
        vp=FeatStruct(
            arrive=FeatStruct(a=Variable('?a'),f=Variable('?f'),t=FeatStruct(t_var=Variable('?t'),time_var=Variable('?time')))
        )
    elif departFlag and departVpFlag:
        vp=FeatStruct(
            depart=FeatStruct(d=Variable('?d'),f=Variable('?fDep'),t=FeatStruct(t_var=Variable('?t_var_dep'),time_var=Variable('?timeDepart'))),
            source=FeatStruct(bus=Variable('?h'),sourceName=FeatStruct(f=Variable('?h'),name=Variable('?nameSource')))
        )
    else:
        vp=FeatStruct(
            depart=FeatStruct(d=Variable('?d'),f=Variable('?fDep'),t=FeatStruct(t_var=Variable('?t_var_dep'),time_var=Variable('?timeDepart'))),
            source=FeatStruct(bus=Variable('?h'),sourceName=FeatStruct(f=Variable('?h'),name=Variable('?nameSource'))),
            arrive=FeatStruct(a=Variable('?a'),f=Variable('?fArr'),t=FeatStruct(t_var=Variable('?t_var_arr'),time_var=Variable('?timeArrive'))),
            dest=FeatStruct(destName=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?hDest'),name=Variable('?nameDest'))))
        )

    if destNpFlag and not(busNameNpFlag):
        np=FeatStruct(dest=FeatStruct(bus=Variable('?f'),dest=FeatStruct(f=Variable('?f'),name=FeatStruct(h=Variable('?h'),name=Variable('?name')))))
    else:
        np=FeatStruct(the=FeatStruct(bus=Variable('?b'),busname=FeatStruct(h=Variable('?h_BusName'),name=Variable('?busName'))))

    wh=FeatStruct(whType=FeatStruct(f=Variable('?f'),type=Variable('?type')))
    sem=FeatStruct(query=FeatStruct(vp=vp,np=np,wh=wh))
    var=Variable('?a')

    para = FeatStruct(
        gap=gap,
        sem=sem,
        var=var
    )
    paraUpdate=FeatStruct(
        gap=gapUp,
        sem=semUp,
        var=varUp
    )    

    """
    FeatDict
        1. gap
        2. sem
        3. var
    """

    return paraUpdate.unify(para)



def convert_featstructures_to_procedure(logical_tree):
    """
    Parse logical tree to procedure semantics
    ----------------------------------------------------------
    Args:
        logical_tree: nltk.tree.Tree created from nltk.parser.parser_one()
    """
    logical_expression = logical_tree['sem']['query']
    f = '?f'
    arrival_location = '?sa'
    arrival_time = '?ta'
    departure_location = '?sd'
    departure_time = '?td'
    runtime='?r'
    busname=''
    verb_expression, bus_expression, wh_expression = logical_expression['vp'],logical_expression['np'],logical_expression['wh']#np - vp - wh (structure)
    gap = '?' + logical_tree['gap']#gap ở đây là r2
    cityDict={'Huế':'HUE','Đà_Nẵng':'DANANG','Hồ_Chí_Minh':'HCMC','Đà_nẵng':'DANANG',"Hà_Nội":"HN"}
    #---------Check bus Expression------------#

    try:
        np_variables = bus_expression['dest']['bus']
    except:
        np_variables = bus_expression['the']['bus']
    
    np_preds = [key for key in bus_expression]#['dest']
     #Get bus variable (f1 or f2 or ...)
    if 'f' in np_variables:
        f = '?'+ np_variables 
    #-------------Check Verb expression-------------#
    verb_pred_list = [key for key in verb_expression]#['arrive'] vd: "arrive" - "depart"

    try:
        if 'dest' in np_preds:
            #DEST(f (NAME(a,B)))
            if bus_expression!='':
                try:
                    arrival_location = cityDict[bus_expression['dest']['dest']['name']['name']]#Ví dụ đến HN
                except:
                    arrival_location = cityDict[bus_expression['the']['busname']['name']]
            else:
                arrival_location = ''
                
        elif  'dest' in verb_pred_list:#['depart', 'source', 'arrive', 'dest']
            #DEST(f (NAME(a,B)))
            if verb_expression['dest']['destName']['f']!='':
                arrival_location = cityDict[verb_expression['dest']['destName']['name']['name']]#Huế

        try:
            busname=bus_expression['the']['busname']['name']#B1
            if gap=='?r2':
                runtime=gap
        except:
            busname=np_preds['dest']['dest']['name']['name']
            if gap=='?r2':
                runtime=gap
     

        if 'source' in verb_pred_list:#['depart', 'source', 'arrive', 'dest']
            #SOURCE(f, NAME(a,B))
            if verb_expression['source']['bus']!='':
                departure_location = cityDict[verb_expression['source']['sourceName']['name']]#'HCMC'
    except:
        if 'dest' in verb_pred_list:
            #DEST(f (NAME(a,B)))
            arrival_location = cityDict[verb_expression['dest']['destName']['name']['name']]
        else:
            pass
           
            
    #In case of this assignment, this condition will be always TRUE
    #because time must be specified or be asked in all questions
    try:         
            #ARRIVE or DEPART?
            
        if 'arrive' in verb_pred_list:#['depart', 'source', 'arrive', 'dest']
            #ARRIVE1(v,f,t)
            time=verb_expression['arrive']['t']['time_var']#Time -> gap
            arrival_time = time if time not in gap else gap
        elif 'depart' in verb_pred_list:
            #DEPART1(v,f,t)
            time=verb_expression['depart']['t']['time_var']
            departure_time = time if time not in gap else gap
        else:
            #RUN-TIME
            pass
    except:
        pass
    
    #'(BUS ?f2)'
    #'(ATIME ?f2 HUE ?time)'
    #'(DTIME ?f2 HCMC ?td)'
    #'(RUNTIME ?f2 B1 HCMC HUE)'
    #'(PRINT-ALL ?r2(BUS ?f2)(ATIME ?f2 HUE ?time)(DTIME ?f2 HCMC ?td)(RUNTIME ?f2 B1 HCMC HUE))'
    #--------Fill with parsed values-----------------#
    bus = "(BUS {})".format(f)
    arrival = "(ATIME {} {} {})".format(f, arrival_location, arrival_time)
    departure = "(DTIME {} {} {})".format(f, departure_location, departure_time)
    runtimeprint = "(RUNTIME {} {} {} {})".format(f,busname, departure_location, arrival_location)
    proceduce = "(PRINT-ALL {}{}{}{}{})".format(gap, bus, arrival, departure,runtimeprint)
    
    return {'query': gap,
            'bus': f,
            'arrival_location': arrival_location,
            'arrival_time': arrival_time,
            'departure_location': departure_location,
            'departure_time': departure_time,
            'str': proceduce,
            'busname':busname,
            'runtime':runtime}
    
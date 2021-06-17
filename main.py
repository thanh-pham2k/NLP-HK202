
from model import *
from util import *

def main(args):
    print(args.question_file)
    print(args.question_file.split("/"))
    question_file = args.question_file.split("/")
    a2fLst = ['a','b','c','d','e','f']
    question = read_file(args.question_file)
    lst_output = ['output/question_'+question_file[1][-5] +"/output_"+a2fLst[i] for i in range(0,len(a2fLst))]
    #Get parse tree English
    print("-------------Loading grammar---------------------")
    nlp_grammar = parse.load_parser(args.grammar, trace = 0)
    print("Grammar loaded at {}".format(args.grammar))
    write_file(lst_output[0], str(nlp_grammar.grammar()))
    
    print("-------------Parsed structure-------------")
    print(question) #Xe bus nào đến thành phố Hà Nội ?
    question = question.replace('?','').replace(':','').replace('.','')#remove (?, :, .)
    tree,token_def,doc=spacy_viet(question,"off")#Thu được  quan hệ ngữ nghĩa
    write_file(lst_output[1], token_def)
    write_file(lst_output[2],str(tree))
    # #Parse to logical form
    # print("-------------Parsed logical form-------------")
    # print(str(doc))
    featStructCfg = parserGSVfeature(doc)

    # #Parse to logical form
    # print(featStructCfg )
    logical_form = featStructCfg['sem']
    # draw_trees(logical_form)# Có thể xem logical_form ở dạng UI
    write_file(lst_output[3],str(logical_form ))

    # print("-------------PROCEDURE SEMANTICS-------------")
    
    procedure_semantics = convert_featstructures_to_procedure(featStructCfg)

    # print(procedure_semantics['str'])
    write_file(lst_output[4],procedure_semantics['str'])

    print("-------------Retrieved result-------------")
    results = retrieve_result(procedure_semantics)
    final_result = []
    if len(results) == 0:
        print("No result found!")
    else:
        for result in results:
            if( len(result)>3):
                temp = result
                final_result.append(temp[:-4] + ':' + temp[-4:])
                print(final_result)
        print('')
        if final_result==[]:#handle for time
            write_file(lst_output[5], " ".join(results))
        else:#handle for bus
            write_file(lst_output[5], " ".join(final_result))



parser = argparse.ArgumentParser(description="NLP ASSIGNMENT CMD")

parser.add_argument(
  '--question_file',
    default = "input/question_5.txt",
      help= "Example: python main.py --question_file=input/question_1.txt"
)
    

parser.add_argument(
  '--grammar',
  default= "grammar.fcfg",
        help= "python main.py --question=your_question_file_name --grammar=your_grammar_file_name"
  )

args = parser.parse_args()

main(args) 


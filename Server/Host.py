class Host:
    def __init__(self):
        self.request_list = []
        self.student_list = []
        self.lecturer_list = []
        self.course_dict = {
            'CE320: Large Scale Software Programming': ['Agile Software Development', 'Extreme Programming',
                                                        'Planning in XP', 'Developing in XP', 'Clean Code',
                                                        'Releasing in XP'],
            'CE305: Languages and Compiler': ['ANTLR', 'Lexical Analysis', 'Finite Automata', 'Grammars and Parsing',
                                              'Semantics','Parsers'],
            'CE314: Natural Language Engineering': ['N Gram Models', 'LMs Evolution and Evaluation',
                                                    'Development of Language Modelling', 'POS Tagging',
                                                    'Word Sense and Word Representations',
                                                    'Text Classfication and Naive Bayes Model']
        }

    def add_request(self, request):
        # Add the provided Request instance to the request_list
        self.request_list.append(request)

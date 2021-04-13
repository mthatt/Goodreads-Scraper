class QueryInterpreter:
    def __init__(self, query):
        self.query = str(query)
        self.elements = {'book_or_author': None,
                    'field': None,
                    'second_field': None,
                    'search_term': None,
                    'exact_search_term': None,
                    'second_search_term': None,
                    'second_exact_search_term': None,
                    'operator': None}
        if "." in query:
            self.elements['book_or_author'] = query.split('.')[0]

        if ":" in query:
            cutString = query.split('.')[1]
            self.elements['field'] = cutString.split(':')[0]

        if "AND" in query:
            self.elements['operator'] = "AND"
            cutString = query.split(':', 1)[1]
            cutStringArray = cutString.split("AND")
            if "\"" in cutStringArray[0]:
                self.elements['exact_search_term'] = cutStringArray[0].split('\"')[1]
            elif '\"' not in cutStringArray[0]:
                self.elements['search_term'] = cutStringArray[0]
            if "\"" in cutStringArray[1]:
                self.elements['second_exact_search_term'] = cutStringArray[1].split('\"')[1]
                cutString2 = cutStringArray[1].split(".")[1]
                self.elements['second_field'] = cutString2.split(":")[0]
            elif '\"' not in cutStringArray[1]:
                cutString2 = cutStringArray[1].split(".")[1]
                self.elements['second_search_term'] = cutString2.split(":")[1]
                self.elements['second_field'] = cutString2.split(":")[0]

        elif "OR" in query:
            self.elements['operator'] = "OR"
            cutString = query.split(':', 1)[1]
            cutStringArray = cutString.split("OR")
            if "\"" in cutStringArray[0]:
                self.elements['exact_search_term'] = cutStringArray[0].split('\"')[1]
            elif '\"' not in cutStringArray[0]:
                self.elements['search_term'] = cutStringArray[0]
            if "\"" in cutStringArray[1]:
                self.elements['second_exact_search_term'] = cutStringArray[1].split('\"')[1]
                cutString2 = cutStringArray[1].split(".")[1]
                self.elements['second_field'] = cutString2.split(":")[0]
            elif '\"' not in cutStringArray[1]:
                cutString2 = cutStringArray[1].split(".")[1]
                self.elements['second_search_term'] = cutString2.split(":")[1]
                self.elements['second_field'] = cutString2.split(":")[0]

        elif "NOT" in query:
            self.elements['operator'] = "NOT"
            cutString = query.split(':')[1]
            cutStringArray = cutString.split("NOT")
            if "\"" in cutStringArray[1]:
                self.elements['exact_search_term'] = cutStringArray[1].split('\"')[1]
            elif '\"' not in cutStringArray[1]:
                self.elements['search_term'] = cutStringArray[1]

        elif ">" in query:
            self.elements['operator'] = ">"
            cutString = query.split(':')[1]
            cutStringArray = cutString.split(">")
            if "\"" in cutStringArray[1]:
                self.elements['second_exact_search_term'] = cutStringArray[1].split('\"')[1]
            elif '\"' not in cutStringArray[1]:
                self.elements['second_search_term'] = cutStringArray[1]

        elif "<" in query:
            self.elements['operator'] = "<"
            cutString = query.split(':')[1]
            cutStringArray = cutString.split("<")
            if "\"" in cutStringArray[1]:
                self.elements['second_exact_search_term'] = cutStringArray[1].split('\"')[1]
            elif '\"' not in cutStringArray[1]:
                self.elements['second_search_term'] = cutStringArray[1]

        else:
            if "\"" in query:
                cutString1 = query.split('.', 1)[1]
                cutString2 = cutString1.split(':', 1)[1]
                self.elements['exact_search_term'] = cutString2.split('\"',)[1]

            if not "\"" in query:
                cutString = query.split(':')[1]
                self.elements['search_term'] = cutString
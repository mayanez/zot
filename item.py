import os

def format_author(author):
    return '%s, %s' % author


class Item:
    def __init__(self, item_dict={}):
        self.__dict__ = item_dict
        
    def __repr__(self):
        return repr(self.__dict__)
        
    def match(self, **kwargs):
        if not 'keywords' in kwargs: kwargs['keywords'] = []
        fields_to_search = {'title': 'title',
                            'pub': 'publicationTitle',
                            'author': 'author_str',
                            'year': 'year',
                            'collection': 'collections',
                            }
        result = []
        match_score = 0
        for field, to_search in fields_to_search.items():
            if not hasattr(self, to_search): continue
            search_terms = kwargs['keywords']
            if field in kwargs: search_terms += kwargs[field]
            
            text_to_search = getattr(self, to_search).lower()
            search_terms = [term.lower() for term in search_terms]
            for search_term in search_terms:
                match_score += text_to_search.count(search_term)
        
        return match_score
        
        
    def author_string(self):
        if not hasattr(self, 'authors'): return ''
        authors = getattr(self, 'authors')
        if len(authors) == 1: return format_author(authors[0])
        elif len(authors) == 2: return ' and '.join([format_author(a) for a in authors])
        else:
            return ', '.join([format_author(authors[n]) if n < len(authors)-1 else 'and %s' % format_author(authors[n]) for n in range(len(authors))])
            
    author_str = property(author_string)
        
        
    def bibliography(self):
        bib = self.author_string()
        if hasattr(self, 'year'): bib += ' %s.' % self.year
        if hasattr(self, 'title'): bib += ' %s.' % self.title
        if hasattr(self, 'publicationTitle'): bib += ' %s.' % self.publicationTitle

        v = []
        if hasattr(self, 'volume'): v += ['Vol. %s' % self.volume]
        if hasattr(self, 'issue'): v += ['Issue %s' % self.issue]
        if hasattr(self, 'pages'): v += ['Pages %s' % self.pages]       
        if v: bib += ' ' + (', '.join(v)) + '.'
        
        if hasattr(self, 'doi'): bib += ' doi:%s' % self.doi
        
        return bib
        
        
    def citation(self):
        citation = ''
        if hasattr(self, 'authors'): 
            citation = (self.authors[0][0])
            if len(self.authors) > 1: citation += ' et al.'
        else: citation = self.title
        if hasattr(self, 'year'): citation += ' %s.' % self.year
        
        return citation
        
        
    def full_text(self, storage_dir):
        if hasattr(self, 'attachments'):
            for attachment in self.attachments:
                # TODO: read text from pdf
                return attachment.replace('storage:', os.path.join(storage_dir, self.key + '/'))
                pass
        else: 
            return "No PDF attachments."

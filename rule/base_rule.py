import re
import soupsieve as sv


class ReRule:
    def __init__(self, string):
        self.string = re.compile(string)
    
    # None / result
    def _find(self, text):
        return self.string.search(text)
   
    # 非list,是iter
    def _findall(self, text):
        return self.string.finditer(text)
        
    def find_raw(self, text, soup, with_string=False):
        result = self._find(text)
        if result is None:
            return None
        return result.group()
        
    # re这里attr不具有实际字面意思，仅仅是为了统一
    def find_attr(self, text, soup, with_string=False):
        result = self._find(text)
        if result is None:
            return None
        return result.group(1)
        
    def findall_raw(self, text, soup, with_string=False):
        results = self._findall(text)
        return [result.group() for result in results]
     
    # 同上
    def findall_attr(self, text, soup, with_string=False):
        results = self._findall(text)
        return [result.group(1) for result in results]

                
class TagRule:
    # None / result
    def _find(self, soup):
        return None
     
    # [] / [result0, …]
    def _findall(self, soup):
        return []
        
    def find_raw(self, text, soup, with_string=False):
        result = self._find(soup)
        if result is None:
            return None
        if not with_string:
            return result
        if self.string_pattern is None:
            return result.string
        return result[self.string_pattern]
        
    def find_attr(self, text, soup, with_string=False):
        result = self._find(soup)
        if result is None:
            return None
        if not with_string:
            return result[self.attr]
        if self.string_pattern is None:
            return result[self.attr], result.string
        return result[self.attr], result[self.string_pattern]
        
    def findall_raw(self, text, soup, with_string=False):
        results = self._findall(soup)
        if not with_string:
            return results
        if self.string_pattern is None:
            return [result.string for result in results]
        return [result[self.string_pattern] for result in results]
            
    def findall_attr(self, text, soup, with_string=False):
        results = self._findall(soup)
        if not with_string:
            return [result[self.attr] for result in results]
        if self.string_pattern is None:
            return [(result[self.attr], result.string) for result in results]
        return [(result[self.attr], result[self.string_pattern]) for result in results]
        
    
class BsRule(TagRule):
    def __init__(self, name, attrs, string, attr, string_pattern):
        self.name = name
        self.attrs = attrs
        if string is not None:
            self.string = re.compile(string)
        else:
            self.string = None
        self.attr = attr
        self.string_pattern = string_pattern
        
    # None / result
    def _find(self, soup):
        return soup.find(name=self.name, attrs=self.attrs, string=self.string)
     
    # [] / [result0, …]
    def _findall(self, soup):
        return soup.find_all(name=self.name, attrs=self.attrs, string=self.string)

                                
class CssSelectorRule(TagRule):
    def __init__(self, css_selector, attr, string_pattern):
        self.css_selector = sv.compile(css_selector)
        self.attr = attr
        self.string_pattern = string_pattern
    
    # None / result
    def _find(self, soup):
        return self.css_selector.select_one(soup)
   
    # list
    def _findall(self, soup):
        return self.css_selector.select(soup)

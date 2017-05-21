from .__init__ import Duedil

_company_status_lookup = {
    "L": "Live",
    "D": "Dissolved",
    "R": "Removed",
    "!": "Deleted",
    "X": "Converted / Closed"
}

_company_type_lookup = {
    "0": "Other",
    "1": "Private unlimited with share capital",
    "2": "Private limited with share capital",
    "3": "Public limited with share capital",
    "4": "Old public limited company",
    "5": "Private limited by guarantee without share capital, exempt from using 'Limited'",
    "6": "Limited Partnership",
    "7": "Private limited by guarantee without share capital",
    "8": "Company converted / closed",
    "9": "Unlimited / No share capital",
    "A": "Limited"
}

_liquidation_status_lookup = {
    "L": "In liquidation",
    "R": "In receivership",
    "S": "Strike off listed",
    "O": "Struck off"
}

class Companies(Duedil):
    """
    Extend Duedil for companies.
    """
    def __init__(self, key=None):
         Duedil.__init__(self, key)
         self._url += "search/companies.json?"

    def search(self, query):
        query = self.__quote__(query)
        response = self.__get__("query=%s" % (query))["data"]
        for item in response:
            yield Company(item['id'], key=self._key)

class Company(Duedil):
    """
    Extend Duedil for a company.
    """
    def __init__(self, id, key=None):
        Duedil.__init__(self, key)
        self._id = id
        self._url += "company/%s.json?" % (self._id)
        get = self.__get__("fields=get_all")
        for key in get.keys():
            if key == "status":
                self.__setattr__(key, _company_status_lookup[get[key]])
            elif key == "companyType":
                self.__setattr__(key, _company_type_lookup[get[key]])
            else:
                self.__setattr__(key, get[key])

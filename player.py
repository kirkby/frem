import re

BK_FREM_MAIN_URL = 'http://www.bkfrem.dk/default.asp?id=19'

class Player:
    html_table_properties = ['', 'Sponsor', 'Position', 'Height', 'Weight', 'Born', 'Games', 
'Wins', 'Ties', 'Losses', 'Goals', 'Debute', 'Career', 'Description']

    def __init__(self, url):
        self.url = url
        self.id = self.__get_id_from_url(url)
        self.name = ''
        self.nbr = ''
        self.props = {}

    def __get_id_from_url(self, url):
        #regex = re.compile('.+bkfrem-(\d+)\.html').search(url)
        match = re.compile('.+bkfrem-(\d+)\.html').search(url)
        if match:
            return match.group(1)
        else:
            return '-1'

    def print_props():
        for key, value in self.props.items():
            print (key + ':' + value)

    def set_name_nbr(self, html):
        # find name and number in H1
        name = html.find('h1', first=True).text
        regex = re.compile('\d+\.')
        match = regex.match(name)
        if match:
            end = match.end()
            self.nbr = name[0:end-1].strip()
            self.name = name[end:].strip()
        else:
            nbr = 'N/A'

        return

    def set_properties(self, html):
        props = {}
        for i in range(1,len(self.html_table_properties)):
            selector = 'table > tr:nth-child(' + str(i) + ') > td:nth-child(2)'
            data = html.find(selector, first=True)
            try:
                props[self.html_table_properties[i]] = data.text
            except AttributeError:
                props[self.html_table_properties[i]] = 'Parse error: No value found.'
                print('ERR! ' + self.name + ' no value for ' + self.html_table_properties[i] + ' found.')
        
        # special case: games and games this season in one string, ex "70 (10)"
        regex = re.compile('(\d+).+\((\d+)\)')
        match = regex.search(props['Games'])
        if match:
            props['Games'] = match.group(1)
            props['Games-this-season'] = match.group(2)

        # special case: goals and goals this season in one string, ex "25 (10)"
        match = regex.search(props['Goals'])
        if match:
            props['Goals'] = match.group(1)
            props['Goals-this-season'] = match.group(2)

        self.props = props
        return

    @property
    def goals(self):
        return self.get_property('Goals')

    @property
    def birthday(self):
        return self.get_property('Born')

    @property
    def weight(self):
        return self.get_property('Weight')

    @property
    def height(self):
        return self.get_property('Height')

    @property
    def born_in_hvidovre(self):
        return self.get_property('Height')

    def get_property(self, value):
        #try:
        #    idx = self.html_table_properties.index(value)
        #except ValueError:
        #    return 'Undefined value: ' + value
        if value in self.props:
            return self.props[value]
        else:
            return 'N/A'
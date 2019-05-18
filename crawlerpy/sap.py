class Article:
    """
        Representation of an article
        an identifiant
        the publish date of the article
        the categorie of the article
        list of section
    """

    def __init__(self, id, publish_date=None, categorie=None):
        self.id = id
        self.publish_date = publish_date
        self.categorie = categorie
        self.sections = []

    def add_section(self, section):
        """add a section in the article"""
        self.sections.append(section)


class Section:
    """represent a part of an article
        identifiant:the name of part
        contains list of data
    """

    def __init__(self, id):
        self.id = id
        self.contents = []

    def add_content(self, data):
        """add a content to the Section"""
        self.contents.append(data)


class Data:
    """Represent a data
        type-> the type of data
        value-> the value"""

    def __init__(self, type_, value):
        self.type = type_
        self.value = value
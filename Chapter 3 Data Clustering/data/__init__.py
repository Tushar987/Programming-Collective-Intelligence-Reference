from feedparser import parse
from re import compile


class Dataset(object):
    """
    Class responsible for generating the word counts and words list used to make the blogdata.txt
    """
    def __init__(self):
        self.__parser = None
        self.__word_count = dict()
        self.__words = list()

    def __get_words(self, html):
        """
        Splits the html and splits the word by non alphabetical characters
        :param html:
        """
        text = compile(r'<[^>]+>').sub('', html)
        words = compile(r'[^A-Z^a-z]+').split(text)
        self.__words = [word.lower() for word in words if word != '']

    def __get_word_counts(self):
        """
        Extracts all words from the feed and makes a word count
        """
        for entry in self.__parser.entries:
            summary = entry.summary if 'summary' in entry else entry.description
            self.__get_words(entry.title + ' ' + summary)
            for word in self.__words:
                self.__word_count.setdefault(word, 0)
                self.__word_count[word] += 1

    def set_parser(self, url):
        self.__parser = parse(url)

    def get_title(self):
        return self.__parser.feed.title

    def get_word_count(self):
        return self.__word_count

    def get_words(self):
        return self.__words


class Generator(object):
    """
    Class responsible for generating the dataset by parsing the feedlist.txt
    """
    def __init__(self, file_name):
        self.__data = None
        self.__dataset_object = Dataset()
        self.__appeared_count = dict()
        self.__word_counts = dict()
        self.__word_list = list()
        self.__feed_list = [line for line in file(file_name)]

    def parse(self):
        """
        Generates the dataset for each blog in given file
        """
        for feed_url in self.__feed_list:
            try:
                self.__dataset_object.set_parser(feed_url)
                title, wc = self.__dataset_object.get_title(), self.__dataset_object.get_word_count()
                self.__word_counts[title] = wc
                for word, count in wc.items():
                    self.__appeared_count.setdefault(word, 0)
                    if count > 1:
                        self.__appeared_count[word] += 1
            except:
                print("Failed to parse feed %s" % feed_url)

    def filter(self):
        """
        Responsible for filtering out very common words like articles, conjunction etc.
        Also filters out words that are used very less
        """
        for w, bc in self.__appeared_count.items():
            fraction = float(bc) / len(self.__feed_list)
            if 0.1 < fraction < 0.5:
                self.__word_list.append(w)

    def write(self):
        self.__data = file('blogdata.txt', 'w')
        self.__data.write('Blog')
        for word in self.__word_list:
            self.__data.write('\t%s' % word)
        self.__data.write('\n')
        for blog, wc in self.__word_counts.items():
            self.__data.write(blog)
            for word in self.__word_list:
                self.__data.write('\t' + str(wc[word]) if word in wc else '\t0')
            self.__data.write('\n')

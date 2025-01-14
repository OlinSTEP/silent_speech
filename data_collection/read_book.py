import os
import random
import nltk

class Book(object):
    def __init__(self, book_file, book_name):
        self.file = book_name

        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

        with open(book_file) as f:
            all_text = f.read()
        paragraphs = all_text.split('\n\n')
        sentences = [s for p in paragraphs for s in sent_detector.tokenize(p.strip())]
        self.sentences = [s.replace('\n', ' ') for s in sentences]

        bookmark_file = self.file + '.bookmark'
        if os.path.exists(bookmark_file):
            with open(bookmark_file) as f:
                self._current_index = int(f.read().strip())
        else:
            self._current_index = 0

        self.idxs = [i for i in range(len(sentences))]
        random.shuffle(self.idxs)
        self.current_index = self.idxs[self._current_index]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        bookmark_file = self.file + '.bookmark'
        with open(bookmark_file, 'w') as f:
            f.write(str(self.current_index))

    def current_sentence(self):
        return self.sentences[self.current_index]

    def next(self):
        self._current_index = (self._current_index+1) % len(self.sentences)
        self.current_index = self.idxs[self._current_index]
        if self._current_index == 0:
            random.shuffle(self.idxs)

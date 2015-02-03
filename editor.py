# conding: utf-8


class Editor:
    # todo: a config file for each language
    # use english for now

    def __init__(self):
        self.dynamic_blacklist = set()
        self.pos_mapping = {'(': '(', ')': ')', ':': ':', 'CD': '3.14'}
        self.pos_blacklist = ['(', ')', ':', '$', 'CD', 'HYPH', '``', '\'\'']
        self.form_blacklist = ['%', '$']

    def add_dyn_form(self, form):
        self.dynamic_blacklist.add(form)

    def reset_dyn_form(self):
        self.dynamic_blacklist = set()

    def check(self, form):
        if form in self.dynamic_blacklist:
            return False
        return True

    def read_mapping(self, map_file):
        pass

    def map(self, pos, form):
        if pos in self.pos_mapping:
            return self.pos_mapping[pos]
        else:
            return form

    def encode_feat(self, form, pos, label):
        if pos in ['IN', 'DT']:
            return '%s_%s_%s' % (form, pos, label)
        else:
            return '%s_%s' % (pos, label)

    def decode_feat(self, feat):
        items = feat.split('_')
        return (items[-2], items[-1])




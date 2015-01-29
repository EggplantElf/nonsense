# conding: utf-8


class Filter:
    def __init__(self, blacklist = []):
        self.blacklist = blacklist
        self.dynamic_blacklist = set()

    def add_dyn_form(self, form):
        self.dynamic_blacklist.add(form)

    def reset_dyn_form(self):
        self.dynamic_blacklist = set()

    def check(self, form):
        if form in self.dynamic_blacklist:
            return False
        return True
class Stack(list):
    def push(self, elem):
        self.append(elem)

    def isEmpty(self):
        return len(self) == 0

    def last(self):
        if self.isEmpty():
            return None
        return self[len(self) - 1]

    def pop(self):
        return super().pop()

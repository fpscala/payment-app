class Payment:
    def __init__(self, id, type, price, debt, month, groupId, comments, studentId, groupName, studentFullName):
        self.id = id
        self.type = type
        self.debt = debt
        self.month = month
        self.price = price
        self.groupId = groupId
        self.studentId = studentId
        self.comments = comments
        self.groupName = groupName
        self.studentFullName = studentFullName

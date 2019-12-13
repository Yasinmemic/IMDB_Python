class Comment ():
    def __init__(self, userName, comment):
        self.userName = userName
        self.comment = comment

    def yazdir(self):
        print("USERNAME: ", self.userName, "COMMENT: ", self.comment)

    def getComment(self):
        return self.comment

    def getUserName(self):
        return self.userName

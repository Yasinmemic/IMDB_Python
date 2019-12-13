class Film ():
    def __init__(self, name, photo, link):
        self.name = name
        self.photo = photo
        self.link = link
        self.id = self.link[9:]

    def yazdir(self):
        print("Name: "+self.name+"\n"+"Photo: " +
              self.photo + "\n"+"Link: "+self.link + "\n"+"id: "+self.id)

    def getName(self):
        return self.name

    def getPhoto(self):
        return self.photo

    def getLink(self):
        return self.link

    def getId(self):
        return self.id

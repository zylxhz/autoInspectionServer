class Report:
    
    def __init__(self, project_team, test_num, pass_num, time, link):
        self.project_team = project_team
        self.test_num = test_num
        self.pass_num = pass_num
        self.time = time
        self.link = link
        
    def setLink(self, link):
        self.link = link
        
    def setTime(self, time):
        self.time = time
        
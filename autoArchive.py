import urllib.request,json,subprocess,time,os,colorama
class Archive():
    def __init__(self,channels,archiveLocations,fileLocation,root):
        self.channels = channels
        if not(os.path.exists(fileLocation)):
            with open(fileLocation,"w+") as File:
                File.write("")
        self.fileLocation = fileLocation
        self.archiveLocations = archiveLocations
        self.root = root
        self.currentIndex = 0
        with open(fileLocation) as fileCount:
            self.latestVideos = fileCount.readlines()
    def download(self,video):
        print(colorama.Fore.LIGHTBLUE_EX+"Downloading " + video,colorama.Style.RESET_ALL)
        try:
            subprocess.check_output(["yt-dlp", "-f", "best", "-ciw", "-o", (self.root + self.archiveLocations[self.currentIndex] + "/%(title)s.%(ext)s"), video],stderr=subprocess.DEVNULL)
            #subprocess.run(["notify-send",(self.author + ' has uploaded a new video!'), self.title]) #uncomment if you want notifications but the invidious latest videos randomizes the top two videos, meaning that you get spammed with notifications
        except subprocess.CalledProcessError:
            print(colorama.Fore.RED+"FAILURE! " + video + " isn't available!",colorama.Style.RESET_ALL,end="")
            return -1
        print(colorama.Fore.LIGHTBLUE_EX+"SUCCESS! Downloaded " + video,colorama.Style.RESET_ALL,end="")
        return 0
    def archive(self):
        os.system("clear")
        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://invidious.namazso.eu/api/v1/channels/latest/'
        for j,x in enumerate(self.channels):
            first_url = base_search_url+x
            video_url = ""
            inp = urllib.request.urlopen(first_url,timeout=15)
            resp = json.load(inp)
            try:
                video_url = base_video_url + resp[0]['videoId']
                self.author = resp[0]['author']
                self.title = resp[0]['title']
                try:
                    self.latestVideos[j].replace('\n','')
                except:
                    cont = 1
                    while cont:
                        with open(self.fileLocation,"a") as File:
                            File.write("\n.")
                        self.latestVideos.append("")
                        cont = 0
                        try:
                            self.latestVideos[j].replace('\n','')
                        except:
                            cont = 1
                if self.latestVideos[j].replace('\n','') != video_url:
                    print(first_url)
                    print(colorama.Fore.RED + '!!!\n' + self.author + ' has uploaded a new video \"' + self.title + "\", URL:", video_url + '\n!!!')
                    print(colorama.Style.RESET_ALL,end="")
                    self.currentIndex = j
                    if(self.download(video_url)==0):
                        self.latestVideos[j] = video_url+'\n'
                        with open(self.fileLocation,"w") as fileCount:
                            fileCount.write("".join(self.latestVideos))
                    print()
                else:
                    print((colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title) if len(colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title) < 82 else (colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title)[:81]+'...')
            except:
                print(colorama.Fore.RED + self.archiveLocations[j] + " has no videos!")
            print(colorama.Style.RESET_ALL,end="")
dictionary = {'<channel id beginning with UC>': '<Download destination in root folder>'}
try:
    archive = Archive([x for x in dictionary], [dictionary[x] for x in dictionary],'<name of autoarchiver data file>','<root folder of all archives>')
    archive.archive()
    print("Completed Full Sweep: Waiting 20SEC")
    time.sleep(20)
except urllib.error.HTTPError:
    pass

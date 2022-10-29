import urllib.request,json,subprocess,time,os,colorama,random
class Archive():
    def __init__(self,channels,archiveLocations,fileLocation,root):
        self.channels = channels
        if not(os.path.exists(fileLocation)):
            with open(fileLocation,"w+") as File:
                File.write("a\n"*len(channels))
        self.fileLocation = fileLocation
        self.archiveLocations = archiveLocations
        self.root = root
        if root[-1] != '/':
            self.root+='/'
        self.currentIndex = 0
        with open(fileLocation) as fileCount:
            self.latestVideos = fileCount.readlines()
    def download(self,video):
        print(colorama.Fore.LIGHTBLUE_EX+"Downloading " + video,colorama.Style.RESET_ALL)
        try:
            subprocess.check_output(["yt-dlp", "-f", "b", "-ciw", "-o", (self.root + self.archiveLocations[self.currentIndex] + "/%(title)s.%(ext)s"), video],stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e)
            print(colorama.Fore.RED+"FAILURE! " + video + " isn't available!",colorama.Style.RESET_ALL,end="")
            return -1
        print(colorama.Fore.LIGHTBLUE_EX+"SUCCESS! Downloaded " + video,colorama.Style.RESET_ALL,end="")
        return 0
    def archive(self):
        os.system("clear")
        apijson = urllib.request.urlopen("https://api.invidious.io/instances.json?pretty=1&sort_by=api")
        apijson = json.load(apijson)
        self.api = apijson
        base_video_url = 'https://www.youtube.com/watch?v='
        for j,x in enumerate(self.channels):
            self.currentIndex = j
            s = 0
            c = 0
            while not(s):
                if(c>8):
                    break
                rans = random.randint(1,5)
                base_search_url = 'https://' + self.api[rans][0] + '/api/v1/channels/latest/'
                first_url = base_search_url+x
                s = 1
                try:
                    inp = urllib.request.urlopen(first_url)
                    resp = json.load(inp)
                    resp[0]['author']
                except Exception as e:
                    c+=1
                    s = 0
            if(c>8):
                print(colorama.Fore.RED+"Couldn't access " + self.archiveLocations[self.currentIndex] + "'s video list" + colorama.Style.RESET_ALL)
                continue
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
                if(self.download(video_url)==0):
                    self.latestVideos[j] = video_url+'\n'
                    with open(self.fileLocation,"w") as fileCount:
                        fileCount.write("".join(self.latestVideos))
                print()
            else:
                print((colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title) if len(colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title) < 82 else (colorama.Fore.GREEN+self.author + '\'s videos are up to date! With the latest being ' + self.title)[:81]+'...')
            print(colorama.Style.RESET_ALL,end="")
dictionary = {'<channel id beginning with UC>': '<Download destination in root folder>'}
archive = Archive([x for x in dictionary], [dictionary[x] for x in dictionary],'<name of autoarchiver data file>','<root folder of all archives>')
archive.archive()
sleeptime = 10
print("Sweep completed, sleeping", sleeptime, "seconds")
time.sleep(sleeptime)

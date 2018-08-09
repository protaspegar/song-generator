import logging
import urllib.request
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.log = logging.getLogger(__name__)

        self.artistName = 'los-hermanos'
        self.baseURL = 'https://www.letras.mus.br'
        self.artistURL = '/los-hermanos/'

        self.lyricsList = None


    def Start(self):
        self.log.info('Starting scraper...')

        songList = self.ProcessArtistPage()
        self.lyricsList = self.ProcessSongList(songList)

        self.log.info('Scraper finished!')


    def ProcessArtistPage(self):
        self.log.info('Loading Artist page...')
        response = urllib.request.urlopen(self.baseURL + self.artistURL)
        html = response.read()
        #self.log.info(html)
        parsedPage = BeautifulSoup(html, 'html.parser')
        self.log.info('Loaded: '+parsedPage.title.string)

        songList = self.GetListOfSongs(parsedPage)
        return songList


    def GetListOfSongs(self, parsedArtistPage):
        container = parsedArtistPage.find("div", id="cnt-artist-songlist")
        if (container is None):
            self.log.error('Song list container was not found!')
            return

        innerContainer = container.find("ul", class_="cnt-list")
        if (innerContainer is None):
            self.log.error('Inner container was not found!')
            return

        songList = innerContainer.find_all("a")
        return songList
        


    def ProcessSongList(self, songList):
        self.log.info(str(len(songList)) + ' songs found')
        lyricsList = []
        for song in songList:
            #self.log.info(song.string + ": "+song['href'])
            songURL = song['href']
            response = urllib.request.urlopen(self.baseURL + songURL)
            html = response.read()
            parsedPage = BeautifulSoup(html, 'html.parser')
            self.log.info('Loaded: '+parsedPage.title.string)
            lyrics = self.GetLyrics(parsedPage)
            lyricsList.append(lyrics)
            #return lyricsList#TODO: remove this return. This return is just to limit to 1 song because we're just testing
        return lyricsList

    def GetLyrics(self, parsedSongPage):
        container = parsedSongPage.find("div", class_="cnt-letra")
        if (container is None):
            self.log.error('Lyric container was not found!')
            return

        lyrics = []
        stropheList = container.find_all("p")
        for strophe in stropheList:
            for verse in strophe.stripped_strings:
                lyrics.append(verse + "\n")
            lyrics.append("\n")

        return lyrics
            
    def SaveToFile(self):
        path = 'Output/'+self.artistName+'.txt'
        outputFile = open(path,'w+') # create if not exists
        for lyric in self.lyricsList:
            for verse in lyric:
                outputFile.write(verse)
            #outputFile.write('\n')
        outputFile.close()


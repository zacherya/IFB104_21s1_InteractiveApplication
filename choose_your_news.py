# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item for QUT's teaching unit
#  IFB104, "Building IT Systems", Semester 1, 2021.  By submitting
#  this code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
student_number = 1077263  # put your student number here as an integer
student_name = "Zachery Adams"  # put your name here as a character string
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
# --------------------------------------------------------------------#


# -----Assignment Description-----------------------------------------#
#
#  Choose Your News
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a useful application that allows the user to compare news stories
#  from multiple sources and save them for later perusal.
#
#  See the client's requirements accompanying this file for full
#  details.
#
# --------------------------------------------------------------------#


# -----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function below.)
from urllib.request import urlopen
from urllib.parse import urlparse
import html
import webbrowser

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: DON'T import all of the "tkinter.tkk" functions
# using a "*" wildcard because this module includes alternative
# versions of standard widgets like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from tkinter.ttk import LabelFrame
from tkinter import messagebox

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()


#
# --------------------------------------------------------------------#


# -----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#

# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we do NOT encourage using
#      this option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(url='http://www.wikipedia.org/',
             target_filename='downloaded_document',
             filename_extension='html',
             save_file=True,
             char_set='UTF-8',
             incognito=False):
    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a Windows 10 computer instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                               'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                               'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError as e:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        print(e.code)
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding=char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents


#
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Create Custom Tkinter Button Object to allow Full control tkinter radio buttons
# we can create bindings and create hover/down/select events to change appearence
# the radiobutton
class SwitchControl(Radiobutton):
    def __init__(self, master, vari, command, parent, **kwargs):
        # Make the class object a decendant of Tk.Radiobutton
        Radiobutton.__init__(self, master, **{**kwargs, 'variable': vari, 'indicatoron': 0, 'command': command,
                                              'background': secondary_bg_color, 'padx': 0, 'pady': 0, 'borderwidth': 0,
                                              'highlightthickness': 0, 'cursor': 'hand2'})

        # if switch control needs to be text buttons then width must be specified but all components are custom
        # state images
        # self.configure(width=20)

        # Define the binding names, states for each menu object
        # we create unqiue binding ids formulated off the event state, customised from the value of the button
        # Binded buttons have a non primitive state (Anything but default)
        self.__bound = False
        self.__binding_names = ['<Enter>', '<Leave>', '<1>']
        self.__binding_states = ['hover' + self["value"], 'up' + self["value"], 'down' + self["value"]]
        self.__binding_ids = [None] * 3

        # Make master of radiobutton and parent object available in code
        self.__master = master
        self.__parent = parent

        # Set variable of radio button and adjust when changed, this represents state of button aka value
        self.__switch_state_value = vari
        self.__switch_state_value.trace('w', self.__adjust)

        # Adjust the non binded buttons
        self.__adjust()

    # Bind all the buttons events, lambda is used again so state doesn't change on program initalise
    def __bindings(self):
        for bind_id_key, (name, state) in enumerate(zip(self.__binding_names, self.__binding_states)):
            # Track binding ids -- image can be changed to text by switch the values in confiure()
            self.__binding_ids[bind_id_key] = self.bind(name, lambda e, s=state: self.configure(image=s))
        # Make this object bound as it's selected
        self.__bound = True

    # unbind all events
    def __unbindings(self):
        # Reset function for all unslected buttons to return to their default state
        # Hover -> Default
        # Selected -> Default
        if self.__bound:
            for name, id in zip(self.__binding_names, self.__binding_ids):
                self.unbind(name, id)
            self.__bound = False

    def __adjust(self, *args):
        # When value of buttons change check if button value is the one selected and set it to be SELECTED
        # else set it to it "default" state
        if self.__switch_state_value.get() == self['value']:
            # if text buttons change image to text
            self['image'] = 'sel' + self['value']
            if self.__bound:
                # object needs to be unbound so it hits its selected visual state ( last in array) (Down)
                self.__unbindings()
        else:
            if not self.__bound:
                # if text buttons change image to text
                self['image'] = 'up' + self['value']
                # re check bindings and confirm state in global BIND
                self.__bindings()


# Set the window controller, main tkinter function that provides base class objects for frames and other components
window_controller = Tk()

font_size = 24  # Size of the font used for all widgets

# Define the fonts we want to use, including a
# fixed-width one which makes all characters easy to see
main_font = ('Arial', font_size - 8)
small_font = ('Arial', font_size - 12)
title_font = ('Arial Black', font_size, 'bold')
header_font = ('Arial', font_size, 'bold')

main_bg_colour = "#000000"
main_font_colour = "#ffffff"

secondary_bg_color = "#414140"
secondary_font_colour = "#ffffff"

content_bg_color = "#333333"
content_font_color = "#ffffff"

# Store all created window obejcts in a variable for reference in memeory. Allocates set location for window so
# information in one windows doesn't affect the other
windows = []

# Define the news types, their corrisponding catch line or title and the location of their banner image
news_types = ["Medical"]
news_titles = {"Medical": "Inject This News"}
news_banners = {"Medical": "medical_banner.gif"}
# ** MEDICAL IMAGE CREDIT **
# The National Health Council US
# https://nationalhealthcouncil.org/blog/flu-season-update-more-than-half-of-the-us-population-remains-unvaccinated/

# Define available news sources
news_sources = ["ABC News", "Nine News", "British Broadcasting Corporation", "Brisbane Times"]
source_links = {"ABC News": "https://www.abc.net.au/news/topic/medical-research",
                "Nine News": "https://www.9news.com.au/medical",
                "British Broadcasting Corporation": "https://www.bbc.com/news/health",
                "Brisbane Times": "https://www.brisbanetimes.com.au/topic/queensland-health-jb8"}

# Define Custom Button Images in each present state (Default, Hover, Pressed, Selected)
# Define export by default as that will never change
# Append new sources later as we use the news_source variable to get latest news source information
images = dict(
    upexport=PhotoImage(file="buttons/export/default.png", name='upexport'),
    hoverexport=PhotoImage(file="buttons/export/hover.png", name='hoverexport'),
    downexport=PhotoImage(file="buttons/export/pressed.png", name='downexport'),
    selexport=PhotoImage(file="buttons/export/selected.png", name='selexport'),
)

# Loop through news outlets and setup button binding events and assign image
for news_outlet in news_sources:
    # Current position of news source (Index value)
    current_event_pos = str(news_sources.index(news_outlet));
    # Determine folder name comprised of news outlet lowercased and removing all spaces
    news_btn_folder_name = news_outlet.lower().replace(" ", "")

    # Define default binding image
    images["up" + current_event_pos] = PhotoImage(file="buttons/" + news_btn_folder_name + "/default.png",
                                                  name='up' + current_event_pos)
    # Define hover binding image
    images["hover" + current_event_pos] = PhotoImage(file="buttons/" + news_btn_folder_name + "/hover.png",
                                                     name='hover' + current_event_pos)
    # Define pressed binding image
    images["down" + current_event_pos] = PhotoImage(file="buttons/" + news_btn_folder_name + "/pressed.png",
                                                    name='down' + current_event_pos)
    # Define selected binding image
    images["sel" + current_event_pos] = PhotoImage(file="buttons/" + news_btn_folder_name + "/selected.png",
                                                   name='sel' + current_event_pos)


class MarkupScraper():
    def __init__(self, source, file):
        # Store selected news source for reference in functions to determine what regex to use
        self.selected_source = source
        self.html_file = file
        pass

    def __getRegEx(self, process):
        source_name_selected = news_sources[self.selected_source]
        # We check against news_source position value to make it easier to change sources in the code
        if (source_name_selected == news_sources[0]):  # ABC News (Predefined Reg Exp For Source At Position)
            if (process == "title"):
                return '<h3[^>]*data-component=\"CardHeading\"><span[^>]*><a[^>]*>([^<]+)</a></span></h3>'
            elif (process == "abstract"):
                return '<div[^>]*data-component=\"CardDescription\">([^<]+)</div>'
            elif (process == "datetime"):
                return '<span[^>]*CardTimestamp[^>]*><time[^>]*dateTime=\"([^<]+)\">.*?</time>.*?</span>'

        elif (source_name_selected == news_sources[1]):  # Nine News (Predefined Reg Exp For Source At Position)
            if (process == "title"):
                return '<div class=\"story__details\"[^>]*>.*?<h3 class=\"story__headline\"[^>]*><a[^>]*><span class=\"story__headline__text\">([^<]+)</span></a></h3>.*?</div>'
            elif (process == "abstract"):
                return '<div class=\"story__details\"[^>]*>.*?<div class=\"story__abstract\"[^>]*>([^<]+)</div>.*?</div>'
            elif (process == "datetime"):
                return '<div class=\"story__details\"[^>]*>.*?<span class=\"story__extras\"[^>]*>.*?<time class=\"story__time\"[^>]*>([^<]+)</time></span>.*?</div>'
        elif (source_name_selected == news_sources[2]):  # BBC News (Predefined Reg Exp For Source At Position)
            if (process == "title"):
                return '<div[^>]*gs-c-promo-body[^>]*>.*?<h3[^>]*gs-c-promo-heading__title[^>]*>([^<]+)</h3></a>'
            elif (process == "abstract"):
                return '<div[^>]*gs-c-promo-body[^>]*>.*?<p[^>]*gs-c-promo-summary[^>]*>([^<]+)</p></div>'
            elif (process == "datetime"):
                return '<time[^>]*date qa-status-date[^>]*dateTime=\"([^<]+)Z\".*?>.*?</time>'
        elif (source_name_selected == news_sources[3]):  # Brisbane Times (Predefined Reg Exp For Source At Position)
            if (process == "title"):
                return '<div[^>]*story-tile[^>]*>.*?<h3[^>]*article-headline[^>]*><a[^>]*>([^<]+)</a></h3>.*?</div>'
            elif (process == "abstract"):
                return '<div[^>]*story-tile[^>]*>.*?<p[^>]*>([^<]+)</p>.*?</div>'
            elif (process == "datetime"):
                return '<div[^>]*story-tile[^>]*>.*?<ul[^>]*>.*?<time[^>]*dateTime=\"([^<]+)\">.*?</time>.*?</ul>.*?</div>'
        print("Bad News vs Selection Error")
        return "NoRegEx"

    def scrapeTitle(self):
        # Define pattern
        pattern = self.__getRegEx("title")
        # Try to find pattern and catch the error to avoid program crashing
        try:
            results = findall(pattern, self.html_file) # Return value from regex
            first_occurance = results[0]
            return html.unescape(first_occurance) # Return unescaped text data
        except:
            return "Failed to scrape Title"

    def scrapeAbstract(self):
        # Define pattern
        pattern = self.__getRegEx("abstract")
        # Try to find pattern and catch the error to avoid program crashing
        try:
            results = findall(pattern, self.html_file) # Return value from regex
            first_occurance = results[0]
            return html.unescape(first_occurance) # Return unescaped text data
        except:
            return "** The abstract was not able to be scraped, this could be due to internet connectivity issues."

    def scrapeTime(self):
        # Define pattern
        pattern = self.__getRegEx("datetime")
        #Try to find pattern and catch the error to avoid program crashing
        try:
            results = findall(pattern, self.html_file) # Return value from regex
            first_occurance = results[0]
            return html.unescape(first_occurance) # Return unescaped text data
        except:
            return "Failed to scrape Time/Date element"

class SQLite():
    def __init__(self, file_path):
        self.file_path = file_path
    def insert(self, table_name, values):
        # Make a connection to the specified database
        try:
            connection = connect(database=self.file_path)
        except:
            # return false as if we didn't connect we obvisouly didn't insert any rows
            return False

        # Get a cursor on the database
        cursor = connection.cursor()

        # Construct the SQLite insert statement
        sql = "INSERT INTO "+table_name+" VALUES(?,?,?,?)",values

        # Execute the query
        cursor.execute(*sql)

        # Get the count of the number of rows inserted
        rows_inserted = cursor.rowcount

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if rows_inserted > 0:
            return True
        return False

    def select(self):
        pass

# Creating a NewsWindow object, this allows us to reuse the news window code and create multiple news windows if
# required, we can also define the news type being shown in each window and customise them accordingly
class NewsWindow(Frame):
    def __init__(self, master=None, window_size="1080x560", news_type=None):
        super().__init__(master)
        self.master = master

        # Check if the windows news type is valid and set the news type for reference later in the object
        if news_type in news_types:
            self.news_config = news_type
        else:
            print("WINDOW ERROR: NEWS TYPE DOESN'T EXIST")
            return

        # set window minimum size constraints. Define as class variables to access in components rendering
        # width constraints
        self.menu_minwidth = 260
        self.newsdisplay_minwidth = 540
        self.minwidth = self.menu_minwidth + self.newsdisplay_minwidth
        # height constraints
        self.minheight = 560
        self.maxheight = 560

        # set the window size passed on object creation
        # to make window responsive we determine the operating system and adjust window size accordinly
        from sys import platform
        if platform == "darwin":
            self.master.geometry(window_size)
        elif platform == "win32":
            self.master.geometry("1100x600")
            self.minheight = 600
            self.maxheight = 600

        self.master.configure(bg=secondary_bg_color)

        # self.master.resizable(0,0) # Make window not resizeable (Fixed Size)

        # set window minimum size to not be less then containers size
        self.master.minsize(self.minwidth, self.minheight)
        self.master.maxsize(4000,self.maxheight)

        # set title of window based on the chosen news category
        self.master.title(news_titles[self.news_config] + " (" + self.news_config + ")")

        # set the grid of the view for content to go into
        self.master.columnconfigure(0, weight=1, minsize=self.menu_minwidth)
        self.master.columnconfigure(1, weight=3, minsize=self.newsdisplay_minwidth)

        # Define side bar and news panel, created later
        self.side_bar = None
        self.news_panel = None

        # We need to control this object for disabled state and non disabled
        self.export_btn = None

        # Define our database for Windows's Selected News Sources
        self.database = SQLite("databases/"+self.news_config.lower().replace(" ", "")+"/selected_news.db")

        # Define news story visual items for reference
        self.story_label = Text
        self.story_abstract = Text
        self.other_info = Label

        # Store the currently displayed values as StringVar for headline and footer
        self.footerinfo = StringVar()
        self.footerinfo.set(
            "Modified: No Source Selected\nNews Source: No Source Selected\nHostname: No Source Selected\nURL: No Source Selected")

        # store new source menu items for potential access down the track
        self.menuitems = []

        # store the currently selected news source as a string var for Tkinter to read and write in non main thread
        # classes
        self.source_selection_value = StringVar(self.master, "-1")

        # Dummy export value to achieve same appearence in export button, will create a better UX for the user
        self.exportValue = StringVar(self.master, "save")
        # Define place holder variable (Location in memory) for pre defined export data
        self.export_data = []

        # begin compiling the window and it's components
        self.__setup_window()

    def __setup_window(self):
        # Create the left side bar containing news selection, banner image and validate source button
        self.__create_sidebar()

        # create the right panel that will display the news article information
        self.__create_news_area()

    def render_window(self):
        # Final command called to render window, it tells python that the window has finished being designed and it
        # can move back to the main thread of the program
        self.master.mainloop()
        self.mainloop()

    def __set_header_image(self):
        # Access outside of class object, images won't load unless we declaire this as global (Outside class memory)
        global banner_image
        banner_image = PhotoImage(file=news_banners[self.news_config])
        self.banner_holder.configure(image=banner_image)  # configure the banner image

    def __create_sidebar(self):
        # Sidebar navigation style menu
        # all side bar components are nested in here (News Sources, Validate action, Banner image)
        # *** Humans read left to right so it only makes sense to build an application where setting panels
        # *** are to the left and content on the right. It also follow modern design principles

        # create banner image and place at the top of the left side menu
        self.banner_holder = Label(self.master, borderwidth=0, highlightthickness=0, padx=0,
                                   pady=0, background=secondary_bg_color)
        self.__set_header_image()
        self.banner_holder.grid(row=0, rowspan=2, column=0, sticky=NSEW)

        # Middle Section for switch buttons
        # this is the primary section of the left panel
        self.news_select_grid = Frame(self.master, background=secondary_bg_color)
        self.news_select_grid.grid(row=2, rowspan=2, column=0, pady=20)

        # create customn switch buttons for news navigation
        # custom switch creates a familar feeling to modern desktop applications
        # iterate through each available sources and show
        for source in news_sources:
            item = SwitchControl(self.news_select_grid, vari=self.source_selection_value, value=f'{news_sources.index(source)}',
                                 command=self.__onNewsChange, parent=self, highlightthickness=0, bd=0, relief='flat')
            self.menuitems.append(item)
            item.pack(anchor=W)

        # create validate button in the bottom grid part of the left panel
        # use lambda in command to stop the function from running when program starts
        self.validate_btn = Button(self.master, font=header_font, background="#ffffff",
                                   command=lambda: self.__validateSource(), text="Validate Source", pady=5, width=15,
                                   activeforeground=secondary_font_colour, relief='raised')
        self.validate_btn.grid(row=4, column=0, pady=0, padx=5)

    def __create_news_area(self):
        # crete the right panel called news frame, news contwent will be placed in here

        # create the section or header label (unrelated to news) and add export button to top right
        # use lambda in command to stop the function from running when program starts
        self.header_label = Label(self.master, text="Latest News in " + self.news_config, font=header_font,
                                  fg=main_font_colour,
                                  background=main_bg_colour, padx=20, pady=18, anchor=SW)
        self.header_label.grid(row=0, column=1, sticky=EW)

        # Export button is disabled by default because no news source is selected
        # To achieve a disabled appearence and functionality we set the SwitchControl as Image and change it
        # when news it selected
        self.export_btn = Label(self.news_panel, borderwidth=0, highlightthickness=0, padx=0,
                                   pady=0, background=secondary_bg_color)
        global export_disabled # Define variable as global so we can access the image (Outside of Class memory location)
        export_disabled = PhotoImage(file="buttons/export/disabled.png")
        self.export_btn.configure(image=export_disabled)
        self.export_btn.grid(row=0, column=1, sticky=E, padx=15)



        self.story_label = Text(self.master, wrap=WORD,
                                bg=content_bg_color, font=title_font,
                                borderwidth=0, relief='flat',
                                takefocus=False, height=2, width=47,
                                padx=20, pady=15, bd=0, highlightthickness=0)

        # inset inital text into abstract field
        self.story_label.insert(END, "Please select a news source!")
        self.story_label.grid(row=1, column=1, sticky=NSEW)
        # configure foreground
        self.story_label.configure(foreground=content_font_color)
        # assists in remove border, remove highlight when selected
        self.story_label.tag_configure('highlight', background=content_bg_color)

        # create story_abstract section inside news_panel grid
        self.story_abstract = Text(self.master, wrap=WORD,
                                   bg=content_bg_color, font=main_font,
                                   borderwidth=0, relief='flat',
                                   takefocus=False, height=1,
                                   padx=20, pady=15, bd=0, highlightthickness=0)

        # inset inital text into abstract field
        self.story_abstract.insert(END, "")
        self.story_abstract.grid(row=2, rowspan=2, column=1, sticky=NSEW)
        # configure foreground
        self.story_abstract.configure(foreground=main_font_colour)
        # assists in remove border, remove highlight when selected
        self.story_abstract.tag_configure('highlight', background=content_bg_color)

        # create other info section inside news_panel grid
        self.other_info = Label(self.master, textvariable=self.footerinfo, font=small_font,
                                fg=content_font_color, background=content_bg_color, padx=20, pady=22,
                                anchor=W, justify=LEFT)
        self.other_info.grid(row=4, column=1, sticky=NSEW)

    def __onNewsChange(self):
        # Define source name here as we use it regularly throughout the function
        source_name = news_sources[int(self.source_selection_value.get())]
        source_url = source_links[source_name]

        # Check if button is still disabled, enable it for news story
        # Export Button is set as a Label with the disabled image of the button when we want to "disable" it
        # we check if it's object type is still a label to determine if it's disabled
        if type(self.export_btn) is Label:
            # we want to destroy the old disabled label to avoid memory leak when we recreate this export btn
            self.export_btn.destroy()
            # Define the export btn as a custom Buttom/Radio Button
            self.export_btn = SwitchControl(self.news_panel, vari=self.exportValue, value=f'{"export"}',
                                    command=lambda: self.__exportSelection(), parent=self)
            # Add new export button to the grid
            self.export_btn.grid(row=0, column=1, sticky=E, padx=15)

        

        # Configure window to indicate something is happening
        self.displayStoryInfo("Loading " + source_name, "",
                              ["", "", "", ""])

        # Download html document of news source here
        source_code = download(url=source_url,
                               target_filename=self.news_config + "_" + source_name + "_Latest",
                               filename_extension="html", save_file=False, incognito=False)
        # UNWRAP NEWS STORY HERE AND PROCESS REG EXP'S
        # Define RegEx Manager and pass current news selection to the manager to process
        regex_manager = MarkupScraper(int(self.source_selection_value.get()), source_code)

        # DEFINE INFORMATION TO SHOW FROM REGEX AND OTHER SOURCES
        title = regex_manager.scrapeTitle()
        abstract = regex_manager.scrapeAbstract()
        datetime = regex_manager.scrapeTime()
        host_name = urlparse(source_url).netloc

        # PASS INFO TO DISPLAY ON USER INTERFACE
        self.displayStoryInfo(title, abstract, [datetime, source_name, host_name, source_url])

        # Prepare scraped data, ready for exporting
        self.export_data = [datetime,title,abstract,source_name]

    def __validateSource(self):
        # ODETERMINE IF A SOURCE IS SELECTED
        if(int(self.source_selection_value.get()) != -1):
            source_name = news_sources[int(self.source_selection_value.get())]
            link = source_links[source_name]
            # Open users default web browser or open a new tab in a current window of the default browser
            webbrowser.open_new_tab(link)
        else:
            self.displayStoryInfo("Select a news source first!",
                                  "To validate news sources you must select a news source first!",
                                  ["No Source Selected",
                                   "No Source Selected",
                                   "No Source Selected",
                                   "No Source Selected"])

    def __exportSelection(self):
        # Save data to database
        # Data in order of table [DateTime, Headline, Abstract, Source]

        # Attempt to insert pre-prepared export data into database using predefined database instance
        # Adding data into latest_news table
        if self.database.insert("latest_news",self.export_data):
            # Inform the user that the story has been exported. Good UX practice
            self.story_label.insert(END, " (EXPORTED)")
        else:
            # This shouldn't happen unless the file is unwriteable or doesn't exist
            # Show a default error message box to the user letting them know we failed to save to database
            messagebox.showerror(title="Failed to export news story!",
                                 message="The database file might be busy or is currently in use. Try again.")

        # Return button value back to default so it can be used again (Reset State to default)
        self.exportValue.set("save")

    def displayStoryInfo(self, storyTitle, storyAbstract, footerData):
        #                       String      String          Array[]
        # Set new headline title
        self.story_label.delete('1.0', END)
        self.story_label.insert(END, storyTitle)

        # Clear abstract then set new abstract
        self.story_abstract.delete('1.0', END)
        self.story_abstract.insert(END, storyAbstract)

        # set footer content
        self.footerinfo.set(
            "Modified: " + footerData[0] + "\nNews Source: " + footerData[1] + "\nHostname: " + footerData[
                2] + "\nURL: " + footerData[3] + "")

        self.update()


# Set the type of news we want this window to display
# Create a medical window using the main window controll
# calls custom class object to manage the window and it's children objects
medical_news_window = NewsWindow(master=window_controller, news_type="Medical")
# add window to array of windows so we can access the window and its function in later code
# also separates the windows using different locations in memory, windows will not collide.
windows.append(medical_news_window)

# Render all windows created if window has been passed a valid config else do not make it (Destroy)
for window in windows:
    if hasattr(window, 'news_config'):
        # Call window instance in open windows and do final renders, run idle tasks
        window.render_window()
    else:
        print("A window was destoryed because it was passed invalud news types")
        windows.pop(window)

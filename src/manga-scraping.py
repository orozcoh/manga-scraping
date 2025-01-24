#------------------------------- Libraries Imports -----------------------------------

from base64 import urlsafe_b64decode
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import requests
import sys
import os
import io
import time
import random

# ----------------------------------------------------------------------------------------
#---------------------------------- CLI Variables and UI ---------------------------------
# ----------------------------------------------------------------------------------------

if len(sys.argv) == 2:
    startChapter =int(sys.argv[1])
    n = 10
    print("\n"," "*20, "-"*15,"\n"," "*20,"Hunter x Hunter\n"," "*20,"-"*15, sep="")
    print("\nDownload starting from chapter: ", startChapter)
    print("3rd parameter not given - 10 Chapters to download\n")
elif len(sys.argv) == 3:
    startChapter = int(sys.argv[1])
    n = int(sys.argv[2])
    print("\n"," "*16, "-"*20,"\n"," "*20,"Hunter x Hunter\n"," "*20,"-"*20, sep="")
    print("\nDownload starting from chapter: ", startChapter)
    print("Chapters to download:", n, "\n")
else:
    print("\n","-"*53,"\n"," "*17,"Manga Scraper\n","-"*53, sep="")
    print("\nAvailable Mangas:")
    print("\n1: One Piece\n2: Hunter X\n3: Bleach\n4: Jujutsu Kaisen\n\n" + "-"*53)
    option = int (input("\nSelect manga (1, 2, 3 or 4): "))
    startChapter = int(input("\nWhich chapter do you want to start downloading from:  "))
    n = int(input("\nHow many chapters do you want to download:  "))

    temp_name = "NOT VALID"

    if option == 1:
      temp_name = "ONE PIECE"
    elif option == 2:
      temp_name = "HUNTER X"
    elif option == 3:
      temp_name = "BLEACH"
    elif option == 4:
      temp_name = "JUJUTSU KAISEN"
    
    print(f"\n{"-"*53}\n   Downloading chapters: {str(startChapter)} -> {str(startChapter + n-1)} of {temp_name}\n {"-"*53}")
# ----------------------------------------------------------------------------------------------------
# ------------------------------ GLOBAL VARIABLES BASED ON CLI OPTIONS -------------------------------
# ----------------------------------------------------------------------------------------------------
url_OP = ""
url_Bleach = "https://w16.bleach.live/manga/bleach-chapter-"
url_HxH = 'https://hunterxhuntermanga.online/manga/hunter-x-hunter-chapter-'
url_JK = "https://thejujutsukaisenmanga.online/manga/jujutsu-kaisen-chapter-"
url_JJK = "https://thejujutsukaisenread.com/jujutsu-kaisen-chapter-"    

urls = { 'One Piece': url_OP, 'Hunter X': url_HxH, "Bleach": url_Bleach, "Jujutsu Kaisen": url_JK}

if option == 1:
  url = urls['One Piece']
  folder_name = "mangas/one_piece"
  chapter_name = "One_Piece_"
  cover = Image.open("./assets/cover/OP_cover.jpeg")
elif option == 2:
  url = urls['Hunter X']
  folder_name = "mangas/hunter_x"
  chapter_name = "HxH_"
  cover = Image.open("./assets/cover/HxH_cover.jpeg")
elif option == 3:
  url = urls['Bleach']
  folder_name = "mangas/bleach"
  chapter_name = "Bleach_"
  cover = Image.open("./assets/cover/Bleach_cover.jpeg")
elif option == 4:
  url = urls['Jujutsu Kaisen']
  folder_name = "mangas/jujutsu_kaisen"
  chapter_name = "JJK_"
  cover = Image.open("./assets/cover/JJK_cover.jpeg")
else:
  print("\n\nOption selected no valid, try again.\n\n")

# ----------------------------------------------------------------------------------------
#----------------------------------- Directory creation ---------------------------------
# ----------------------------------------------------------------------------------------

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# ----------------------------------------------------------------------------------------
# ---------------------------- THIS IS UNIQUE PER WEBPAGE --------------------------------
# --------------------------- CHAPTER IMAGES URL EXTRACTION-------------------------------
# ----------------------------------------------------------------------------------------  <<<<<<---------- Add custom get per manga

def ImgLinkExtraction(html_parsed_soup):
  temp_links = html_parsed_soup.find_all("meta", property="og:image")

  for i in range(len(temp_links)):
      temp_links[i] = temp_links[i].get('content')

  img_links = []

  for link in temp_links:
      if not link in img_links:
          img_links.append(link)

  return img_links

# ----------------------------------------------------------------------------------------
#------------------------------- Download function definition ----------------------------
# ----------------------------------------------------------------------------------------

def DownloadChapter(chapter):

  # GET request for each chapter, html parse with beautifulSoup
  resp = requests.get((url + "1-2") if option == 1 and chapter == 1 else (url + str(chapter)))    # how to avoid if on one piece
  soup = BeautifulSoup(resp.content, 'html.parser')
  # Extract images url from soup
  img_links = ImgLinkExtraction(soup)

  # -----------------------------------------------------------------------------------------
  # ----------------------------- DOWNLOAD IMAGES -> ADD TO ARRAY ---------------------------
  # -----------------------------------------------------------------------------------------

  print("Downloading",len(img_links), "pages from Chapter:", chapter)

  chapter_img = []

  for page, link in enumerate(img_links):
    r = requests.get(link)
    try:
      im = Image.open(io.BytesIO(r.content))
    except:
      print("\nmissing page")
      #im = current_cover

    chapter_img.append(im)

  # -----------------------------------------------------------------------------------------
  # ------------------------------------- PDF CREATION --------------------------------------
  # -----------------------------------------------------------------------------------------

  current_cover = cover.copy()    # Copy cover to avoid drawing over previous cover
  chapter_str = f"{chapter:02d}"  # Automatically pad with leading zeros
  chapter_pdf_name = f"./{folder_name}/{chapter_name}{chapter_str}.pdf"   # Set pdf name
  font = ImageFont.truetype("./assets/fonts/Road_Rage.otf", 300)          # Load custom font .otf file

  draw = ImageDraw.Draw(current_cover) # Call the ImageDraw functions to make the image editable 

  # Depending on how many digits needs to be drawn the text has to be position differently
  if len(chapter_str) == 2:
     draw.text((350, 1000), chapter_str, font=font, fill=(0,0,0)) 
  elif len(chapter_str)  == 3:
    draw.text((280, 1000), chapter_str, font=font, fill=(0,0,0)) 
  elif len(chapter_str)  == 4:
    draw.text((210, 1000), chapter_str, font=font, fill=(0,0,0)) 
  else:
     print("This should never be, too long :)")

  if (len(chapter_img) < 5):
    current_cover.save("Bad_File_" + str(chapter), save_all=True, append_images=chapter_img)
  else:
    current_cover.save(chapter_pdf_name, save_all=True, append_images=chapter_img)
#----------------------------------------------------------------------------------------

#------------------------------------- MAIN ---------------------------------------------
if __name__ == "__main__":
    start_time = time.time()  # Get script start time
    fail_download = []        # Where chapter number of failed downloads is stored 
    waited_time = 0           # Time waited due to random 1 -> 10 sec between scrapings

    try:
        print("Press Ctrl+C to stop\n\n")
        for i in range(startChapter, startChapter + n):
            try:
                DownloadChapter(i)
            except Exception as e:
                print(f"Could not download chapter: {i}")
                fail_download.append(i)

            wait_time = random.randint(1, 10)
            wait_start = time.time()
            try:
                time.sleep(wait_time)
                waited_time += wait_time  # Full wait if not interrupted
            except KeyboardInterrupt:
                # Add partial waited time (if sleep was interrupted)
                waited_time += time.time() - wait_start
                raise  # Re-raise to exit the loop

    except KeyboardInterrupt:
        print("\n\nEarly exit requested!")

    # culculation of elapsed time + waited time
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    wminutes = int(waited_time // 60)
    wseconds = int(waited_time % 60)

    # Print results
    print(f"\nElapsed time: {minutes} minutes and {seconds} seconds")
    print(f"Total waited time: {wminutes} minutes and {wseconds} seconds\n")
    if len(fail_download) > 0:
      print("\nThese chapters could not be downloaded:", fail_download, "\n") 
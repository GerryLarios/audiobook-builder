import argparse
import PyPDF2
import pyttsx3

def get_args():
  parser = argparse.ArgumentParser(description="Create audio files from PDF files")
  parser.add_argument("--female", type=bool, default= True, help="The voice used in the audio files")
  parser.add_argument("--file", type=str, help="PDF File with the text")
  parser.add_argument("--start", type=int, default=1, help="Page number to start the process")
  parser.add_argument("--language", type=str, default="en_US" ,help="The language used in the audio files")
  parser.add_argument("--output", type=str, help="Folder to storage the audio files")
  return parser.parse_args()

def get_engine(language, female):
  engine = pyttsx3.init()
  gender = "VoiceGenderFemale" if female else "VoiceGenderMale"
  for voice in engine.getProperty('voices'):
    if language in voice.languages and gender == voice.gender:
      engine.setProperty('voice', voice.id)
      return engine
  raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

def get_reader(filename):
  file = open(filename, "rb")
  reader = PyPDF2.PdfFileReader(file)
  return reader

def format_text(text=""):
  return " ".join(text.replace("-", " ").split())

if __name__ == "__main__":
  args = get_args()
  engine = get_engine(args.language, args.female)
  reader = get_reader(args.file)
  num_pages = reader.numPages
  for num_page in range(8, 9):
    print(">>> Page '{}' of {}".format(num_page, num_pages))
    page = reader.getPage(num_page)
    text = format_text(page.extract_text())
    engine.say(text=text)
    engine.runAndWait()
    engine.stop()

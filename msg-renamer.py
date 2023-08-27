from email import policy
from email.parser import BytesParser
import datetime
from pathlib import Path
import os

extension = ".msg"

paths = Path().glob(f"**/*{extension}")

i = 0

for path in paths:
  if path.is_file():
    with open(path, 'rb') as fp:
      msg = BytesParser(policy=policy.default).parse(fp)
      date_header = msg["date"]

      if date_header:
        date_time_str = date_header
        date_time_obj = datetime.datetime.strptime(date_time_str,
                                                   '%a, %d %b %Y %H:%M:%S %z')
        dateoffile = date_time_obj.date().strftime("%Y%m%d")
      else:
        dateoffile = "unknown_date"

      titleoffile = msg['subject'] or "unknown_subject"
      reciever = msg["To"] or "unknown_recipient"
      sender = msg["From"] or "unknown_sender"

      new_filename = f"{dateoffile}  {sender}  {titleoffile}.msg"
      new_filename = new_filename.replace(
          "/", "-")  # Replace forward slashes in filename

      new_path = Path(path.parent, new_filename)
      if new_path.exists():
        new_filename = f"{dateoffile}  {reciever}  {titleoffile}_{i}.msg"
        new_path = Path(path.parent, new_filename)
        i += 1

      os.rename(path, new_path)
      print("File Renamed:", new_path)

      fp.close()  # Close the file

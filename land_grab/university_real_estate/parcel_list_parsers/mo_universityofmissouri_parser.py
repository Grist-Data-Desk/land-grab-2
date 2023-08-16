def moum_parser():
  # if there are ., -, or spaces, take those out and concatenate
  # if there are ; or & symbols, those are delimiters; the values listed are individual parcel IDs
  # if there is a string description, return that line so we can inspect
  # if there are values within parens, return that line so we can inspect
  # use column 8 or [7]
  # ignore header cell
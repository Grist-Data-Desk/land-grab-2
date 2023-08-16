def cauc_parser(l):
  # take out - and spaces, concatenate
  # commas and semicolons are usually delimiters, but sometimes it separates the last few digits, which
  # technically are like additional parcel IDs, with a slight change at the end
  # sometimes it has "or" to also indicate new ID combo with the last few digits being different
  # weird adjustments need to be made for some of the strings (string descriptions include 'and', further desc. etc)
  # return cells with weird strings for additional parsing

  pass
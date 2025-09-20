This is the say executable I built off of my modified version of DECTalk. Here are a list of changes from the original
DECTalk program:

 - expanded vocal range from C2-C5 to A1-E5
 - increased pitch interpolation rate from ~100ms to ~50ms (duration to glide from one note to another)
 - removed comma pause (tl;dr: fuck commas)
 - added intonation correction
 - rewrote notetab[] (from A4=432Hz to A4=440Hz) and removed original pitch correction (because it was wrong)

from PIL import Image
import os, os.path
import cv2
import SaltPeperFilter
import RotateImage
import GaussFilter
import AddGlasses
import AddBeard
import Merge2Imges
import argparse

import sys, getopt

def main(argv):

  parser = argparse.ArgumentParser()
  parser.add_argument('--filter', type=int, choices=[1, 2, 3,4,5,6],required=True,
                     help = 'Zvolte cislo filra:, 1-pridanie brady 2-Gauss filter 3-SaltPeper filter 4-Rotacia 5-pridanie okuliari 6-prekrytie s obrazkom')
  parser.add_argument('--infile', type=str,required=True,
                      help='Zadajte cestu k priecinku, s ktoreho cerpat obrazky')
  parser.add_argument('--outfile',type=str, required=True,
                      help='Zadajte cestu k priecinku, do ktoreho zapisat obrazky')
  parser.add_argument('--uhol', type=int, default=60,
                      help='Nepovinny, zadajte uhol o aky ma byt obrazok otoceny, pouzitelny len pri filtri 4, default=60')
  parser.add_argument('--gauss', type=int, default=99,
                      help='Nepovinny, zadajte rozmer matice aka ma byt pouzita pri Gaussovi, pouzitelny len pri filtri 3, default=99, pozor rozmer musi byt neparny')
  parser.add_argument('--saltpepper', type=int, default=5,
                      help='Nepovinny, zadajte hustotu filtra v percentach, pouzitelny len pri filtri 3, default=5')
  parser.add_argument('--prekrytie', type=int, default=50,
                      help='Nepovinny, zadajte aku vahu ma mat vami zadany obrazok v percentach, pouzitelny len pri filtri 6, default=50')
  args = parser.parse_args()
  filter = args.filter;
  iPath = args.infile;
  oPath = args.outfile;
  uhol  =args.uhol;
  matrix = args.gauss;
  saltpepper = args.saltpepper/float(100);
  weight  =args.prekrytie/float(100);

  imgs = []
  valid_images = [".jpg", ".gif", ".png", ".tga"]
  for f in os.listdir(iPath):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
      continue
    imgs.append(Image.open(os.path.join(iPath, f)))
    path = os.path.join(iPath, f)
    opath = os.path.join(oPath, f)

    if filter == 1:
      img = AddBeard.AddBread(path);
      cv2.imwrite(opath, img)
    if filter == 2:
      img = GaussFilter.GaussFilter(path,matrix,);
      cv2.imwrite(opath, img)
    if filter == 3:
      img = SaltPeperFilter.SaltPapperFilter(path,saltpepper);
      cv2.imwrite(opath, img)
    if filter == 4:
      img = RotateImage.RotateImage(path, uhol);
      cv2.imwrite(opath, img)
    if filter == 5:
      img = AddGlasses.AddEyeGlasses(path);
      cv2.imwrite(opath, img)
    if filter == 6:
      img = Merge2Imges.Merge2Imges(path,weight);
      cv2.imwrite(opath, img)




if __name__ == "__main__":
  main(sys.argv[1:])









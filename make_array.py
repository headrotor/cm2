

pitch = 20*25.4/32.0

def make_refstr(i, j):
    tail = "1"
    if j >= 8:
        j = j - 8
        tail = "2"
    return "D{:02d}{}{}".format(i,chr(ord("A") + j),tail)

def make_posxy(i, j, pitch):
    return("{:.4f} {:.4f}".format(pitch*float(i), pitch*float(j)))

maxi = 32
maxj = 16

rownet = ["(net {:d} /row{:d})".format(i+1,i) for i in range(maxi)]
colnet = ["(net {:d} /col{:02d})".format(j+maxi+1,j) for j in range(maxj)]
    

# refstr = "D00A1"
# net1 = "net 1 /row0"
# net2 = "net 2 /col00"
# posxy = "31.101 

mod_template = """
(module LED_THT:LED_D5.0mm (layer F.Cu) (tedit 5995936A) (tstamp 609A22A9)
    (at {posxy})
    (descr "LED, diameter 5.0mm, 2 pins, http://cdn-reichelt.de/documents/datenblatt/A500/LL-504BC2E-009.pdf")
    (tags "LED diameter 5.0mm 2 pins")
    (path /60904BD1)
    (fp_text reference {refstr} (at 1.27 -3.96) (layer F.SilkS) hide
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text value LED_Small_ALT (at 1.27 3.96) (layer F.Fab) hide
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start 4.5 -3.25) (end -1.95 -3.25) (layer F.CrtYd) (width 0.05))
    (fp_line (start 4.5 3.25) (end 4.5 -3.25) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.95 3.25) (end 4.5 3.25) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.95 -3.25) (end -1.95 3.25) (layer F.CrtYd) (width 0.05))
    (fp_line (start -1.29 -1.545) (end -1.29 1.545) (layer F.SilkS) (width 0.12))
    (fp_line (start -1.23 -1.469694) (end -1.23 1.469694) (layer F.Fab) (width 0.1))
    (fp_circle (center 1.27 0) (end 3.77 0) (layer F.SilkS) (width 0.12))
    (fp_circle (center 1.27 0) (end 3.77 0) (layer F.Fab) (width 0.1))
    (fp_text user %R (at 1.25 0) (layer F.Fab) hide
      (effects (font (size 0.8 0.8) (thickness 0.2)))
    )
    (fp_arc (start 1.27 0) (end -1.29 1.54483) (angle -148.9) (layer F.SilkS) (width 0.12))
    (fp_arc (start 1.27 0) (end -1.29 -1.54483) (angle 148.9) (layer F.SilkS) (width 0.12))
    (fp_arc (start 1.27 0) (end -1.23 -1.469694) (angle 299.1) (layer F.Fab) (width 0.1))
    (pad 2 thru_hole circle (at 2.54 0) (size 1.8 1.8) (drill 0.9) (layers *.Cu *.Mask)
      {net1})
    (pad 1 thru_hole rect (at 0 0) (size 1.8 1.8) (drill 0.9) (layers *.Cu *.Mask)
      {net2})
    (model ${{KISYS3DMOD}}/LED_THT.3dshapes/LED_D5.0mm.wrl
      (at (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )
  )
"""



print("**********THIS IS NOT A VALID KICAD FILE**************\n\n")

print("\n******** add this to the list of nets")
for i in range(maxi):
    print("  " + rownet[i])
for j in range(maxj):
    print("  " + colnet[j])
        
print("\n**************add this to the net_class section")
for i in range(maxi):
    print("    (add_net /row{:d})".format(i))
for j in range(maxj):
    print("    (add_net /col{:02d})".format(j))

print("\n*********** add this to the general section at top")        
print("    (nets {})".format(maxi + maxj + 1))        
print("    (modules {})".format(maxi*maxj))        



for i in range(maxi):
    for j in range(maxj):
        print(mod_template.format(refstr = make_refstr(i, j),
                          net1 = rownet[i],
                          net2 = colnet[j],
                          posxy = make_posxy(i, j, pitch=pitch)))
